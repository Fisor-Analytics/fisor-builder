import cohere
import json
from app.config import COHERE_API_KEY
from app.logger import logger

client = cohere.Client(COHERE_API_KEY)

def evaluate_confidence(insight_text: str) -> dict:
    """
    Evaluates the factual reliability of a structured insight using Cohere R+.
    Returns:
    - confidence_score: float (0.0 to 1.0)
    - reasoning: short explanation
    - sources_mentioned: int (if inferred)
    - flagged: bool (true if low quality / hallucinated)
    """
    logger.info("🔍 Running confidence evaluation via Command R+")

    prompt = (
        "You are an insight validation agent.\n"
        "Read the following economic or business insight, and return a JSON object with:\n"
        "- confidence_score: float (0.0 to 1.0)\n"
        "- reasoning: short explanation\n"
        "- sources_mentioned: integer\n"
        "- flagged: boolean\n\n"
        "Only return the JSON object.\n\n"
        f"Insight:\n{insight_text.strip()}\n\n"
        "JSON:"
    )

    try:
        response = client.chat(
            model="command-r-plus",
            temperature=0.0,
            max_tokens=500,
            message=prompt,
        )

        raw = response.text.strip()

        # Strip markdown block if exists
        if "```json" in raw:
            raw = raw.split("```json")[-1].strip().rstrip("```").strip()

        logger.info("✅ Confidence evaluation complete.")

        # Safely parse JSON
        return json.loads(raw)

    except Exception as e:
        logger.error(f"❌ Confidence evaluation failed: {e}")
        return {
            "confidence_score": 0.0,
            "reasoning": "LLM evaluation failed or invalid JSON.",
            "sources_mentioned": 0,
            "flagged": True
        }
