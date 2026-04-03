# GitLab Changelog Generator

A tool to generate a changelog of commits between an environment's current deployment and a git reference on GitLab.

## Installation

```bash
pipx install git+https://github.com/maclav3/gitlab-changelog.git
```

If you don't have `pipx` installed, you can install it using `pip`:
```bash
pip install --user pipx
pipx ensurepath
```

### In local development:

```bash
git clone https://github.com/maclav3/gitlab-changelog.git
cd gitlab-changelog
pip install -e ".[dev]"
```

### Development

Available tasks (requires [Taskfile](https://taskfile.dev/)):
- `task fmt` - Format code
- `task lint` - Lint code
- `task venv` - Create venv manually
- `task install` - Install the package locally

## Usage

### Setup

**GitLab Personal Access Token** - Create a token with `read_api` scope:
1. GitLab → Avatar → Edit profile → Access Tokens → Add new token
2. Select `read_api` scope
3. Copy and save the token

**Project ID** - Find it at: Settings → General (displayed at the top)

### Running

```bash
export GITLAB_TOKEN=<your_token>
export PROJECT_ID=<your_project_id>

# List all environments
gitlab-changelog --list

# Generate changelog for an environment
gitlab-changelog <environment_name> [-from <ref>]
```
