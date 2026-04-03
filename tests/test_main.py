import pytest
import sys
from unittest.mock import patch
from gitlab_changelog import main


def test_main_no_args(capsys):
    with patch.object(sys, "argv", ["gitlab-changelog"]):
        with patch("gitlab_changelog.main.GITLAB_TOKEN", "token"):
            with patch("gitlab_changelog.main.PROJECT_ID", "123"):
                with pytest.raises(SystemExit):
                    main.main()
    captured = capsys.readouterr()
    assert "the following arguments are required: env" in captured.err


def test_main_list(capsys):
    with patch.object(sys, "argv", ["gitlab-changelog", "--list"]):
        with patch("gitlab_changelog.main.GITLAB_TOKEN", "token"):
            with patch("gitlab_changelog.main.PROJECT_ID", "123"):
                with patch(
                    "gitlab_changelog.gitlab_client.get_environments"
                ) as mock_get_envs:
                    mock_get_envs.return_value = []
                    main.main()
    captured = capsys.readouterr()
    assert "No environments found." in captured.out


def test_main_missing_env_vars(capsys):
    with patch.object(sys, "argv", ["gitlab-changelog", "prod"]):
        with patch.dict("os.environ", {}, clear=True):
            # We need to re-import or re-evaluate the module level variables
            # but since they are already loaded, we might need to mock them in main
            with patch("gitlab_changelog.main.GITLAB_TOKEN", None):
                with patch("gitlab_changelog.main.PROJECT_ID", None):
                    with pytest.raises(SystemExit):
                        main.main()
    captured = capsys.readouterr()
    assert (
        "Error: Set GITLAB_TOKEN and PROJECT_ID environment variables" in captured.out
    )


@patch("gitlab_changelog.gitlab_client.get_default_branch")
@patch("gitlab_changelog.gitlab_client.get_environment_commit")
@patch("gitlab_changelog.gitlab_client.get_commits_between")
@patch("gitlab_changelog.formatter.format_changelog")
def test_main_success(
    mock_format, mock_commits, mock_env_commit, mock_default_branch, capsys
):
    mock_default_branch.return_value = "main"
    mock_env_commit.return_value = "old-sha"
    mock_commits.return_value = []

    with patch.object(sys, "argv", ["gitlab-changelog", "prod"]):
        with patch.dict("os.environ", {"GITLAB_TOKEN": "token", "PROJECT_ID": "123"}):
            with patch("gitlab_changelog.main.GITLAB_TOKEN", "token"):
                with patch("gitlab_changelog.main.PROJECT_ID", "123"):
                    main.main()

    captured = capsys.readouterr()
    assert "Fetching default branch" in captured.out
    assert "Comparing with main" in captured.out
    mock_format.assert_called_once()
