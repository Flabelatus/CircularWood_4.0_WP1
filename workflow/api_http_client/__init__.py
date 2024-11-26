# TODO: Implement the process logging and history of production run

# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import re
import logging

from collections import namedtuple
from typing import List, Dict

from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import inspect

from resources import wood_blueprint, sub_wood_blp
from resources import production_blp, design_blp
from resources import user_blp, tags_blueprint
from resources.routes import Resources

from settings import workflow_manager_config_loader as wrkflow_cfg
from settings import data_service_config_loader as ds_api_cfg

from schema import WoodSchema, SubWoodSchema
from schema import ProductionSchema, UserSchema
from schema import DesignRequirementSchema, TagSchema

# Logging scope
logger = logging.getLogger('cw4.0-api').getChild('workflows.api-client')

# Global configurations loaded from settings.yml
__configs__ = {
        'data_service': ds_api_cfg,
        'workflow': wrkflow_cfg
    }

# Resource routes
__resources__ = Resources()

 # Dict of data model names and imported blueprints as `Dict[name: blueprint]`
__api__ = {
    "wood": {"blueprint": wood_blueprint, "schema": WoodSchema},
    "users": {"blueprint": user_blp, "schema": UserSchema},
    "taglist": {"blueprint": tags_blueprint, "schema": TagSchema},
    "production": {"blueprint": production_blp, "schema": ProductionSchema},
    "requirements": {"blueprint": design_blp, "schema": DesignRequirementSchema},
    "sub_wood": {"blueprint": sub_wood_blp, "schema": SubWoodSchema}
}


class ApiBlueprints:
    def __init__(self):
        # Map blueprints to model names
        self.blueprints = __api__
        
        # Matches parameters like <int:id> or <name>
        self.url_params_mask_pattern = re.compile(r"<(\w+:?\w*)>")
        # Matches names in between the endpoint segments to find the relation fields
        self.relation_mask_pattern = re.compile(r"/(\w+)/<\w+:\w+>$")

        self.route_mapping = {
            'no_params': [],
            'params': {},
            'relations': {}
        }

    def _get_blueprint_routes(self, model_name: str) -> List[str]:
        assert model_name in __api__, f'{model_name} not found in data models'
        
        blueprint = self.blueprints[model_name].get('blueprint')

        routes = []
        for func in blueprint.deferred_functions:
            if hasattr(func, '__closure__') and func.__closure__:
                for cell in func.__closure__:
                    # Look for strings that resemble route patterns
                    if isinstance(cell.cell_contents, str) and cell.cell_contents.startswith('/'):
                        routes.append(cell.cell_contents)
        return routes

    def _parse_and_dispatch_routes(self, routes: List[str]) -> Dict[str, Dict[str, List[str]]]:

        for route in routes:
            params = self.url_params_mask_pattern.findall(route)
            relation_match = self.relation_mask_pattern.search(route)

            # Group routes by the parameter
            if not params:
                self.route_mapping["no_params"].append(route)
            else:
                for param in params:
                    if param not in self.route_mapping['params']:
                        self.route_mapping['params'][param] = []
                    self.route_mapping['params'][param].append(route) 

            # If a relation is found, group it under "relations"   
            if relation_match:
                relation = relation_match.group(1)
                if relation not in self.route_mapping['relations']:
                    self.route_mapping['relations'][relation] = []
                self.route_mapping['relations'][relation].append(route)
        
        return self.route_mapping
    
    def _dispatch_route_by_criteria(self, model_name: str, criteria='no_params') -> Dict[str, Dict[str, List[str]]]:
        routes = self._get_blueprint_routes(model_name=model_name)
        return self._parse_and_dispatch_routes(routes=routes)[criteria]
    
    def _get_min_route(self, routes: List[str]):
        min_arr_len_route = min(routes, key=lambda route: len(route.split("/")))
        return min_arr_len_route

    def _strip_route(self, route: str):
        if not route:
            return ""
        segments = route.split("/")
        stripped_segments = [self.url_params_mask_pattern.sub("", segment) for segment in segments]
        stripped_route = f'/{"/".join(filter(None, stripped_segments))}/'
        return stripped_route

    def _get_flattened_routes_by_criteria(self, key: str, criteria: str):
        routes_from_blp = self._dispatch_route_by_criteria(key, criteria)
        # Flatten all routes from the dictionary
        routes = [route for routes_by_pattern in routes_from_blp.values() for route in routes_by_pattern]
        return self._strip_route(self._get_min_route(routes))

    @property
    def wood_route(self) -> str:
        """`/wood` Endpoint to get the list of wood data, or post a new wood record to the list"""
        key, criteria = 'wood', 'no_params'
        routes = self._dispatch_route_by_criteria(model_name=key, criteria=criteria)
        return self._get_min_route(routes)
    
    @property
    def subwood_route(self) -> str:
        """`/sub_wood` Endpoint to get the list of sub wood data, or post a new sub wood record to the list"""
        key, criteria = 'sub_wood', 'no_params'
        routes = self._dispatch_route_by_criteria(model_name=key, criteria=criteria)
        return self._get_min_route(routes)
    
    @property
    def design_route(self) -> str:
        """`/design/client` Endpoint to get the list of design data, or post a new design record to the list"""
        key, criteria = 'requirements', 'no_params'
        routes = self._dispatch_route_by_criteria(model_name=key, criteria=criteria)
        return self._get_min_route(routes)

    @property
    def production_route(self) -> str:
        """`/production` Endpoint to get the list of production data, or post a new production record to the list"""
        key, criteria = 'production', 'no_params'
        routes = self._dispatch_route_by_criteria(model_name=key, criteria=criteria)
        return self._get_min_route(routes)

    @property
    def taglist_route(self) -> str:
        """`/tags` Endpoint to get the list of tags data, or post a new tag record to the list"""
        key, criteria = 'taglist', 'no_params'
        routes = self._dispatch_route_by_criteria(model_name=key, criteria=criteria)
        return self._get_min_route(routes)

    @property
    def wood_by_id_route(self) -> str:
        """`/wood/<int:wood_id>` Endpoint to get, update or delete the wood data by ID"""
        key, criteria = 'wood', 'params'
        return self._get_flattened_routes_by_criteria(key=key, criteria=criteria)
    
    @property
    def wood_reserve_route(self) -> str:
        key = 'reserve'
        return f"{self.wood_by_id_route}{key}/"

    @property
    def wood_unreserve_route(self) -> str:
        key = 'unreserve'
        return f"{self.wood_by_id_route}{key}/"

    @property
    def wood_set_used_route(self) -> str:
        key = 'used'
        return f"{self.wood_by_id_route}{key}/"

    @property
    def subwood_by_id_route(self) -> str:
        """`/sub_wood/<int:subwood_id>` Endpoint to get, update or delete the sub wood data by ID"""
        key, criteria = 'sub_wood', 'params'
        return self._get_flattened_routes_by_criteria(key=key, criteria=criteria)

    @property
    def design_by_id_route(self) -> str:
        """`/design/client/<int:design_id>` Endpoint to get, update or delete the design data by ID"""
        key, criteria = 'requirements', 'params'
        return self._get_flattened_routes_by_criteria(key=key, criteria=criteria)

    @property
    def production_by_id_route(self) -> str:
        """`/production/<int:production_id>` Endpoint to get, update or delete the production data by ID"""
        key, criteria = 'production', 'params'
        return self._get_flattened_routes_by_criteria(key=key, criteria=criteria)

    @property
    def tag_by_id_route(self) -> str:
        """`/tag/<int:tag_id>` Endpoint to get, update or delete the tag data by ID"""
        key, criteria = 'taglist', 'params'
        return self._get_flattened_routes_by_criteria(key=key, criteria=criteria)

    # Back populated models
    @property
    def subwood_by_wood_id_route(self):
        """
        `/subwood/wood/<int:wood_id>` Endpoint to get sub wood data linked to wood by wood ID
            
            :Important: 'Sub wood data model and its registered blueprint in the API have naming inconsistency'. 

                Sub wood tablename is `sub_wood`, while the endpoint route name referenced to it `subwood`
        """
        
        key, criteria, relation = 'sub_wood', 'relations', 'wood'
        route = self._dispatch_route_by_criteria(model_name=key, criteria=criteria).get(relation)
        
        # Resolving the Inconsistency
        key = key.replace("_", "")
        return self._strip_route(*[end_pt for end_pt in route if key in end_pt])

    @property
    def subwood_by_design_id_route(self):
        """
        `/subwood/design/<int:design_id>` Endpoint to get sub wood data linked to design part by design ID
            
            :Important: 'Sub wood data model and its registered blueprint in the API have naming inconsistency'. 

                Sub wood tablename is `sub_wood`, while the endpoint route name referenced to it `subwood`
        """
        
        key, criteria, relation = 'sub_wood', 'relations', 'design'
        route = self._dispatch_route_by_criteria(model_name=key, criteria=criteria).get(relation)
        
        # Resolving the Inconsistency
        key = key.replace("_", "")
        return self._strip_route(*[end_pt for end_pt in route if key in end_pt])
    
    @property
    def design_by_wood_id_route(self):
        """
        `/design/wood/<int:wood_id>` Endpoint to get design part data linked to wood by wood ID\n
            
            :Important: 'Design data model and its registered blueprint in the API have naming inconsistency'. 

                Design data in the database is stored in the `requirements` table, while the endpoint 
                name referenced to it within the api routes is `design`
                
                - Database tablename used as key `design_keys['tablename']` to extract the routes from the
                design blueprint.
                
                - Endpoint name used as key `design_keys['endpoint']` to filter the desired route
        """

        design_keys = {
            'tablename': 'requirements',
            'endpoint': 'design'
        }

        # Database tablename used as key `design_keys['tablename']` to extract the routes from the design blueprint
        key, criteria, relation = design_keys['tablename'], 'relations', 'wood'
        route = self._dispatch_route_by_criteria(model_name=key, criteria=criteria).get(relation)
        
        # Endpoint name used as key `design_keys['endpoint']` to filter the desired route
        key = design_keys['endpoint']
        return self._strip_route(*[end_pt for end_pt in route if key in end_pt])

    @property
    def production_by_wood_id_route(self):
        """`/production/wood/<int:wood_id>` Endpoint to get production data linked to wood by wood ID"""
        key, criteria, relation = 'production', 'relations', 'wood'
        route = self._dispatch_route_by_criteria(model_name=key, criteria=criteria).get(relation)
        return self._strip_route(*[end_pt for end_pt in route if key in end_pt])


class HttpClientCore:
    def __init__(self, configs=__configs__):
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
        return params

    @property
    def params(self):
        return self._get_api_client_configs()


def get_modifiable_fields(model):
    """
    Identifies modifiable fields in a SQLAlchemy model that are not part of specified
    relationships or partial fields.
    """
    model_instance = model()
    mapper = inspect(model)

    all_columns = [
        prop.key for prop in mapper.attrs if not isinstance(prop, RelationshipProperty)
    ]

    # Assume relationship_fields and wood_partials are either methods or properties
    if callable(getattr(model_instance, "relationship_fields", None)):
        fk_relations = model_instance.relationship_fields()
    else:
        fk_relations = getattr(model_instance, "relationship_fields", [])

    if callable(getattr(model_instance, "partials", None)):
        partials = model_instance.partials
    else:
        partials = getattr(model_instance, "partials", [])

    # Identify modifiable fields by excluding relationships and partials
    modifiable_fields = [
        field
        for field in all_columns
        if field not in fk_relations and field not in partials
    ]

    return modifiable_fields
