from openai import OpenAI
from pulse.config import OPENAI_API_KEY

def generate_standup_summary(commits: list[dict]) -> str:
    """
    Sends commit messages to OpenAI to produce a daily standup format.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Format commits into a readable text list for the prompt
    commit_text = "\n".join(
        [f"- [{c['date']}] {c['message']} (by {c['author']})" for c in commits]
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful software engineering assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content