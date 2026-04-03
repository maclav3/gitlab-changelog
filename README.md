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
pip install -e .
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/). To update the version:

1. Update the `version` field in `pyproject.toml`.
2. Commit the change.
3. Tag the commit:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```
4. Push the tag:
   ```bash
   git push origin vX.Y.Z
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
