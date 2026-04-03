# GitLab Changelog Generator

A tool to generate a changelog of commits between an environment's current deployment and a git reference on GitLab.

## Installation

The recommended way to install this tool is using [pipx](https://github.com/pypa/pipx):

```bash
pipx install git+https://github.com/maclav3/gitlab-changelog.git
```

If you don't have `pipx` installed, you can install it using `pip`:
```bash
pip install --user pipx
pipx ensurepath
```

Alternatively, you can install it directly from the GitHub repository using `pip`:

```bash
pip install git+https://github.com/maclav3/gitlab-changelog.git
```

Alternatively, for local development:
```bash
git clone https://github.com/maclav3/gitlab-changelog.git
cd gitlab-changelog
pip install -e ".[test,dev]"
```

### Development

This project uses [Taskfile](https://taskfile.dev/) to manage local development tasks. These commands will automatically create a local virtual environment (`.venv`) and install dependencies if they are missing or if `pyproject.toml` changes.

- **Format code**: `task fmt`
- **Lint code**: `task lint`
- **Run tests**: `task test`
- **Create venv manually**: `task venv`

### Versioning

This project uses [Semantic Versioning](https://semver.org/) and is automated via [Python Semantic Release](https://python-semantic-release.readthedocs.io/).

Versions are automatically updated and tagged in CI based on commit messages. This project follows [Conventional Commits](https://www.conventionalcommits.org/).

- **Major** version bump: Commits with `BREAKING CHANGE` or containing `#major` / `break:` prefix.
- **Minor** version bump: Commits with `feat:` or `#minor` / `minor:` prefix.
- **Patch** version bump: Commits with `fix:`, `perf:` or `#patch` / `patch:` prefix.

Manual versioning is no longer required. Just use the appropriate commit prefixes.

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
