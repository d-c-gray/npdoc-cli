# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'npdoc-cli'
copyright = '2025, Daniel Cole Gray'
author = 'Daniel Cole Gray'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'numpydoc',
    'autoapi.extension',
    'sphinx_gallery.gen_gallery'
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- SPHINX GALLERY OPTIONS --

sphinx_gallery_conf = {
     'examples_dirs': '../../examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path to where to save gallery generated output
     'within_subsection_order': 'FileNameSortKey'
     }

# -- AUTO API OPTIONS --------
autoapi_dirs = ['../../src/npdoc_cli']
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members']
autoapi_ignore = [
    '*migrations*'
    ]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ['_static']
