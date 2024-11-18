# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from os.path import abspath, dirname
from dotenv import load_dotenv
from collections import namedtuple

from settings import logger
from settings import workflow_manager_config_loader as wrkflow_cfg
from settings import data_service_config_loader as ds_api_cfg

logger = logging.getLogger('cw4.0-api').getChild('workflows.api-client')


def get_default_params():

    app_directoty = os.path.join(abspath(dirname(dirname(dirname(__file__)))))
    base_url = ds_api_cfg.backend_env['url']
    
    WorkflowParameters = namedtuple(
        'WorkflowParameters',
        field_names=[
            'dir',
            'root_dir',
            'static_path',
            'credentials',
            'base_url',
            'idemat'
        ]
    )

    default_params = WorkflowParameters(
        dir=[
            "wood_intake",
            "depth_png",
            "metal_region"
        ],
        root_dir=app_directoty,
        static_path=os.path.join(
            app_directoty,
            'static',
            'img'
        ),
        credentials={
            'username': wrkflow_cfg.http_network_configs['credentials']['username'],
            'password': wrkflow_cfg.http_network_configs['credentials']['password']
        },
        base_url=base_url,
        idemat=os.path.join(app_directoty, ds_api_cfg.external['tools']['idemat']['path'])
    )

    logger.debug("parameters loaded")
    return default_params
