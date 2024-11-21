"""DatabaseHandler summary ...

"""
import sys
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root)

import requests
from collections import namedtuple
from os.path import dirname, abspath
from workflow.production_run import logger, get_production_run_params
from workflow.api_http_client import DataServiceApiClient

logger.getChild("db-handler")

default_params = get_production_run_params()
