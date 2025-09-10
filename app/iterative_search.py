from app.perplexity_client import PerplexityClient
from app.cohere_query_gen import generate_subqueries
from app.logger import logger

def run_iterative_search(prompt: str, max_queries: int = 5, location: dict = None) -> list[dict]:
    """
    Given a user prompt, generate subqueries and run each using Perplexity.
    Returns a list of results with LLM-generated summaries and search queries.
    """
    logger.info(" Starting iterative search process")

    queries = generate_subqueries(prompt, count=max_queries)
    logger.info(f" Subqueries to run: {queries}")

    client = PerplexityClient()
    all_results = []

    for query in queries:
        logger.info(f" Running Perplexity search: {query}")
        res = client.search(query, location=location)

        if "answer" in res and res["answer"].strip():
            all_results.append({
                "query": res["query"],
                "title": res.get("title", ""),  # Optional, can enrich later
                "url": res.get("url", ""),      # Optional
                "snippet": res["answer"]
            })
        else:
            logger.warning(f"⚠️ No valid answer returned for query: {query}")

    logger.info(f" Total collected results: {len(all_results)}")
    return all_results
