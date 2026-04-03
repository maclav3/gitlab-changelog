import os
from datetime import datetime

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")


def list_environments(envs, project_id=None):
    """List all available environments for the project."""
    if not envs:
        print("No environments found.")
        return

    from . import gitlab_client

    print("\n🌍 Available Environments:")
    print("=" * 80)
    for env in envs:
        name = env["name"]
        if project_id:
            try:
                sha = gitlab_client.get_environment_commit(project_id, name)
                commit = gitlab_client.get_commit(project_id, sha)
                short_sha = sha[:8]
                title = commit.get("title", "")
                print(f"• {name:20} {short_sha}  {title}")
            except ValueError:
                print(f"• {name:20} No deployment")
        else:
            print(f"• {name:20} Unknown")
    print()


def format_changelog(commits, project_id):
    """Format commits into a readable changelog."""
    if not commits:
        print(
            "✅ No commits awaiting deployment - environment is up to date with main!"
        )
        return

    print(f"\n📋 Changelog: {len(commits)} commit(s) awaiting deployment\n")
    print("=" * 80)

    for commit in reversed(commits):  # Show oldest first
        sha = commit["id"][:8]
        title = commit["title"]
        author = commit["author_name"]
        date = datetime.fromisoformat(commit["created_at"].replace("Z", "+00:00"))
        formatted_date = date.strftime("%Y-%m-%d %H:%M")

        commit_url = f"{GITLAB_URL}/{project_id}/-/commit/{commit['id']}"

        print(f"• [{sha}]({commit_url}) {title}")
        print(f"  👤 {author} | 📅 {formatted_date}\n")
