# Fisor Builder

Fisor Builder is a research/data pipeline module.  
It converts open-ended natural language questions into **structured datasets** by combining:

- **Cohere Command R+** → reasoning and sub-query generation
- **Perplexity API** → real-time search
- **Custom validators** → structured, validated output

---

## Features
- Iterative query → search → parse loop
- Sub-query generation with Cohere
- Web search integration (Perplexity)
- Structured dataset extraction
- Confidence + dataset validation
- JSON/Redis caching (extensible)
- Prometheus metrics & logger
- Docker + shell deploy scripts

---

## Project Structure

```text
fisor-builder-main/
├── main.py                   # Entrypoint
├── requirements.txt
├── Dockerfile
├── deploy_fisor_builder.sh
├── app/
│   ├── builder.py             # Core orchestration
│   ├── cache_manager.py       # Cache (JSON/Redis)
│   ├── cohere_query_gen.py    # Generate sub-queries
│   ├── cohere_extractor.py    # Extract structured rows
│   ├── confidence_validator.py# Fact-checking / confidence
│   ├── dataset_validator.py   # Dataset schema validation
│   ├── perplexity_client.py   # Perplexity API client
│   ├── iterative_search.py    # Iterative loop logic
│   ├── schemas.py             # Pydantic models
│   ├── logger.py              # Unified logging
│   ├── metrics.py             # Metrics helpers
│   └── metrics_server.py      # Prometheus endpoint
```

## Example Cache
The repo includes `fisor_cache.example.json` as a sample of what the cache output looks like.
The real `fisor_cache.json` is generated at runtime and should not be committed.


## License

MIT – see [LICENSE](LICENSE)

