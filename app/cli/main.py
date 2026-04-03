import typer
from rich import print

from app.core.config import get_settings
from app.core.database import init_db

app = typer.Typer(help="MemForge CLI")


@app.command()
def initdb() -> None:
    """Initialize local database tables."""
    init_db()
    print("[green]Database initialized.[/green]")


@app.command()
def doctor() -> None:
    """Print current configuration summary."""
    settings = get_settings()
    print("[bold cyan]MemForge Doctor[/bold cyan]")
    print(f"App: {settings.app_name}")
    print(f"Env: {settings.env}")
    print(f"Database: {settings.database_url}")
    print(f"Vector backend: {settings.vector_backend}")
    print(f"Vector dir: {settings.vector_dir}")
    print(f"Embedding provider: {settings.embedding_provider}")
    print(f"Embedding model: {settings.embedding_model}")


if __name__ == "__main__":
    app()
