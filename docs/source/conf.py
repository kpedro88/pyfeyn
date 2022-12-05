# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime
import os
import re
import sys

import toml

from pyfeyn2.render.ascii import ASCIIRender
from pyfeyn2.render.dot import DotRender
from pyfeyn2.render.feynmp import FeynmpRender
from pyfeyn2.render.pyx.pyxrender import PyxRender
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

try:
    info = toml.load("../../pyproject.toml")
except FileNotFoundError:
    info = toml.load("pyproject.toml")
project = info["tool"]["poetry"]["name"]
copyright = str(datetime.datetime.now().year) + ", Alexander Puck Neuwirth"
author = ", ".join(info["tool"]["poetry"]["authors"])
version = re.sub("^", "", os.popen("git describe --tags").read().strip())
rst_epilog = f""".. |project| replace:: {project}\n\n"""


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "nbsphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.napoleon",
    "sphinx_math_dollar",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "jupyter_sphinx",
    "IPython.sphinxext.ipython_console_highlighting",
    "autoapi.extension",
]

napoleon_use_ivar = True
autoapi_type = "python"
autoapi_dirs = ["../../" + project]
autoapi_python_class_content = "both"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
highlight_language = "none"


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

renders = {
    PyxRender: "pyx",
    DotRender: "dot",
    ASCIIRender: "ascii",
    FeynmpRender: "feynmp",
    TikzFeynmanRender: "tikzfeynman",
}
styles = ["arrow-pos", "parallel-arrow-sense", "parallel-arrow-displace"]
types = [
    "boson",
    "fermion",
    "photon",
    "higgs",
    "gluon",
    "ghost",
    "scalar",
    "vector",
    "gluino",
    "squark",
    "slepton",
    "gaugino",
    "neutralino",
    "chargino",
    "higgsino",
    "graviton",
]
attributes = [
    "x",
    "y",
    "bend",
    "label",
    "pdgid",
    "sense",
    "target",
    "source",
    "style",
    "id",
    "type",
]
rst_epilog = (
    rst_epilog
    + """
.. |check| replace:: ✔


.. |uncheck| replace:: ✖


.. |mixed| replace:: ✔/✖

"""
)
for r, n in renders.items():
    for s in styles:
        rst_epilog += (
            f".. |{n}.style.{s}| replace:: "
            + ("|check|" if r.valid_style(s) else "|uncheck|")
            + "\n\n"
        )
    for s in types:
        rst_epilog += (
            f".. |{n}.type.{s}| replace:: "
            + ("|check|" if r.valid_type(s) else "|uncheck|")
            + "\n\n"
        )
    for s in attributes:
        rst_epilog += (
            f".. |{n}.attribute.{s}| replace:: "
            + ("|check|" if r.valid_attribute(s) else "|uncheck|")
            + "\n\n"
        )

import copy

from smpl import doc, io

style_tab = {":ref:`style`": [v for v in renders.values()]}
original = copy.copy(style_tab)
for s in styles:
    arr = []
    for r, n in renders.items():
        arr += [f"|{n}.style.{s}|"]
    style_tab[f":ref:`{s}`"] = arr
    io.write(
        "shared/style/" + s + ".rst",
        doc.array_table({**original, f":ref:`{s}`": arr}, tabs=0, init=True),
    )

types_tab = {":ref:`type`": [v for v in renders.values()]}
for s in types:
    for r, n in renders.items():
        types_tab[f":ref:`{s}`"] = (
            [] if f":ref:`{s}`" not in types_tab else types_tab[f":ref:`{s}`"]
        )
        types_tab[f":ref:`{s}`"] += [f"|{n}.type.{s}|"]

attr_tab = {":ref:`attribute`": [v for v in renders.values()]}
for s in attributes:
    for r, n in renders.items():
        attr_tab[f":ref:`{s}`"] = (
            [] if f":ref:`{s}`" not in attr_tab else attr_tab[f":ref:`{s}`"]
        )
        attr_tab[f":ref:`{s}`"] += [f"|{n}.attribute.{s}|"]


io.write("shared/style_tab.rst", doc.array_table(style_tab, tabs=0, init=True))
io.write("shared/type_tab.rst", doc.array_table(types_tab, tabs=0, init=True))
io.write("shared/attr_tab.rst", doc.array_table(attr_tab, tabs=0, init=True))
