# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from pathlib import Path

from sphinx.ext import apidoc
import sphinx_rtd_theme  # noqa: theme for build

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
config_framework_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(config_framework_path))
sys.path.insert(1, str(Path(__file__).parent))

import config_framework  # noqa: getting version of module

# -- Project information -----------------------------------------------------

project = 'ConfigFramework'
copyright = '2021, Rud356'
author = 'Rud356'

# The full version, including alpha/beta/rc tags
release = config_framework.__version__

# -- General configuration ---------------------------------------------------

master_doc = 'index'
source_suffix = '.rst'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', '**tests**', '**setup**']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
autodoc_member_order = 'bysource'

html_static_path = ['_static']
apidoc_module_dir = "./../"
apidoc_output_dir = './source/'
apidoc_separate_modules = True
apidoc_excluded_paths = ['tests', 'setup.py']
autodoc_default_flags = ['members']
autoclass_content = 'both'
autosummary_generate = True
add_module_names = False
class_members_toctree = False
html_show_sourcelink = False


def setup(app):
    config_framework_dir = '../config_framework'
    if not on_rtd:
        apidoc.main([
            '-f', '-Var', '-E', '-M',
            '-o', './source/',
            config_framework_dir,
        ])
