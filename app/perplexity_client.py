from openai import OpenAI
from app.config import PERPLEXITY_API_KEY
from app.logger import logger
from app.metrics import perplexity_success_total, perplexity_failure_total

client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai",
)

class PerplexityClient:
    def search(self, query: str, location: dict = None) -> dict:
        """
        Uses Perplexity Sonar chat model with built-in web search.
        Optionally refines with location (e.g., {city: 'Toronto', country: 'CA'}).
        """
        logger.info(f" Sonar LLM → Asking: '{query}'")

        web_search_options = {
            "search_context_size": "high"
        }

        if location:
            web_search_options["user_location"] = location
            logger.info(f" Search location context: {location}")

        try:
            response = client.chat.completions.create(
                model="sonar",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You're an AI analyst. Use up-to-date public web data to answer questions factually and clearly."
                        ),
                    },
                    {
                        "role": "user",
                        "content": query,
                    },
                ],
                temperature=0.3,
                extra_body={
                    "web_search_options": web_search_options
                }
            )

            perplexity_success_total.inc()
            return {
                "query": query,
                "answer": response.choices[0].message.content
            }

        except Exception as e:
            perplexity_failure_total.inc()
            logger.error(f"❌ Sonar LLM call failed: {e}")
            return {
                "query": query,
                "answer": "",
                "error": str(e)
            }
