# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from os.path import abspath, dirname
from dotenv import load_dotenv
from collections import namedtuple

from settings import logger, app_settings
# load_dotenv()

# # Debug
# LOG_FORMAT_DEBUG = '%(levelname)-8s: %(name)-5s.%(filename)-30s %(message)s'

# # Production
# LOG_FORMAT_PROD = '%(asctime)-15s %(levelname)s:%(name)s: %(message)s'
# LOG_LEVEL_PROD = logging.WARNING


# def is_color_terminal():
#     if os.getenv('TERM') in ('dumb', 'unknown'):
#         return False
#     return sys.stdout.isatty()


# def logging_config_debug():
#     try:
#         import coloredlogs  # pylint: disable=import-outside-toplevel
#     except ImportError:
#         coloredlogs = None

#     log_level = os.environ.get('API_LOG_LEVEL', 'DEBUG')
#     if coloredlogs and is_color_terminal():
#         level_styles = {
#             'spam': {'color': 'green', 'faint': True},
#             'debug': {},
#             'notice': {'color': 'magenta'},
#             'success': {'bold': True, 'color': 'green'},
#             'info': {'bold': True, 'color': 'cyan'},
#             'warning': {'color': 'yellow'},
#             'error': {'color': 'red'},
#             'critical': {'bold': True, 'color': 'red'},
#         }
#         field_styles = {
#             'asctime': {'color': 'green'},
#             'hostname': {'color': 'magenta'},
#             'levelname': {'color': 8},
#             'name': {'color': 8},
#             'programname': {'color': 'cyan'},
#             'username': {'color': 'yellow'},
#         }
#         coloredlogs.install(level=log_level, level_styles=level_styles,
#                             field_styles=field_styles, fmt=LOG_FORMAT_DEBUG)
#     else:
#         logging.basicConfig(level=logging.getLevelName(
#             log_level), format=LOG_FORMAT_DEBUG)


# def logging_config_production():
#     logging.basicConfig(level=LOG_LEVEL_PROD, format=LOG_FORMAT_PROD)


# def configure_logging():
#     env = os.getenv('ENVIRONMENT', 'development')
#     if env == 'production':
#         logging_config_production()
#     else:
#         logging_config_debug()


# configure_logging()
logger = logging.getLogger('wood-api.workflows')


def get_default_params():

    app_directoty = os.path.join(abspath(dirname(dirname(dirname(__file__)))))

    WorkflowParameters = namedtuple(
        'WorkflowParameters',
        field_names=[
            'dir',
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
        static_path=os.path.join(
            app_directoty,
            'static',
            'img'
        ),
        credentials={
            'username': input('Username: '),
            'password': input('Password: ')
        },
        base_url=app_settings.server_configs['environment']['url'],
        idemat=os.path.join(
            app_directoty,
            "idemat",
            "idenmat_2023_wood_simplified.json",
        )
    )

    logger.debug("parameters loaded")
    return default_params
