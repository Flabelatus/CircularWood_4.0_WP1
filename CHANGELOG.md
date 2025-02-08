# 📘 CHANGELOG

This document monitors the development of the CW4.0 Workflow API. It builds on the foundational processes of the existing Database API, which has now become a core component of this workflow. Moving forward, the Workflow API will also support other processes within the Robot Lab for future projects. As a result, versioning will no longer account for previous work done on the Database API. Instead, it will start fresh, with only new changes and updates being recorded from this point onward.

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

---

## [Unreleased]
### ✨ Added
- [ ] New endpoints to upload `.obj`, `.step` file formats in the project instead of I/O to the database
  
### 🛠️ Changed

- [ ] Refactored MQTT topics names to cover broader and more universal processes in the production run

### 🐛 Fixed
- [ ] WIP
  
### ⚠️ Deprecated

- [ ] The `pointcloud` data model and its resource blueprint routes is **scheduled for deprecation in upcoming release**.
- [ ] The `woods_requirement` data model and its resource blueprint routes is **scheduled for deprecation in upcoming release**.

### 🚫 Removed

- [ ] Cleaned up obsolete methods.

---

## [v1.3.4] - 08-02-2025

### ✨ Added
- [x] The new file uploading helper in the utils
- [x] The 3D MESH and CAD data file handling endpoints
- [x] The Digital Twin workflow init

### 🛠️ Changed
- [x] Refactored the image uploading resources to use the general file upload helpers instead of the old image helpers from the utils

### 🚫 Removed
- [x] The `image_helper.py` from the utils
---

## [v1.3.3] - 13-01-2025

### ✨ Added
- [x] A the database handler to the production run workflow to fetch data for production run `workflow/production_run/database_handler.py`
- [x] Added the finalized MQTT module in production run workflow

### 🛠️ Changed
- [x] Refactored naming of imported modules in `scripts/mqtt_client.py`

---

## [v1.3.2] - 24-12-2024

### ✨ Added
- [x] A Python script `convert_yaml_to_dataclass.py` to generate the typed dataclasses from yaml 
- [x] Script `run.sh` to run the app from CLI for the configs to be generated and added in the application: 
    Running commdands for:
    1. Activating the virtual env 
    2. Executing the `convert_yaml_to_dataclass.py`
    3. Running the docker container via the `docker-compose up` command.

### 🛠️ Changed
- [x] Refactored the schema of the mqtt field `settings.yml` file `development` changed to `development_env` and `production` changed to `production_env`
- [x] Changed the implementation of loading the configs in the global scale using the dot notation instead of using the dictionary key lookups. This help with the VS_Code autocomplete suggesting the attributes within each schema. The main modified files are `settings.py` and `__init__.py` files in each of the sub packages inside the `workflow` package 

---

## [v1.3.1] - 17-12-2024

### ✨ Added
- [x] The MQTT client for the production run workflow
- [x] Utility functions to help generating data classes as types automatically from given `yaml` schema to help with autocomplete dot notation data look up while developing

### 🛠️ Changed
- [x] Refactored the schema of the mqtt field `settings.yml` file 

---

## [v1.3.0] - 16-12-2024

### ✨ Added
- [x] New database tables `design_geometry` and `project` to structure the data of the design metadata in a more clear way and integrate with the live monitorin dashboard better
- [x] New API resource blueprints and endpoints 
`/design_geometries`, 
`/design_geometries<int:design_geometry_id>`
`/project`
`/project/<int:project_id>` 

### 🛠️ Changed
- [x] Updated the schema of the `history` model adding new fields of `name`, `success`, `requirement_id` to the table in order to adjust with the digital twin dashboard schema

- [x] A new directory structure is added for serving design geometry files, including whole models and sub-parts, organized as follows:
    ```
    └───static
        ├───design
        │   └───<design_id>_<project_id>
        │       │   <design_geometry_id>.obj   # The whole model
        │       │   <design_geometry_id>.step  # The whole model
        │       │
        │       └───parts
        │               <requirement_id>_<partname_1>.obj
        │               <requirement_id>_<partname_1>.step
        │               <requirement_id>_<partname_2>.obj
        │               <requirement_id>_<partname_2>.step
        │               ...
        └───img

---

## [v1.2.2] - 16-12-2024

### 🛠️ Fixed
- [x] Added the new added models and apie endpoints to the `sphinx` library congig file for the developer documentation

---

## [v1.2.1] - 16-12-2024

### 🛠️ Changed
- [x] New commit message format added to the CONTRIBUTING.md document

---

## [v1.2.0] - 28-11-2024

### ✨ Added
- [x] New endpoint to set wood as used `/wood/used/<int:wood_id>`

---

## [v1.1.0] - 26-11-2024

### 🛠️ Changed
- [x] Refortored modules of the `/workflow` components to comprehend with the dynamic loading of the settings from the `settings.yml`
- [x] Changes to logging, and API settings 

---
## [v1.0.1] - 24-11-2024

### 🐛 Fixed
- [x] Fixed bugs in the datetime formatting for the background schedueler keeping track of reservations

---

## [v1.0.0] - 07-11-2024
### ✨ Added
- [x] Workflow components such as `api_http_client`, `production_run` to allow the production gateway software manage the workflow of production smoothly
- [x] Centralized `settings.yml` file to allow adjusting the process settings that are dynamic, from one place.
- [x] Scripts to automate the developer docs generation
- [x] Comprehensive logging of the process
- [x] New endpoints for the data models to get the modifiable fields from the model
- [x] Scripts to enable custom updating of the data model based on a specific field
- [x] New script to streamline and simplify the data fetching method for the production instructions using wood ID
- [x] Script for database backup
- [x] New endpoint for image file upload

---
