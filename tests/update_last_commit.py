import yaml
import pytest
import requests
from unittest import mock
from update_last_commit import get_repo_info, update_extensions


SAMPLE_XBLOCKS_YAML = """
xblocks:
  - name: SampleXBlock
    url: https://github.com/example/sample-xblock
    description: This is a sample XBlock.
    vendor: SampleVendor
    status: Active
    last_commit: 2022-05-01
"""

SAMPLE_REPO_INFO = {
    "status": "Active",
    "last_commit": "2023-10-01",
}


@pytest.fixture
def sample_xblocks(tmp_path):
    file_path = tmp_path / "extensions.yml"
    with open(file_path, "w") as f:
        f.write(SAMPLE_XBLOCKS_YAML)
    return file_path


@mock.patch("requests.get")
def test_get_repo_info(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "archived": False,
        "pushed_at": "2023-10-01T12:00:00Z",
    }

    result = get_repo_info("https://github.com/example/sample-xblock")
    assert result == SAMPLE_REPO_INFO


@mock.patch("update_last_commit.get_repo_info", return_value=SAMPLE_REPO_INFO)
def test_update_xblocks(mock_get_repo_info, sample_xblocks):
    update_extensions(sample_xblocks)

    with open(sample_xblocks, "r") as f:
        updated_data = yaml.safe_load(f)

    assert updated_data["xblocks"][0]["status"] == "Active"
    assert updated_data["xblocks"][0]["last_commit"] == "2023-10-01"
