import os
import sys
from datetime import datetime

# Add the scripts directory to the sys.path
sys.path.insert(0, os.path.abspath("../../scripts"))

# -- Project information -----------------------------------------------------

# project = "OpenedX Extensions"
author = "Emad Rad"
current_year = datetime.utcnow().year
copyright = f"{current_year}, Emad Rad"
release = "1.0.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinxcontrib.images",
    "sphinxcontrib.youtube",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"
html_title = "OpenedX Extensions"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static", "_images"]
html_css_files = ["css/custom.css"]
html_sidebars = {}
# For custom styles
html_theme_options = {
    "repository_url": "https://github.com/codewithemad/openedx-extensions",
    "repository_branch": "main",
    "path_to_docs": "source",
    "primary_sidebar_end": "primary_sidebar_end",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "navigation_with_keys": False,
}

# Enable some more features
autodoc_default_options = {
    "members": True,
    "private-members": True,
    "special-members": True,
    "inherited-members": True,
    "show-inheritance": True,
}
