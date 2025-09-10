import cohere
from app.config import COHERE_API_KEY
from app.logger import logger

client = cohere.Client(COHERE_API_KEY)

def extract_dataset_from_text(text: str, columns: list[str] = None) -> list[dict]:
    """
    Uses Cohere Command R+ to convert a free-form LLM snippet into structured JSON (table-like) data.
    Returns a list of dictionaries (rows).
    """
    logger.info(" Extracting structured data using Cohere Command R+")

    prompt = (
        "You're a data extraction agent.\n"
        "Given the following business insight or answer text, extract a clean dataset in JSON format.\n"
        "Return only valid JSON — a list of dictionaries (each one is a row). Do NOT include explanations or markdown.\n"
    )

    if columns:
        prompt += f"Ensure the following columns are included: {', '.join(columns)}.\n"

    prompt += f"\nInsight:\n{text.strip()}\n\nReturn the dataset only:"

    try:
        chat = client.chat(
            model="command-r-plus",
            temperature=0.0,
            max_tokens=600,
            message=prompt,
        )

        extracted = chat.text.strip()

        if extracted.startswith("```json"):
            extracted = extracted.split("```json")[-1].strip().rstrip("```").strip()

        logger.info(" Extraction successful")
        return eval(extracted) if extracted.startswith("[") else []

    except Exception as e:
        logger.error(f" Dataset extraction failed: {e}")
        return []
