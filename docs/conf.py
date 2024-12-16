# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import models

excluded_fields = []
# Fetch attribute names for all models
wood_attr_names = dir(models.WoodModel)
production_attr_names = dir(models.ProductionModel)
sub_wood_attr_names = dir(models.SubWoodModel)
design_attr_names = dir(models.DesignRequirementsModelFromClient)
impact_attr_names = dir(models.ImpactModel)
tag_attr_names = dir(models.TagModel)
history_attr_names = dir(models.HistoryModel)
user_attr_names = dir(models.UserModel)
pointcloud_attr_names = dir(models.PointCloudModel)
wood_tags_attr_names = dir(models.WoodTagsModel)
woods_requirements_attr_names = dir(models.WoodsAndRequirementsFromClientModel)
design_geometry_attr_names = dir(models.DesignGeometryModel)
project_attr_names = dir(models.ProjectModel)

# Define a function to exclude certain fields
def exclude_fields(attr_names):
    excl_fields = []
    for attr_name in attr_names:
        if attr_name.startswith("_") or attr_name.endswith("_"):
            continue
        if attr_name == 'metadata':
            continue
        excl_fields.append(attr_name)
    return excl_fields

# Exclude fields for each model
excl_wood_attr = exclude_fields(wood_attr_names)
excl_prod_attr = exclude_fields(production_attr_names)
excl_sub_wood_attr = exclude_fields(sub_wood_attr_names)
excl_design_attr = exclude_fields(design_attr_names)
excl_impact_attr = exclude_fields(impact_attr_names)
excl_tag_attr = exclude_fields(tag_attr_names)
excl_history_attr = exclude_fields(history_attr_names)
excl_user_attr = exclude_fields(user_attr_names)
excl_pointcloud_attr = exclude_fields(pointcloud_attr_names)
excl_wood_tags_attr = exclude_fields(wood_tags_attr_names)
excl_woods_requirements_attr = exclude_fields(woods_requirements_attr_names)
excl_design_geometries_attr = exclude_fields(design_geometry_attr_names)
exlc_project_attr = exclude_fields(project_attr_names)

# Combine all excluded fields
excluded_fields = (
    excl_wood_attr + 
    excl_prod_attr + 
    excl_sub_wood_attr + 
    excl_design_attr + 
    excl_impact_attr + 
    excl_tag_attr + 
    excl_history_attr + 
    excl_user_attr + 
    excl_pointcloud_attr + 
    excl_wood_tags_attr + 
    excl_woods_requirements_attr +
    excl_design_geometries_attr + 
    exlc_project_attr
)

# Optionally, remove duplicates from the combined list
excluded_fields = list(set(excluded_fields))

project = 'CircularWood_4.0 Database API'
copyright = '2024, Javid Jooshesh'
author = 'Javid Jooshesh'
release = '1.3.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'exclude-members': ", ".join(excluded_fields),
    'special-members': '__init__'
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_static_path = ['_static']

# Add this line to include your custom CSS file
html_css_files = [
    'themes.css',
]