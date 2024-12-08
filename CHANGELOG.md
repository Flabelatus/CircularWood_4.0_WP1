# 📘 CHANGELOG

This document monitors the development of the CW4.0 Workflow API. It builds on the foundational processes of the existing Database API, which has now become a core component of this workflow. Moving forward, the Workflow API will also support other processes within the Robot Lab for future projects. As a result, versioning will no longer account for previous work done on the Database API. Instead, it will start fresh, with only new changes and updates being recorded from this point onward.

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

---

## [Unreleased]
### ✨ Added
- [ ] New database tables `design_geometry` and `project` to structure the data of the design metadata in a more clear way and integrate with the live monitorin dashboard better
- [ ] New API resource blueprints and endpoints 
`/design_geometries`, 
`/design_geometries<int:design_geometry_id>`
`/project`
`/project/<int:project_id>` 
- [ ] New endpoints to upload `.obj`, `.step` file formats in the project instead of I/O to the database
  
### 🛠️ Changed
- [ ] The requirements table schema has been updated: The features field is now part_file_path, which stores the file path of the `.step` file instead of its content as a string.

- [ ] A new directory structure is added for serving design geometry files, including whole models and sub-parts, organized as follows:
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
    ```
- [ ] Refactored MQTT topics names to cover broader and more universal processes in the production run
- [ ] Production process logs table and resource blueprints to add new logs from the production processes

### 🐛 Fixed
- [ ] WIP
  
### ⚠️ Deprecated

- [ ] The `pointcloud` data model and its resource blueprint routes is **scheduled for deprecation in upcoming release**.
- [ ] The `woods_requirement` data model and its resource blueprint routes is **scheduled for deprecation in upcoming release**.

### 🚫 Removed

- [ ] Cleaned up obsolete methods.

---

## [v1.2.0] - 28-12-2024

### ✨ Added
- [x] New endpoint to set wood as used `/wood/used/<int:wood_id>`

---

## [v1.1.0] - 26-12-2024

### 🛠️ Changed
- [x] Refortored modules of the `/workflow` components to comprehend with the dynamic loading of the settings from the `settings.yml`
- [x] Changes to logging, and API settings 

---
## [v1.0.1] - 24-12-2024

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