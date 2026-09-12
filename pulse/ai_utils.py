import os
from groq import Groq
from rich.console import Console

console = Console()

def generate_standup_summary(commits: list[dict]) -> str:
    """
    Sends commit messages to the Groq API to produce a daily standup format.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        console.print("[bold red]Error:[/bold red] GROQ_API_KEY is missing from your .env file!")
        return "Failed to generate standup: Missing API key."

    # Initialize native Groq client
    client = Groq(api_key=api_key)

    # Format commits into a readable text list for the prompt
    if not commits:
        commit_text = "No recent commits found."
    else:
        commit_text = "\n".join(
            [f"- [{c.get('date', 'N/A')}] {c.get('message', '')} (by {c.get('author', 'Unknown')})" for c in commits]
        )

    prompt = f"""
    You are an AI assistant helping a software developer generate a clear daily standup update.
    Based on the following git commit messages, generate a professional daily standup update with three sections:
    1. 🛠️ **What I worked on recently**
    2. 🎯 **What I am working on next**
    3. 🚧 **Blockers / Risks** (if any inferred, otherwise state 'None')

    Git Commits:
    {commit_text}
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful software engineering assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        console.print(f"[bold red]Groq API Error:[/bold red] {e}")
        return "Failed to generate standup due to API error."