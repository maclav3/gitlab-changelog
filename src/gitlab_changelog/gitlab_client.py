import os
import requests

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


def get_headers():
    return {"PRIVATE-TOKEN": GITLAB_TOKEN}


def get_default_branch(project_id):
    """Get the default branch of the project."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json().get("default_branch", "main")


def get_environments(project_id):
    """List all available environments for the project."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/environments"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def get_environment_commit(project_id, env_name):
    """Get the latest successfully deployed commit SHA for an environment."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/deployments"
    params = {
        "environment": env_name,
        "status": "success",
        "order_by": "created_at",
        "sort": "desc",
        "per_page": 1
    }
    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    deployments = response.json()

    if not deployments:
        raise ValueError(f"Environment '{env_name}' not found or has no successful deployments")

    return deployments[0]["sha"]


def get_commit(project_id, sha):
    """Get commit details by SHA."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/commits/{sha}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def get_commits_between(project_id, from_sha, to_ref):
    """Get all commits between from_sha and to_ref."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/compare"
    params = {"from": from_sha, "to": to_ref}
    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json().get("commits", [])
