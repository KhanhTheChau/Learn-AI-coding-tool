import os
import sys
import time
import logging
import asyncio
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from gtts import gTTS

logger = logging.getLogger(__name__)

class Scene:
    def __init__(self, query: str, text: str, duration: float, is_intro: bool = False):
        self.query = query
        self.text = text
        self.duration = duration
        self.is_intro = is_intro
        self.layout_cached = False
        self.lines = []
        self.y_start = 0

class VideoAssembler:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.fps = 30
        self.bg_cache = {}
        
        # Cấu hình UI
        self.bg_color_top = (15, 23, 42)    # Slate 900
        self.bg_color_bottom = (30, 41, 59) # Slate 800
        self.card_bg = (255, 255, 255, 255)
        self.shadow_color = (0, 0, 0, 150)
        self.text_color_dark = (15, 23, 42)
        self.text_color_light = (241, 245, 249)
        self.accent_color = (56, 189, 248)  # Sky 400
        
        # Khởi tạo font
        self.font_dir = "src/assets/fonts"
        self._load_fonts()
        
        # Cache layer tĩnh
        self.static_bg = self._create_gradient_bg()
        
    def _load_fonts(self):
        regular = os.path.join(self.font_dir, "Roboto-Regular.ttf")
        bold = os.path.join(self.font_dir, "Roboto-Bold.ttf")
        
        try:
            self.font_title = ImageFont.truetype(bold, 48)
            self.font_query = ImageFont.truetype(bold, 56)
            self.font_answer = ImageFont.truetype(regular, 52)
        except Exception:
            logger.warning("Fonts not found in assets/fonts. Using default fallback.")
            self.font_title = ImageFont.load_default()
            self.font_query = ImageFont.load_default()
            self.font_answer = ImageFont.load_default()

    def _create_gradient_bg(self) -> Image.Image:
        """Tạo background gradient dọc và lưu vào cache."""
        base = np.zeros((self.height, self.width, 3), dtype=np.float32)
        r1, g1, b1 = self.bg_color_top
        r2, g2, b2 = self.bg_color_bottom
        
        # Tạo lưới gradient (tối ưu hóa numpy)
        linspace = np.linspace(0, 1, self.height)[:, None]
        base[:, :, 0] = r1 * (1 - linspace) + r2 * linspace
        base[:, :, 1] = g1 * (1 - linspace) + g2 * linspace
        base[:, :, 2] = b1 * (1 - linspace) + b2 * linspace
        
        return Image.fromarray(np.uint8(base), 'RGB')

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
        words = text.split()
        lines = []
        current_line = []
        
        def get_w(txt):
            if hasattr(font, 'getlength'):
                return font.getlength(txt)
            if hasattr(font, 'getsize'):
                return font.getsize(txt)[0]
            return len(txt) * 20
            
        for word in words:
            current_line.append(word)
            if get_w(" ".join(current_line)) > max_width:
                current_line.pop()
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def _parse_scenes(self, query: str, script: str) -> list[Scene]:
        """Tách answer dài thành nhiều trang. Đảm bảo thời gian đọc."""
        # Chuẩn hóa
        script = script.replace("Script:", "").strip()
        script = script.replace("Kịch bản:", "").strip()
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        
        scenes = []
        # Scene 1: Introduction (Tập trung hiển thị câu hỏi)
        intro_duration = max(3.0, len(query.split()) * 0.5)
        scenes.append(Scene(query, "", intro_duration, is_intro=True))
        
        if not sentences:
            return scenes
            
        # Chia text thành các nhóm không quá dài để hiển thị trên 1 màn hình
        current_chunk = []
        max_words_per_scene = 40
        word_count = 0
        
        for s in sentences:
            s_words = len(s.split())
            if word_count + s_words > max_words_per_scene and current_chunk:
                chunk_text = ". ".join(current_chunk) + "."
                duration = max(4.0, word_count * 0.4)
                scenes.append(Scene(query, chunk_text, duration))
                current_chunk = [s]
                word_count = s_words
            else:
                current_chunk.append(s)
                word_count += s_words
                
        if current_chunk:
            chunk_text = ". ".join(current_chunk) + "."
            duration = max(4.0, word_count * 0.4)
            scenes.append(Scene(query, chunk_text, duration))
            
        # Căn chỉnh layout một lần cho từng scene
        for scene in scenes:
            self._layout_scene(scene)
            
        return scenes

    def _layout_scene(self, scene: Scene):
        """Tính toán Layout Text trước (Wrap, Height, Y position)"""
        if scene.is_intro:
            scene.layout_cached = True
            return
            
        max_w = 1400
        scene.lines = self._wrap_text(scene.text, self.font_answer, max_w)
        line_height = 80
        total_h = len(scene.lines) * line_height
        
        # Đặt dưới question card (Y ~ 450)
        start_y = 500
        scene.y_start = start_y
        scene.layout_cached = True

    def _draw_rounded_shadow_card(self, draw: ImageDraw.ImageDraw, img: Image.Image, x: int, y: int, w: int, h: int, radius: int):
        """Vẽ shadow bằng layer rời rồi alpha_composite (tối ưu nhất Pillow)"""
        # Shadow layer
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        offset = 15
        shadow_draw.rounded_rectangle([x+offset, y+offset, x+w+offset, y+h+offset], radius=radius, fill=self.shadow_color)
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
        
        img.alpha_composite(shadow)
        
        # Card layer
        card = Image.new('RGBA', img.size, (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card)
        card_draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=self.card_bg)
        
        # Accent line ở viền trái
        card_draw.rounded_rectangle([x, y, x+12, y+h], radius=radius, fill=self.accent_color)
        
        img.alpha_composite(card)

    def _get_text_w(self, text, font):
        if hasattr(font, 'getlength'): return font.getlength(text)
        if hasattr(font, 'getsize'): return font.getsize(text)[0]
        return len(text) * 20

    def _get_bg_image(self, query: str) -> Image.Image:
        """Load and map background image based on query with caching"""
        q = query.lower()
        if "ph scale" in q:
            img_path = "src/assets/images/ph_scale.jpg"
        elif "difference" in q or "ionic" in q:
            img_path = "src/assets/images/ionic_vs_covalent.jpg"
        elif "covalent" in q:
            img_path = "src/assets/images/covalent.jpg"
        else:
            return self.static_bg.copy().convert('RGBA')
            
        if img_path in self.bg_cache:
            return self.bg_cache[img_path].copy()
            
        if not os.path.exists(img_path):
            return self.static_bg.copy().convert('RGBA')
            
        try:
            bg = Image.open(img_path).convert('RGBA')
            bg = ImageOps.fit(bg, (self.width, self.height), Image.Resampling.LANCZOS)
            
            # Dark overlay (60% black)
            overlay = Image.new('RGBA', bg.size, (0, 0, 0, int(255 * 0.6)))
            bg.alpha_composite(overlay)
            
            self.bg_cache[img_path] = bg
            return bg.copy()
        except Exception:
            return self.static_bg.copy().convert('RGBA')

    def _render_frame(self, scene: Scene, time_in_scene: float) -> np.ndarray:
        # Base background mapped to query
        frame = self._get_bg_image(scene.query)
        draw = ImageDraw.Draw(frame)
        
        # Calculate Animation (Fade)
        # 0->1s: fade in
        # last 0.5s: fade out (chỉ với scene không phải cuối)
        alpha = 255
        if time_in_scene < 0.8:
            alpha = int(255 * (time_in_scene / 0.8))
        elif time_in_scene > scene.duration - 0.5:
            alpha = int(255 * max(0, (scene.duration - time_in_scene) / 0.5))
            
        # Draw Title (Query) centered at the top
        q_lines = self._wrap_text(scene.query, self.font_query, 1600)
        
        y_t = 120
        for line in q_lines:
            # Center text
            w = self._get_text_w(line, self.font_query)
            x_t = (self.width - w) // 2
            draw.text((x_t, y_t), line, font=self.font_query, fill=self.accent_color)
            y_t += 80
            
        draw.line([(300, y_t + 20), (1620, y_t + 20)], fill=self.accent_color, width=2)
        
        # Draw Script Text (Educational Slide style)
        if not scene.is_intro:
            draw_ans = Image.new('RGBA', frame.size, (0,0,0,0))
            d_ans = ImageDraw.Draw(draw_ans)
            
            y_a = max(y_t + 100, 350)
            
            # Slide up effect and fade
            y_offset = int((1.0 - (alpha/255.0)) * 30)
            
            for line in scene.lines:
                w = self._get_text_w(line, self.font_answer)
                # Left align with generous padding
                d_ans.text((150, y_a + y_offset), line, font=self.font_answer, fill=self.text_color_light + (alpha,))
                y_a += 80
                
            frame.alpha_composite(draw_ans)
            
        # Trả về numpy uint8 (bỏ kênh Alpha để vào rgb24)
        return np.array(frame.convert('RGB'), dtype=np.uint8)

    def _validate_frame(self, frame_np: np.ndarray) -> None:
        if frame_np.shape != (self.height, self.width, 3):
            raise ValueError(f"Invalid frame shape: {frame_np.shape}")
        if frame_np.dtype != np.uint8:
            raise ValueError(f"Invalid frame dtype: {frame_np.dtype}")
        # Chặn black frame tuyệt đối
        if not frame_np.any():
            raise ValueError("Corrupted frame: Completely black")

    async def _generate_audio(self, script: str, audio_path: str) -> bool:
        """Sinh audio TTS với cơ chế Network Fallback"""
        logger.info(f"Generating TTS audio for script (len: {len(script)})")
        try:
            tts = gTTS(text=script, lang='en')
            await asyncio.to_thread(tts.save, audio_path)
            return True
        except Exception as e:
            logger.error(f"TTS Generation failed due to network or API error: {e}")
            # Fallback: Create a silent audio file or simply return False so we can encode without audio if needed.
            # Here we just return False and the muxing logic will handle it.
            return False

    async def assemble_video(self, query: str, script: str, output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Assembling video for: {query}")
        
        start_time = time.time()
        scenes = self._parse_scenes(query, script)
        
        audio_path = output_path.replace(".mp4", ".mp3")
        has_audio = await self._generate_audio(script, audio_path)
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self.width}x{self.height}',
            '-pix_fmt', 'rgb24',
            '-r', str(self.fps),
            '-i', '-',
        ]
        
        if has_audio:
            cmd.extend(['-i', audio_path])
            
        cmd.extend([
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'fast',
            '-crf', '23',
        ])
        
        if has_audio:
            cmd.extend([
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest'
            ])
            
        cmd.append(output_path)
        
        try:
            stderr_file = open(f"{output_path}.log", "w")
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=stderr_file)
            
            total_rendered = 0
            for scene in scenes:
                total_frames = int(scene.duration * self.fps)
                for i in range(total_frames):
                    time_in_scene = i / self.fps
                    
                    frame = self._render_frame(scene, time_in_scene)
                    self._validate_frame(frame)
                    
                    try:
                        process.stdin.write(frame.tobytes())
                        total_rendered += 1
                    except (BrokenPipeError, OSError) as e:
                        # FFmpeg closed the pipe early due to -shortest
                        break
                
                if process.poll() is not None:
                    # process already exited
                    break
                    
            try:
                process.stdin.close()
            except Exception:
                pass
            process.wait()
            stderr_file.close()
            
            if process.returncode != 0:
                with open(f"{output_path}.log", "r") as f:
                    err = f.read()
                raise RuntimeError(f"FFmpeg encode error: {err}")
                
            elapsed = time.time() - start_time
            logger.info(f"Rendered {total_rendered} frames in {elapsed:.2f}s ({total_rendered/elapsed:.1f} fps)")
            
        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            raise
        finally:
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass
            
        return output_path
