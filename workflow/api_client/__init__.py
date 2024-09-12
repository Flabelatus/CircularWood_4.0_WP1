# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from os.path import abspath, dirname
from dotenv import load_dotenv
from collections import namedtuple

from settings import logger, app_settings


logger = logging.getLogger('wood-api.workflows')


def get_default_params():

    app_directoty = os.path.join(abspath(dirname(dirname(dirname(__file__)))))
    base_url = app_settings.backend_env
    
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
            *app_settings.api_configs['upload_image_destination']
        ),
        credentials={
            'username': input('Username: '),
            'password': input('Password: ')
        },
        base_url=base_url,
        idemat=os.path.join(app_directoty, app_settings.external['tools']['idemat']['path'])
    )

    logger.debug("parameters loaded")
    return default_params
