import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pulse.config import validate_config
from pulse.git_utils import get_recent_commits
from pulse.ai_utils import generate_standup_summary

app = typer.Typer(
    name="pulse",
    help="⚡ PulseCLI: Daily Standup Generator from Git activity",
    add_completion=False,
)
console = Console()

@app.command()
def generate(
    days: int = typer.Option(1, "--days", "-d", help="Number of days of git history to check"),
    repo_path: str = typer.Option(".", "--path", "-p", help="Path to target git repository"),
):
    """
    Generate a standup update based on local git commits using OpenAI.
    """
    if not validate_config():
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY is missing from your .env file.")
        raise typer.Exit(code=1)

    console.print(Panel.fit("[bold cyan]⚡ PulseCLI[/bold cyan] [bold white]| Standup Generator[/bold white]", border_style="bright_blue"))

    with console.status("[bold green]Fetching Git commits...[/bold green]"):
        commits = get_recent_commits(repo_path, days)

    if not commits:
        console.print(f"[bold yellow]No commits found[/bold yellow] in the last {days} day(s) at '[italic]{repo_path}[/italic]'.")
        return

    console.print(f"📜 Found [bold green]{len(commits)}[/bold green] commit(s). Generating standup with OpenAI...")

    with console.status("[bold magenta]Asking ChatGPT to synthesize standup...[/bold magenta]"):
        summary = generate_standup_summary(commits)

    console.print("\n" + "=" * 50 + "\n")
    console.print(Panel(Markdown(summary), title="🚀 [bold green]Your Daily Standup[/bold green]", border_style="green"))

if __name__ == "__main__":
    app()