import pytest
from unittest.mock import patch, MagicMock
from gitlab_changelog import gitlab_client


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_default_branch(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"default_branch": "master"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    branch = gitlab_client.get_default_branch("project123")

    assert branch == "master"
    mock_get.assert_called_once_with(
        "https://gitlab.com/api/v4/projects/project123", headers={"PRIVATE-TOKEN": None}
    )


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_environments(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"name": "production"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    envs = gitlab_client.get_environments("project123")

    assert envs == [{"name": "production"}]
    mock_get.assert_called_once_with(
        "https://gitlab.com/api/v4/projects/project123/environments",
        headers={"PRIVATE-TOKEN": None},
    )


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_environment_commit_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"sha": "1234567890"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    sha = gitlab_client.get_environment_commit("project123", "production")
    assert sha == "1234567890"
    mock_get.assert_called_once_with(
        "https://gitlab.com/api/v4/projects/project123/deployments",
        headers={"PRIVATE-TOKEN": None},
        params={
            "environment": "production",
            "status": "success",
            "order_by": "created_at",
            "sort": "desc",
            "per_page": 1
        }
    )


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_environment_commit_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Environment 'production' not found or has no successful deployments"):
        gitlab_client.get_environment_commit("project123", "production")


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_commit(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "abc123", "title": "test commit"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    commit = gitlab_client.get_commit("project123", "abc123")

    assert commit == {"id": "abc123", "title": "test commit"}
    mock_get.assert_called_once_with(
        "https://gitlab.com/api/v4/projects/project123/repository/commits/abc123",
        headers={"PRIVATE-TOKEN": None},
    )


@patch("gitlab_changelog.gitlab_client.requests.get")
def test_get_commits_between(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"commits": [{"id": "abc", "title": "test"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    commits = gitlab_client.get_commits_between("project123", "sha1", "sha2")

    assert commits == [{"id": "abc", "title": "test"}]
    mock_get.assert_called_once_with(
        "https://gitlab.com/api/v4/projects/project123/repository/compare",
        headers={"PRIVATE-TOKEN": None},
        params={"from": "sha1", "to": "sha2"},
    )
