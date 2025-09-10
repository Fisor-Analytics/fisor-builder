from typing import List
from app.metrics import dataset_validation_counter, dataset_validation_gauge

def validate_dataset(dataset: List[dict], confidence: float, min_rows: int = 10) -> dict:
    """
    Checks if structured dataset meets quality thresholds.
    Records validation metrics to Prometheus.
    """
    if not dataset or len(dataset) < min_rows:
        _update_metrics(valid=False, confidence=confidence, non_null_ratio=0.0, row_count=len(dataset))
        return {
            "valid": False,
            "reason": "Too few rows",
            "metrics": {
                "row_count": len(dataset),
                "confidence_score": confidence,
                "non_null_ratio": 0.0
            }
        }

    field_count = len(dataset[0])
    total_cells = len(dataset) * field_count
    non_null_cells = sum(
        sum(1 for v in row.values() if v not in [None, "", "null"]) for row in dataset
    )
    non_null_ratio = non_null_cells / total_cells if total_cells else 0
    valid = confidence >= 0.75 and non_null_ratio >= 0.85

    _update_metrics(valid, confidence, non_null_ratio, len(dataset))

    return {
        "valid": valid,
        "reason": "Passed" if valid else "Low confidence or too many nulls",
        "metrics": {
            "row_count": len(dataset),
            "field_count": field_count,
            "confidence_score": confidence,
            "non_null_ratio": round(non_null_ratio, 2)
        }
    }

def _update_metrics(valid: bool, confidence: float, non_null_ratio: float, row_count: int):
    dataset_validation_counter.labels(valid=str(valid)).inc()
    dataset_validation_gauge.labels(metric="confidence").set(confidence)
    dataset_validation_gauge.labels(metric="non_null_ratio").set(non_null_ratio)
    dataset_validation_gauge.labels(metric="row_count").set(row_count)

def print_metrics(metrics: dict):
    print("\n Dataset Metrics:")
    for key, value in metrics.items():
        print(f" - {key.replace('_', ' ').capitalize()}: {value}")
