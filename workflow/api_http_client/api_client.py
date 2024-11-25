"""DataServiceApiHTTPClient summary ...

"""

import urllib
import urllib.parse
import requests
import json
from typing import Dict, List, Union, Any
from requests import Response
from workflow.api_http_client import logger, __configs__, _data_model_params
from workflow.api_http_client import HttpClientCore, __api__
from marshmallow import Schema, fields


class DataServiceApiHTTPClient(HttpClientCore):
    
    def __init__(self):
        super().__init__()
        self.base_url = self.params.base_url
        self.username = self.params.credentials['username']
        self.password = self.params.credentials['password']
        # self.data_model_params = _data_model_params
        self.auth_endpoint = f"{self.base_url}/login"
        self.access_token = ""
        self.schema = __api__
        self.field_type_mapping = {
            fields.Integer: int,
            fields.String: str,
            fields.Float: float,
            fields.Boolean: bool,
            fields.Date: 'datetime.date',
            fields.DateTime: 'datetime.datetime',
        }

    def logout(self):
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url=f'{self.base_url}/logout', headers=headers)
            if response.status_code == 200:
                self.access_token = ""
            else:
                logger.error(f'{response.json()}, code: {response.status_code}')
        except ConnectionError as e:
            logger.error(e)

    def authenticate(self):
        payload = {"username": self.username, "password": self.password}
        try:
            response = requests.post(url=self.auth_endpoint, json=payload)
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
            else:
                logger.error(f'{response.json()}, code: {response.status_code}')
        except ConnectionError as e:
            logger.error(e)

    def _get_schema(self, model) -> Schema:
        return self.schema.get(model).get('schema')()
            
    def _extract_model_name_from_url(self, url: str) -> str:
        path = urllib.parse.urlparse(url).path
        path_segments = path.split("/")
        stripped_segment = path_segments[1:-1]
        model_name = '/'.join(stripped_segment)
        # Dealing with special cases
        if model_name == 'subwood':
            model_name = 'sub_wood'
        elif model_name == 'design/client':
            model_name = 'requirements'
        return model_name
    
    def _get_fields(self, model_name: str) -> List[str]:
        
        try:
            response = requests.get(url=f"{self.base_url}/{model_name}/modifiable-fields")
            if response.status_code == 200:
                # logger.debug(response.json())
                return response.json()['modifiable_fields']
            else:
                logger.error(response.json())
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None
        
    def _fetch_record(self, url: str) -> requests.Response:
        """
        Fetch a record from the given URL.
        """
        self._check_auth_status()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(url, headers=headers)    
            response = requests.get(url, headers=headers)    
            # If token is expired, re-authenticate and retry
            if response.status_code == 401:
                self.authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.get(url, headers=headers)
            response = requests.get(url, headers=headers)
            # If token is expired, re-authenticate and retry
            if response.status_code == 401:
                self.authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error fetching record: {response.status_code}, {response.text}")
                return None
            return response
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None
    
    def _check_auth_status(self):
        """Check the status of the auth token, Re-authenticates if the token is expired."""
        admin_route = f"{self.base_url}/admin/wood/1"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(admin_route, headers=headers)    
            if response.status_code == 401:
                self.authenticate()
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None
        
    def _insert_record(self, url: str, record: dict) -> requests.Response:
        ...

    def _update_record(self, url: str, data: dict =None) -> requests.Response:
        model = self._extract_model_name_from_url(url)
        existing_record = self._fetch_record(url).json()
        updated_record = {}
        record_id = urllib.parse.urlparse(url).path.split("/")[-1]
        if not existing_record:
            logger.error("No valid record with the ID {0} found".format(record_id))
        
        for field in data:
            if field not in existing_record:
                logger.error(f'Schema error: "{field}" field does not exist in the {model} model')
                return
            existing_record[field] = data[field]
        
        self._check_auth_status()
        headers = {"Authorization": f"Bearer {self.access_token}"}

        for field in self._get_fields(model):
            # Handle the Null fields
            if field in existing_record and not existing_record[field]:

                field_type = type(self._get_schema(model).declared_fields[field])
                python_supported_type = self.field_type_mapping.get(field_type, 'Unknown')
                
                if python_supported_type == type(str()):
                    existing_record[field] = ""
                elif python_supported_type == type(bool()):
                    existing_record[field] = False
                elif python_supported_type == type(int()):
                    existing_record[field] = 0
            updated_record[field] = existing_record[field]        

        try:
            response = requests.patch(url, json=updated_record, headers=headers)
            if response.status_code == 200:
                logger.info(f"{len(data)} fields updated: {data} within the {model} model")
                # logger.debug(existing_record)
            else: 
                logger.error(response.json())
            return response
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None

    def _delete_record(self, url_list: List[str]) -> List[requests.Response]:
        ...
    
    def wood_bundle_data(self, resource_id=0):
        
        bundle_schema = dict()

        design_metadata = None
        process_title = ""

        wood = self.fetch_wood_by_id(wood_id=resource_id)
        sub_woods = self.fetch_subwood_by_wood_id(wood_id=resource_id)
        production_instructions = self.fetch_production_by_wood_id(wood_id=resource_id)
        design_data = self.fetch_design_by_wood_id(wood_id=resource_id)
        
        if design_data:
            design_metadata = [{key: value for key, value in design.items() if key != 'features'} for design in design_data ]
            process_title = [d['project_id'] for d in design_data][0]
        
        bundle_schema['wood'] = wood
        bundle_schema['process_title'] = process_title
        bundle_schema['production'] = production_instructions
        bundle_schema['sub_wood'] = sub_woods
        bundle_schema['design_metadata'] = design_metadata
        
        # TODO: Remove this test part later
        with open('test.json', 'w') as f:
            json.dump(bundle_schema, f, indent=4)
        return bundle_schema

    def fetch_wood_by_id(self, wood_id=0) -> Union[Dict, None]:
        endpoint = self.api_blueprints.wood_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}").json()

    def fetch_subwood_by_id(self, subwood_id=0) -> Union[List[Dict], None]:
        endpoint = self.api_blueprints.subwood_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{subwood_id}").json()

    def fetch_subwood_by_wood_id(self, wood_id=0) -> Union[List[Dict], None]:
        endpoint = self.api_blueprints.subwood_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}").json()
    
    def fetch_subwood_by_design_id(self, design_id=0) -> Union[Dict, None]:
        endpoint = self.api_blueprints.subwood_by_design_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{design_id}").json()

    def fetch_design_by_id(self, design_id=0) -> Union[Dict, None]:
        endpoint = self.api_blueprints.design_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{design_id}").json()
    
    def get_design_raw_cad_data(self, design_id=0) -> str:
        design_part_data = self.fetch_design_by_id(design_id).json()
        if design_part_data:
            return design_part_data.get('features')

    def fetch_design_by_wood_id(self, wood_id=0) -> Union[List[Dict], None]:
        endpoint = self.api_blueprints.design_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}").json()
    
    def fetch_production_by_id(self, production_id=0) -> Union[Dict, None]:
        endpoint = self.api_blueprints.production_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{production_id}").json()
    
    def fetch_production_by_wood_id(self, wood_id=0) -> Union[List[Dict], None]:
        endpoint = self.api_blueprints.production_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}").json()
    
    def post_wood(self, data):
        endpoint = self.api_blueprints.wood_route
    

    def set_wood_as_used(self, wood_id=0):
        ...
