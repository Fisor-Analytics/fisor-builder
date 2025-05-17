from prometheus_client import Counter, Histogram
from prometheus_client import Counter, Gauge

builder_runs_total = Counter(
    "fisor_builder_runs_total", "Total number of builder runs executed"
)

builder_subqueries_total = Counter(
    "fisor_subqueries_generated_total", "Total number of subqueries generated"
)

perplexity_success_total = Counter(
    "fisor_perplexity_success_total", "Successful Perplexity API calls"
)

perplexity_failure_total = Counter(
    "fisor_perplexity_failure_total", "Failed Perplexity API calls"
)

builder_duration_seconds = Histogram(
    "fisor_builder_duration_seconds", "Total time taken to complete builder pipeline"
)

dataset_validation_counter = Counter(
    "dataset_validation_total",
    "Total number of dataset validations",
    ["valid"]
)

dataset_validation_gauge = Gauge(
    "dataset_validation_metric",
    "Validation metric values",
    ["metric"]
)
