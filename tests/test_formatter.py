from unittest.mock import patch
from gitlab_changelog import formatter


def test_list_environments_empty(capsys):
    formatter.list_environments([])
    captured = capsys.readouterr()
    assert "No environments found." in captured.out


def test_list_environments_without_project_id(capsys):
    envs = [{"name": "production"}]
    formatter.list_environments(envs)
    captured = capsys.readouterr()
    assert "Available Environments" in captured.out
    assert "production" in captured.out
    assert "Unknown" in captured.out


@patch("gitlab_changelog.gitlab_client.get_commit")
@patch("gitlab_changelog.gitlab_client.get_environment_commit")
def test_list_environments_success(mock_get_env_commit, mock_get_commit, capsys):
    mock_get_env_commit.return_value = "1234567890abcdef"
    mock_get_commit.return_value = {"title": "Test commit"}

    envs = [{"name": "production"}]
    formatter.list_environments(envs, "project123")
    captured = capsys.readouterr()
    assert "Available Environments" in captured.out
    assert "production" in captured.out
    assert "12345678" in captured.out
    assert "Test commit" in captured.out


def test_format_changelog_empty(capsys):
    formatter.format_changelog([], "project123")
    captured = capsys.readouterr()
    assert "No commits awaiting deployment" in captured.out


def test_format_changelog_success(capsys):
    commits = [
        {
            "id": "abc123456789",
            "title": "Feature A",
            "author_name": "Author A",
            "created_at": "2023-01-01T12:00:00Z",
        }
    ]
    formatter.format_changelog(commits, "project123")
    captured = capsys.readouterr()
    assert "Changelog" in captured.out
    assert "Feature A" in captured.out
    assert "abc12345" in captured.out
    assert "Author A" in captured.out
    assert "2023-01-01 12:00" in captured.out
