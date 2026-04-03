from gitlab_changelog import formatter


def test_list_environments_empty(capsys):
    formatter.list_environments([])
    captured = capsys.readouterr()
    assert "No environments found." in captured.out


def test_list_environments_success(capsys):
    envs = [{"name": "production", "last_deployment": {"sha": "1234567890"}}]
    formatter.list_environments(envs)
    captured = capsys.readouterr()
    assert "Available Environments" in captured.out
    assert "production" in captured.out
    assert "12345678" in captured.out


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
