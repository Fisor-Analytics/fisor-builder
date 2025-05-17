import os
import json
import hashlib
from datetime import datetime

CACHE_FILE = "fisor_cache.json"

def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_query_hash(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()

def get_cached_result(query: str, cache: dict) -> dict:
    key = get_query_hash(query)
    return cache.get(key, {})

def store_result(query: str, result: dict, cache: dict):
    key = get_query_hash(query)
    cache[key] = {
        "query": query,
        "snippet": result.get("snippet", ""),
        "structured_data": result.get("structured_data", []),
        "confidence_score": result.get("confidence_score", 0),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
