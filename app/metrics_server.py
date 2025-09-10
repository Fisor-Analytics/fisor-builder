from prometheus_client import start_http_server

def launch_metrics_server(port=8001):
    print(f" Prometheus metrics available at http://localhost:{port}/metrics")
    start_http_server(port)
