import time
from app.builder import build_search_plan
from app.metrics_server import launch_metrics_server
from app.logger import logger
from app.cohere_extractor import extract_dataset_from_text
from app.config import DEFAULT_LOCATION





if __name__ == "__main__":
    launch_metrics_server(port=8001)  # Exposes Prometheus metrics on the /metrics dir

    print(f"[INFO] Default location set to {DEFAULT_LOCATION}")

    prompt = "Analyze housing affordability in Toronto for the last year"
    logger.info("🚀 Starting Fisor Builder")

    start = time.time()
    plan = build_search_plan(prompt, location=DEFAULT_LOCATION)
    duration = round(time.time() - start, 2)
    logger.info(f"⏱️ Completed in {duration} seconds")

    
    print("\nBuilderSearchPlan Output:\n")
    print(plan.model_dump_json(indent=2))

    
    print("\n AI Answers and Extracted Datasets:\n")

    for idx, insight in enumerate(plan.insights):
        print(f"\n {insight.query}")
        print(insight.snippet)

        print(f"\n Structured Dataset:\n")
        if insight.structured_data:
            for row in insight.structured_data:
                print(f" - {row}")
        else:
            print("[No structured data extracted]")

        print(f"\n Confidence: {insight.confidence_score:.2f} | Flagged: {insight.flagged}")
        print(f" Reasoning: {insight.reasoning}")
