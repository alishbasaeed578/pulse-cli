from datetime import datetime, timedelta
import git

def get_recent_commits(repo_path: str = ".", days: int = 1) -> list[dict]:
    """
    Extracts commit messages and details from a local git repository.
    """
    try:
        repo = git.Repo(repo_path)
    except Exception:
        return []

    since_date = datetime.now() - timedelta(days=days)
    commits_data = []

    try:
        for commit in repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            # Stop if commits are older than the requested timeframe
            if commit_date < since_date:
                break

            commits_data.append({
                "hash": commit.hexsha[:7],
                "message": commit.message.strip(),
                "author": commit.author.name,
                "date": commit_date.strftime("%Y-%m-%d %H:%M"),
            })
    except Exception:
        pass

    return commits_data