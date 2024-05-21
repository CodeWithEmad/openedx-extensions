import os
import requests
import yaml
from collections import defaultdict

# Load XBlock data from YAML file
with open("extensions.yml", "r") as file:
    data = yaml.safe_load(file)

# Load Vendor data from YAML file
with open("vendors.yml", "r") as file:
    vendors_data = yaml.safe_load(file)

xblocks = data["xblocks"]
vendors = vendors_data["vendors"]


def get_vendor_hyperlink(name):
    """
    Generate a RST hyperlink for the vendor given its name.

    Args:
        name (str): The name of the vendor.

    Returns:
        str: The RST hyperlink as a string.
    """
    vendor_info = vendors.get(name, {})
    vendor_url = vendor_info.get("url", "#")
    return f"`{name} <{vendor_url}>`__"


def xblock_sort_key(xblock, key):
    """
    Helper function to generate a sorting key for an XBlock dictionary.

    Args:
        xblock (dict): The XBlock dictionary.
        key (str): The key to use for sorting.

    Returns:
        str: The value corresponding to the key in lower case.
    """
    return xblock.get(key, "").lower()


def title_case(c):
    """
    Convert a character to title case (uppercase if it is a letter).

    Args:
        c (str): The character to convert.

    Returns:
        str: The title-cased character.
    """
    if c.isalpha():
        return c.upper()
    return c


def get_letter_group(letter):
    """
    Map a letter to its alphabetical group for categorization.

    Args:
        letter (str): The letter to categorize.

    Returns:
        str: The alphabetical group of the letter.
    """
    letter = letter.upper()
    if "A" <= letter <= "C":
        return "A, B, C"
    elif "D" <= letter <= "F":
        return "D, E, F"
    elif "G" <= letter <= "I":
        return "G, H, I"
    elif "J" <= letter <= "L":
        return "J, K, L"
    elif "M" <= letter <= "O":
        return "M, N, O"
    elif "P" <= letter <= "R":
        return "P, Q, R"
    elif "S" <= letter <= "U":
        return "S, T, U"
    elif "V" <= letter <= "X":
        return "V, W, X"
    elif "Y" <= letter <= "Z":
        return "Y, Z"
    return "Other"


def write_xblocks_to_rst(file, xblocks):
    """
    Write a list of XBlocks to an RST file.

    Args:
        file: The file object to write to.
        xblocks (list): The list of XBlock dictionaries.
    """
    for xblock in xblocks:
        title = f"`{xblock['name']} <{xblock['url']}>`__"
        image = (
            "placeholder.webp"
            if xblock.get("image") is None
            else os.path.basename(xblock["image"])
        )
        underline = "*" * len(title)
        vendor_hyperlink = get_vendor_hyperlink(xblock["vendor"])
        file.write(f"{title}\n{underline}\n\n")
        file.write(f"{xblock['description']}\n\n")
        if not xblock.get("image") and xblock.get("youtube"):
            file.write(f".. youtube:: {xblock.get('youtube')}\n")
            file.write(f"    :align: center\n\n")
            file.write(f"    :width: 100%\n\n")
        else:
            file.write(f".. image:: /_images/{image}\n")
            file.write(f"    :alt: {xblock['name']}\n")
            file.write(f"    :align: center\n\n")
        file.write(f"**Vendor:** {vendor_hyperlink}\n\n")
        file.write(f"**Status:** {xblock['status']}\n\n")
        file.write(f"**Last Commit:** {xblock['last_commit']}\n\n")
        file.write(f"**URL:** {xblock['url']}\n\n")
        if xblock.get("license"):  # Some repos don't have a license
            file.write(f"**License:** {xblock['license']}\n\n")
        file.write(f"**Categories:** {xblock['category']}\n\n")


def write_section_rst_file(directory, sections, title, description=None):
    """
    Write RST files for different sections with the categorized XBlocks.

    Args:
        directory (str): The directory where RST files will be created.
        sections (dict): The categorized sections with lists of XBlocks.
        title (str): The title of the index file.
        description (str, optional): The description for the index file. Defaults to None.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    index_file = os.path.join(directory, "index.rst")

    with open(index_file, "w") as f:
        f.write(f"{title}\n")
        f.write("=" * len(title) + "\n\n")
        if description:
            f.write(f"{description}\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 1\n")
        f.write("   :caption: Sections:\n\n")

        for section, xblocks in sections.items():
            section_filename = os.path.join(directory, f"{section}.rst")
            with open(section_filename, "w") as section_file:
                section_file.write(f"{section}\n")
                section_file.write("=" * len(section) + "\n\n")
                write_xblocks_to_rst(section_file, xblocks)
            f.write(f"   {section} <{section}>\n")


# New function to generate a single RST file for all XBlocks
def write_all_rst_file(directory, xblocks, title, description=None):
    """
    Write an RST file for all XBlocks without sections.

    Args:
        directory (str): The directory where the RST file will be created.
        xblocks (list): The list of all XBlock dictionaries.
        title (str): The title of the RST file.
        description (str, optional): The description for the RST file. Defaults to None.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, "index.rst")

    with open(file_path, "w") as f:
        f.write(f"{title}\n")
        f.write("=" * len(title) + "\n\n")
        if description:
            f.write(f"{description}\n\n")

        write_xblocks_to_rst(f, xblocks)


def categorize_xblocks(xblocks):
    """
    Categorize XBlocks by name, category, and vendor.

    Args:
        xblocks (list): The list of XBlock dictionaries.

    Returns:
        tuple: Three dictionaries categorized by name, category, and vendor.
    """
    xblocks_by_name = defaultdict(list)
    xblocks_by_category = defaultdict(list)
    xblocks_by_vendor = defaultdict(list)

    for xblock in xblocks:
        # Categorize by first letter of name
        first_letter = get_letter_group(xblock["name"][0].upper())
        xblocks_by_name[first_letter].append(xblock)

        # Categorize by category
        xblocks_by_category[xblock["category"]].append(xblock)

        # Categorize by vendor
        xblocks_by_vendor[xblock["vendor"]].append(xblock)

    return xblocks_by_name, xblocks_by_category, xblocks_by_vendor


def generate_rst_files(xblocks):
    """
    Generate RST files for XBlocks categorized by name, category, and vendor.

    Args:
        xblocks (list): The list of XBlock dictionaries.
    """
    by_name, by_category, by_vendor = categorize_xblocks(xblocks)

    # Sort individual sections
    for section in by_name.values():
        section.sort(key=lambda x: xblock_sort_key(x, "name"))

    # Write sectioned RST files
    write_section_rst_file("docs/source/name", by_name, "By Name")
    write_section_rst_file("docs/source/category", by_category, "By Category")
    write_section_rst_file("docs/source/vendor", by_vendor, "By Vendor")

    # Write all Extensions in a single RST file
    write_all_rst_file("docs/source/all", xblocks, "All")


if __name__ == "__main__":
    generate_rst_files(xblocks)
