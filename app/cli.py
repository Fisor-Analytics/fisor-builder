import typer
from app.builder import build_dataset

app = typer.Typer(help="Fisor Builder CLI: turn queries into structured datasets.")

@app.command()
def run(query: str):
    """
    Run Fisor Builder with a natural language query.
    Example:
        fisor-builder run "Canadian construction forecasts for 2025"
    """
    results = build_dataset(query)
    typer.echo(results)

if __name__ == "__main__":
    app()
