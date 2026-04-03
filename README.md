# GitLab Changelog Generator

A tool to generate a changelog of commits between an environment's current deployment and a git reference on GitLab.

## Installation

You can install this tool directly from the GitHub repository:

```bash
pip install https://github.com/maclav3/gitlab-changelog.git
```

Alternatively, for local development:
```bash
git clone https://github.com/maclav3/gitlab-changelog.git
cd gitlab-changelog
pip install -e .
```

## Usage

Set the required environment variables:
```bash
export GITLAB_TOKEN=<your_token>
export PROJECT_ID=<your_project_id>
```

Run the tool:
```bash
gitlab-changelog <environment_name> [-from <ref>]
gitlab-changelog --list
```
