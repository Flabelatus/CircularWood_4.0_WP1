# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from os.path import abspath, dirname
from dotenv import load_dotenv
from collections import namedtuple

from settings import logger, ds_api_configs


logger = logging.getLogger('wood-api.workflows.prod-gateway')
