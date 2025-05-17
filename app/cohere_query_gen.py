import os
import cohere
from app.config import COHERE_API_KEY
from app.metrics import builder_subqueries_total
from app.logger import logger

client = cohere.Client(COHERE_API_KEY)

def generate_subqueries(prompt: str, count: int = 4) -> list[str]:
    """
    Use Cohere Command R+ to generate subqueries from a user prompt.
    Returns a list of subqueries (str).
    """
    logger.info("🧠 Generating subqueries via Cohere Command R+")

    system_msg = (
        "You're a research planner. Break the user's prompt into multiple specific web search queries "
        "that can be run independently to gather data for a report. Keep them short and relevant."
    )

    try:
        chat = client.chat(
            model="command-r-plus",
            temperature=0.3,
            max_tokens=300,
            message=prompt,
            preamble=system_msg
        )

        raw_output = chat.text.strip()
        subqueries = [line.lstrip("-•1234567890. ").strip() for line in raw_output.split("\n") if line.strip()]
        
        builder_subqueries_total.inc(len(subqueries))
        logger.info(f"📌 Subqueries generated: {subqueries[:count]}")
        return subqueries[:count]

    except Exception as e:
        logger.error(f"❌ Cohere subquery generation failed: {e}")
        return []


def regenerate_subquery(query: str) -> str:
    """
    Reformulates a failed query into a new variation using Cohere.
    """
    logger.info(f"♻️ Reformulating query: {query}")
    prompt = f"Rewrite this web search query using different phrasing: \"{query}\""

    try:
        chat = client.chat(
            model="command-r-plus",
            temperature=0.4,
            max_tokens=100,
            message=prompt
        )
        reformulated = chat.text.strip().strip('"')
        logger.info(f"🔁 Reformulated query: {reformulated}")
        return reformulated
    except Exception as e:
        logger.error(f"❌ Cohere query regeneration failed: {e}")
        return query  # fallback
