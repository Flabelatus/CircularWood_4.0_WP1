#!/bin/bash

source ./venv/bin/activate
python convert_yaml_to_dataclass.py
docker-compose up