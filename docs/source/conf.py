# -*- coding: utf-8 -*-

import os
from datetime import datetime
from importlib.metadata import version as get_version, metadata

package_name = "lindsey_learn_open_source_101"
_meta = metadata(package_name)

package_version = get_version(package_name)

_author_email_raw = _meta.get("Author-email", "")
if _author_email_raw and "<" in _author_email_raw:
    package_author = _author_email_raw.split("<")[0].strip()
else:
    package_author = _meta.get("Author", "Unknown")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx_jinja",
    "sphinx_copybutton",
    "sphinx_design",
    "docfly.directives",
    "nbsphinx",
]

templates_path = ["_templates"]

source_suffix = {
    ".rst": "restructuredtext",
}

master_doc = "index"

project = package_name
copyright = "{}, {}".format(datetime.utcnow().year, package_author)
author = package_author

version = package_version
release = package_version

language = "en"
exclude_patterns = []
pygments_style = "monokai"
todo_include_todos = True

html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": False,
}
pygments_dark_style = "monokai"

html_static_path = ["_static"]
html_css_files = [
    "css/custom-style.css",
]

htmlhelp_basename = "{}doc".format(package_name)

latex_elements = {}
latex_documents = [
    (
        master_doc,
        "{}.tex".format(package_name),
        "{} Documentation".format(package_name),
        author,
        "manual",
    ),
]

man_pages = [
    (master_doc, package_name, "{} Documentation".format(package_name), [author], 1)
]

texinfo_documents = [
    (
        master_doc,
        package_name,
        "{} Documentation".format(package_name),
        author,
        package_name,
        "Lindsey's first open source Python library.",
        "Miscellaneous",
    ),
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"

custom_style_file_path = os.path.join(
    os.path.dirname(__file__), "_static", ".custom-style.rst"
)
with open(custom_style_file_path, "rb") as f:
    custom_style_file_content = f.read().decode("utf-8")
rst_prolog = "\n" + custom_style_file_content + "\n"

jinja_contexts = {
    "doc_data": {
        "doc_data": {},
    },
}

from pathlib import Path
import docfly.api as docfly

docfly.ApiDocGenerator(
    dir_output=Path(__file__).absolute().parent.joinpath("api"),
    package_name=package_name,
    ignore_patterns=[
        f"{package_name}.docs",
        f"{package_name}.tests",
        f"{package_name}.vendor",
        f"{package_name}.paths",
    ],
).fly()
