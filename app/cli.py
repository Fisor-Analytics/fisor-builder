import typer
from app.builder import build_dataset, build_search_plan
from app.config import DEFAULT_LOCATION

app = typer.Typer(help="Fisor Builder CLI")

@app.command()
def run(
    query: str,
    city: str = typer.Option(DEFAULT_LOCATION["city"], help="City context"),
    country: str = typer.Option(DEFAULT_LOCATION["country"], help="ISO-2 country code"),
):
    location = {"city": city, "country": country}
    plan = build_search_plan(query, location=location)
    typer.echo(plan.model_dump_json(indent=2))

if __name__ == "__main__":
    app()
