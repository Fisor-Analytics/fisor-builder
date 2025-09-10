from pydantic import BaseModel
from typing import List, Optional, Union

class SearchResult(BaseModel):
    query: str
    title: str
    url: str
    snippet: str

class StructuredInsight(BaseModel):
    query: str                         # The original subquery
    snippet: str                       # Raw answer from LLM
    structured_data: Union[List[dict], dict]  # Table-like JSON output
    confidence_score: float            # 0.0–1.0 score from validation engine
    flagged: bool                      # True if confidence too low
    reasoning: Optional[str] = None    # LLM explanation (why passed/failed)

class BuilderSearchPlan(BaseModel):
    topic: str                         # Optional placeholder ("auto" for now)
    region: str
    time_range: str
    intent: str                        # e.g., "analyze"
    search_queries: List[str]          # All generated subqueries
    results: List[SearchResult]        # Raw search responses
    insights: List[StructuredInsight]  # Final structured plus scored outputs
