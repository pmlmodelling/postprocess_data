# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os

sys.path.insert(0, os.path.abspath('../../'))
sys.path.append('../../postprocess_data')


project = 'postprocess_data'
copyright = '2024, Michael Wathen'
author = 'Michael Wathen'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

autodoc_mock_imports = ['xarray']

extensions = ['sphinxcontrib.apidoc',
              'myst_parser',
              'sphinx.ext.napoleon']

# Napoleon settings
napoleon_google_docstring = True


apidoc_output_dir = 'api'
apidoc_module_dir = '../../postprocess_data'
apidoc_extra_args = ['-P']
apidoc_separate_modules = True
apidoc_module_first = True


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
#source_suffix = ['.rst', '.md']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
