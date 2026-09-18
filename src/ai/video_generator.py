import asyncio
import logging
import random

logger = logging.getLogger(__name__)

# Strict English keywords for chemistry validation
CHEMISTRY_KEYWORDS = [
    "acid", "base", "ph", "neutral", "scale", 
    "electrons", "share", "transfer", "covalent", 
    "ionic", "bond", "atoms", "molecules"
]

def validate_chemistry_keywords(output: str) -> bool:
    """
    Check if the output contains at least one relevant chemistry keyword.
    If not, raise ValueError to signal an AI hallucination.
    """
    output_lower = output.lower()
    for kw in CHEMISTRY_KEYWORDS:
        if kw in output_lower:
            return True
            
    raise ValueError("Output does not contain chemistry keywords (Hallucination detected)")

class AIVideoGenerator:
    async def _mock_ai_call(self, query: str) -> str:
        """
        Simulate an expensive AI API call.
        Includes a 20% deliberate hallucination rate to trigger retries.
        """
        await asyncio.sleep(2)
        
        # 20% Hallucination Rate
        if random.random() < 0.2:
            return "The capital of France is Paris. This has nothing to do with science."

        q = query.lower()
        
        if "how does the ph scale work" in q:
            return "Script: The pH scale measures how acidic or basic a substance is. It ranges from 0 to 14, with 7 being neutral. Acids have a pH lower than 7, and bases have a pH higher than 7."
        elif "why do atoms form covalent bonds" in q:
            return "Script: Atoms form covalent bonds by sharing electrons. This allows them to achieve a full outer electron shell, making them more stable and forming strong chemical structures."
        elif "what is the difference between ionic and covalent bonding" in q:
            return "Script: The main difference lies in the electrons. Ionic bonding involves the transfer of electrons from one atom to another, creating charged ions. Covalent bonding involves the sharing of electrons between atoms."
        
        return f"Script: A simulation of {query} involving chemical reactions."

    async def generate_with_retry(self, query: str, max_retries: int = 3) -> str:
        """
        Calls the mock LLM and automatically retries if it hallucinates (fails validation).
        """
        for attempt in range(max_retries):
            try:
                # Call AI
                output = await self._mock_ai_call(query)
                
                # Validate result
                validate_chemistry_keywords(output)
                
                # If no exception, return the valid output
                return output
                
            except Exception as e:
                logger.warning(f"AI generation failed on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt == max_retries - 1:
                    # Exhausted retries, raise the error to be caught by Background Task
                    raise
                
        raise RuntimeError("Failed to generate video script after max retries")
