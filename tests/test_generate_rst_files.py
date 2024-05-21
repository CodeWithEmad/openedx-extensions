import os
import pytest
import yaml
from collections import defaultdict
from unittest import mock
from generate_rst_files import (
    get_vendor_hyperlink,
    xblock_sort_key,
    title_case,
    get_letter_group,
    write_xblocks_to_rst,
    write_section_rst_file,
    categorize_xblocks,
    generate_rst_files,
)

# Sample data
SAMPLE_XBLOCKS = [
    {
        "name": "SampleXBlock",
        "url": "https://example.com/sample",
        "description": "This is a sample XBlock.",
        "vendor": "SampleVendor",
        "status": "Active",
        "last_commit": "2023-10-01",
        "image": None,
        "youtube": "youtubeVideoID",
        "category": "Course content type",
    }
]

SAMPLE_VENDORS = {"SampleVendor": {"url": "https://example.com"}}


@pytest.fixture
def sample_data_files(tmp_path):
    # Create temporary YAML files
    xblocks_file = tmp_path / "extensions.yml"
    vendors_file = tmp_path / "vendors.yml"

    with open(xblocks_file, "w") as f:
        yaml.dump({"xblocks": SAMPLE_XBLOCKS}, f)

    with open(vendors_file, "w") as f:
        yaml.dump({"vendors": SAMPLE_VENDORS}, f)

    return xblocks_file, vendors_file


def test_get_vendor_hyperlink():
    from generate_rst_files import vendors

    original_vendors = vendors.copy()
    vendors["SampleVendor"] = {"url": "https://example.com"}

    try:
        result = get_vendor_hyperlink("SampleVendor")
        expected = "`SampleVendor <https://example.com>`__"
        assert result == expected
    finally:
        # Restore the original vendors
        vendors.clear()
        vendors.update(original_vendors)


def test_xblock_sort_key():
    xblock = {"name": "SampleXBlock"}
    result = xblock_sort_key(xblock, "name")
    assert result == "samplexblock"


def test_title_case():
    assert title_case("a") == "A"
    assert title_case("1") == "1"


def test_get_letter_group():
    assert get_letter_group("B") == "A, B, C"
    assert get_letter_group("H") == "G, H, I"
    assert get_letter_group("Z") == "Y, Z"
    assert get_letter_group("1") == "Other"


@mock.patch(
    "generate_rst_files.get_vendor_hyperlink",
    return_value="`SampleVendor <https://example.com>`__",
)
def test_write_xblocks_to_rst(mock_get_vendor_hyperlink, tmp_path):
    xblock_file = tmp_path / "xblock.rst"

    with open(xblock_file, "w") as f:
        write_xblocks_to_rst(f, SAMPLE_XBLOCKS)

    with open(xblock_file, "r") as f:
        content = f.read()

    assert "SampleXBlock" in content
    assert "This is a sample XBlock." in content
    assert "SampleVendor" in content


@mock.patch("generate_rst_files.write_xblocks_to_rst")
def test_write_section_rst_file(mock_write_xblocks_to_rst, tmp_path):
    sections = {"Section1": SAMPLE_XBLOCKS}
    directory = tmp_path / "section_dir"
    write_section_rst_file(directory, sections, "Test Title", "Test Description")

    index_file = directory / "index.rst"
    section_file = directory / "Section1.rst"

    assert index_file.exists()
    assert section_file.exists()

    with open(index_file, "r") as f:
        content = f.read()
    assert "Test Title" in content
    assert "Test Description" in content
    assert "Sections:" in content


def test_categorize_xblocks():
    name_dict, category_dict, vendor_dict = categorize_xblocks(SAMPLE_XBLOCKS)

    assert "S, T, U" in name_dict
    assert "Course content type" in category_dict
    assert "SampleVendor" in vendor_dict


# Ensure the defaultdict is imported
@mock.patch(
    "generate_rst_files.categorize_xblocks",
    return_value=(defaultdict(list), defaultdict(list), defaultdict(list)),
)
@mock.patch("generate_rst_files.write_all_rst_file")
@mock.patch("generate_rst_files.write_section_rst_file")
def test_generate_rst_files(
    mock_write_section_rst_file, mock_write_all_rst_file, mock_categorize_xblocks
):
    generate_rst_files(SAMPLE_XBLOCKS)
    assert mock_categorize_xblocks.called
    assert mock_write_section_rst_file.called
    assert mock_write_all_rst_file.called
