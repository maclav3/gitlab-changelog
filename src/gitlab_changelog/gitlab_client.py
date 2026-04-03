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
    """Get the latest commit SHA deployed to an environment."""
    envs = get_environments(project_id)
    for env in envs:
        if env["name"] == env_name:
            if env.get("last_deployment"):
                return env["last_deployment"]["sha"]
    raise ValueError(f"Environment '{env_name}' not found or has no deployments")


def get_commits_between(project_id, from_sha, to_ref):
    """Get all commits between from_sha and to_ref."""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/compare"
    params = {"from": from_sha, "to": to_ref}
    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json().get("commits", [])
