# TODO: Implement the process logging and history of production run

# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import re
import logging

from collections import namedtuple
from typing import List, Dict

import requests

from flask_smorest import Blueprint

from resources import wood_blueprint, sub_wood_blp
from resources import production_blp, design_blp
from resources import user_blp, tags_blueprint
from resources.routes import Resources

from settings import logger
from settings import workflow_manager_config_loader as wrkflow_cfg
from settings import data_service_config_loader as ds_api_cfg
from models.interface_model import DataModelInterface

# Logging scope
logger = logging.getLogger('cw4.0-api').getChild('workflows.api-client')

# Global configurations loaded from settings.yml
configs = {
        'data_service': ds_api_cfg,
        'workflow': wrkflow_cfg
    }

# Resource routes
resources = Resources()

# Data models
__models__ = ["wood", "users", "taglist", "production", "requirements", "sub_wood"]

 # List of imported blueprints in respect to the data models
__blueprints__ = [
    wood_blueprint,
    user_blp, 
    tags_blueprint, 
    production_blp, 
    design_blp, 
    sub_wood_blp
]

class ApiBlueprints:
    def __init__(self):
        # Map blueprints to model names
        self.blueprints = {
            __models__[i]: __blueprints__[i] for i, _ in enumerate(__blueprints__)
            }

    def _get_blueprint_routes(self, model_name: str) -> List[str]:
        assert model_name in __models__, f'{model_name} not found in data models'
        
        blueprint = self.blueprints[model_name]
        routes = []

        for func in blueprint.deferred_functions:
            if hasattr(func, '__closure__') and func.__closure__:
                for cell in func.__closure__:
                    # Look for strings that resemble route patterns
                    if isinstance(cell.cell_contents, str) and cell.cell_contents.startswith('/'):
                        routes.append(cell.cell_contents)
        return routes

    def _parse_and_dispatch_routes(self, routes: List[str]) -> Dict[str, Dict[str, List[str]]]:
        route_mapping = {
            'no_params': [],
            'params': {},
            'relations': {}
        }

        # Matches parameters like <int:id> or <name>
        param_pattern = re.compile(r"<(\w+:?\w*)>")
        relation_pattern = re.compile(r"/(\w+)/<\w+:\w+>$")

        for route in routes:
            params = param_pattern.findall(route)
            relation_match = relation_pattern.search(route)

            # Group routes by the parameter
            if not params:
                route_mapping["no_params"].append(route)
            else:
                for param in params:
                    if param not in route_mapping['params']:
                        route_mapping['params'][param] = []
                    route_mapping['params'][param].append(route) 

            # If a relation is found, group it under "relations"   
            if relation_match:
                relation = relation_match.group(1)
                if relation not in route_mapping['relations']:
                    route_mapping['relations'][relation] = []
                route_mapping['relations'][relation].append(route)
        
        return route_mapping
    
    def _dispatch_route_by_criteria(self, model_name: str, criteria='no_params') -> Dict[str, Dict[str, List[str]]]:
        routes = self._get_blueprint_routes(model_name=model_name)
        return self._parse_and_dispatch_routes(routes=routes)[criteria]

    @property
    def wood_routes_no_params(self) -> List[str]:
        return self._dispatch_route_by_criteria('wood')

    @property
    def subwood_routes_no_params(self) -> List[str]:
        return self._dispatch_route_by_criteria('sub_wood')
    
    @property
    def design_routes_no_params(self) -> List[str]:
        return self._dispatch_route_by_criteria('requirements')

    @property
    def production_routes_no_params(self) -> List[str]:
        return self._dispatch_route_by_criteria('production')

    @property
    def taglist_routes_no_params(self) -> List[str]:
        return self._dispatch_route_by_criteria('production')

    @property
    def wood_routes_with_id(self) -> List[str]:
        return self._dispatch_route_by_criteria('wood', 'params').get('int:wood_id')

    @property
    def subwood_routes_with_id(self):
        return self._dispatch_route_by_criteria('sub_wood', 'params').get('int:subwood_id')

    @property
    def design_routes_with_id(self):
        return self._dispatch_route_by_criteria('requirements', 'params').get('int:requirement_id')

    @property
    def production_routes_with_id(self):
        return self._dispatch_route_by_criteria('production', 'params').get('int:production_id')

    @property
    def taglist_routes_with_id(self):
        return self._dispatch_route_by_criteria('taglist', 'params').get('int:tag_id')

    # Back populated models
    @property
    def wood_back_populating_subwood(self):
        return self._dispatch_route_by_criteria('sub_wood', 'relations').get('wood')

    @property
    def design_back_populating_subwood(self):
        return self._dispatch_route_by_criteria('sub_wood', 'relations').get('design')

    @property
    def wood_back_populating_design(self):
        return self._dispatch_route_by_criteria('requirements', 'relations').get('wood')

    @property
    def wood_back_populating_production(self):
        return self._dispatch_route_by_criteria('production', 'relations').get('wood')


class DataServiceApiHTTPClient:
    def __init__(self, configs=configs):
        self.configs = configs
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.api_blueprints = ApiBlueprints()

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

    def fetch_wood_data(self, wood_id=0):
        wood_endpoints = self.api_blueprints.wood_routes_with_id
        for e in wood_endpoints:
            print(e)

    def fetch_subwood_data(self, subwood_id=0):
        subwood_endpoints = self.api_blueprints.subwood_routes_with_id
        for e in subwood_endpoints:
            print(e)

    def fetch_design_data(self, design_id=0):
        design_endpoints = self.api_blueprints.design_routes_with_id
        for e in design_endpoints:
            print(e)

    def fetch_production_data(self, production_id=0):
        prod_endpoints = self.api_blueprints.production_routes_with_id
        for e in prod_endpoints:
            print(e)


a = DataServiceApiHTTPClient().fetch_design_data()
