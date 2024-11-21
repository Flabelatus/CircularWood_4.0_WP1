# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from os.path import abspath, dirname
from collections import namedtuple

import requests

from settings import logger
from settings import workflow_manager_config_loader as wrkflow_cfg
from settings import data_service_config_loader as ds_api_cfg

logger = logging.getLogger('cw4.0-api').getChild('workflows.api-client')
configs = {
        'data_service': ds_api_cfg,
        'workflow': wrkflow_cfg
    }


class DataServiceApiHTTPClient:
    def __init__(self, configs=configs):
        self.configs = configs
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def _get_api_client_configs(self):
        base_url = self.configs.get('data_service').backend_env['url']
        ApiClientParameters = namedtuple(
            'ApiClientParameters',
            field_names=[
                'dir',
                'root_dir',
                'static_path',
                'credentials',
                'base_url',
                'idemat'
            ]
        )
        params = ApiClientParameters(
            dir=[
                "wood_intake",
                "depth_png",
                "metal_region"
            ],
            root_dir=self.root,
            static_path=os.path.join(
                self.root,
                'static',
                'img'
            ),
            credentials={
                'username': self.configs.get('workflow').http_network_configs['credentials']['username'],
                'password': self.configs.get('workflow').http_network_configs['credentials']['password']
            },
            base_url=base_url,
            idemat=os.path.join(self.root, self.configs.get('data_service').external['tools']['idemat']['path'])
        )
        logger.debug("data service api parameters loaded")
        return params

    @property
    def params(self):
        return self._get_api_client_configs()

    def authenticate(self):
        username = self.params.credentials['username']
        password = self.params.credentials['password']
        auth_endpoint = f"{self.params.base_url}/login"
        payload = {
            "username": username,
            "password": password
        }
        access_token = ""
        response = requests.post(url=auth_endpoint, json=payload)

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            return access_token
        else:
            logger.error(response.json())

    def fetch_wood_data(self, wood_id):
        ...

    def fetch_subwood_data(self, subwood_id):
        ...

    def fetch_design_data(self, design_id):
        ...

    def fetch_production_data(self, production_id):
        ...
