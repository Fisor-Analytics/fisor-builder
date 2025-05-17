import json
import re
from app.cohere_query_gen import generate_subqueries, regenerate_subquery
from app.perplexity_client import PerplexityClient
from app.cohere_extractor import extract_dataset_from_text
from app.confidence_validator import evaluate_confidence
from app.dataset_validator import validate_dataset
from app.cache_manager import load_cache, save_cache, get_cached_result, store_result
from app.schemas import BuilderSearchPlan, SearchResult, StructuredInsight
from app.logger import logger

def deduplicate_rows(rows: list[dict]) -> list[dict]:
    """
    Deduplicates a list of dicts even if values are unhashable (e.g., lists).
    """
    unique_serialized = {json.dumps(row, sort_keys=True) for row in rows}
    return [json.loads(row) for row in unique_serialized]

def extract_query_only(text: str) -> str:
    """
    Extracts a usable reformulated query from LLM output.
    """
    match = re.search(r'["“](.+?)["”]', text)
    return match.group(1).strip() if match else text.strip()

def build_search_plan(prompt: str, location: dict = None) -> BuilderSearchPlan:
    logger.info(f"📥 Received prompt: {prompt}")

    # Step 1: Generate subqueries
    queries = generate_subqueries(prompt, count=5)
    logger.info(f"🔍 Generated queries: {queries}")

    client = PerplexityClient()
    raw_results = []
    structured_insights = []
    cache = load_cache()

    MIN_ROWS = 10
    MIN_CONFIDENCE = 0.75
    MAX_ATTEMPTS = 3

    for original_query in queries:
        query = original_query
        logger.info(f"🌐 Processing query: {query}")
        cached = get_cached_result(query, cache)
        cached_rows = cached.get("structured_data", []) if cached else []
        cached_conf = cached.get("confidence_score", 1.0)
        confidence_score = 0.0
        attempts = 0
        final_snippet = ""
        all_rows = cached_rows.copy()
        seen_queries = set()

        while attempts < MAX_ATTEMPTS:
            logger.info(f"🔁 Attempt {attempts + 1} for: {query}")
            response = client.search(query, location=location)

            if "answer" not in response or not response["answer"].strip():
                logger.warning(f"⚠️ No answer returned for query: {query}")
                break

            snippet = response["answer"]
            final_snippet = snippet
            structured = extract_dataset_from_text(snippet)
            confidence = evaluate_confidence(snippet)
            confidence_score = confidence["confidence_score"]

            all_rows += structured
            deduped_rows = deduplicate_rows(all_rows)
            validation = validate_dataset(deduped_rows, confidence_score, min_rows=MIN_ROWS)

            if validation["valid"]:
                logger.info(f"✅ Query passed validation on attempt {attempts + 1}")
                break

            # Reformulate query
            reformulated = regenerate_subquery(query)
            query = extract_query_only(reformulated)

            if query in seen_queries:
                logger.warning(f"⚠️ Detected reformulation loop. Aborting query: {query}")
                break
            seen_queries.add(query)

            attempts += 1

        if len(deduped_rows) >= MIN_ROWS and confidence_score >= MIN_CONFIDENCE:
            structured_insights.append(StructuredInsight(
                query=query,
                snippet=final_snippet,
                structured_data=deduped_rows,
                confidence_score=confidence_score,
                flagged=confidence.get("flagged", False),
                reasoning=confidence.get("reasoning", "")
            ))

            raw_results.append(SearchResult(
                query=query,
                title=response.get("title", ""),
                url=response.get("url", ""),
                snippet=final_snippet
            ))

            store_result(query, {
                "snippet": final_snippet,
                "structured_data": deduped_rows,
                "confidence_score": confidence_score
            }, cache)
        else:
            logger.warning(f"❌ Skipped query due to insufficient data or confidence: {query}")

    save_cache(cache)

    return BuilderSearchPlan(
        topic="auto",
        region="auto",
        time_range="auto",
        intent="analyze",
        search_queries=queries,
        results=raw_results,
        insights=structured_insights
    )
