"""DataServiceApiHTTPClient summary ...

"""

import urllib
import urllib.parse
import requests
from typing import Dict, List, Union
from workflow.api_http_client import logger, __configs__
from workflow.api_http_client import HttpClientCore, __api__
from marshmallow import Schema, fields


class DataServiceApiHTTPClient(HttpClientCore):
    
    def __init__(self):
        super().__init__()
        self.base_url = self.params.base_url
        self.username = self.params.credentials['username']
        self.password = self.params.credentials['password']
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
    
    def _extract_record_id_from_url(self, url: str) -> str:
        return urllib.parse.urlparse(url).path.split("/")[-1]
    
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
        try:
            response = requests.get(url)    
            if response.status_code != 200:
                logger.error(f"Error fetching record: {response.status_code}, {response.text}")
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
        try:
            response = requests.post(url=url, json=record)
            if response.status_code != 201:
                logger.error(f"Error inserting record: {response.status_code}, {response.text}")
                return None
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None

    def _update_record(self, url: str, data: dict =None) -> requests.Response:
        model = self._extract_model_name_from_url(url)
        existing_record = self._fetch_record(url).json()
        updated_record = {}
        record_id = self._extract_record_id_from_url(url)
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

    def _delete_record(self, url: str) -> List[requests.Response]:
        self._check_auth_status()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }
        record_id = self._extract_record_id_from_url(url)
        model = self._extract_model_name_from_url(url)
        response = requests.delete(url=url, headers=headers)
        if response.status_code == 200:
            logger.info(
                "Record from {0} table; with ID: {1} successfully removed - 200"
                .format(model, record_id)
            )
        elif response.status_code == 404:
            logger.error(
                "Record from {0} table; with ID: {1} not found - 404: message: {2}"
                .format(model, record_id, response.json())
            )
        else:
            logger.error(response.json())
        return response

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
    
    def update_wood_by_id(self, wood_id: int, data: dict) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_by_id_route}{wood_id}"
        return self._update_record(url=url, data=data)

    def update_subwood_by_id(self, subwood_id: int, data: dict) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.subwood_by_id_route}{subwood_id}"
        return self._update_record(url=url, data=data)
        
    def update_production_by_id(self, production_id: int, data: dict) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.production_by_id_route}{production_id}"
        return self._update_record(url=url, data=data)
        
    def update_design_by_id(self, design_id: int, data: dict) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.design_by_id_route}{design_id}"
        return self._update_record(url=url, data=data)            
    
    def update_tag_by_id(self, tag_id: int, data: dict) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.tag_by_id_route}{tag_id}"
        return self._update_record(url=url, data=data)
    
    def remove_wood_by_id(self, wood_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_by_id_route}{wood_id}"
        return self._delete_record(url=url)

    def remove_subwood_by_id(self, subwood_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.subwood_by_id_route}{subwood_id}"
        return self._delete_record(url=url)
    
    def remove_design_by_id(self, design_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.design_by_id_route}{design_id}"
        return self._delete_record(url=url)    
    
    def remove_production_by_id(self, production_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.production_by_id_route}{production_id}"
        return self._delete_record(url=url)
    
    def remove_tag_by_id(self, tag_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.tag_by_id_route}{tag_id}"
        return self._delete_record(url=url)
    
    def add_wood(self, data) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_route}"
        return self._insert_record(url=url, record=data)
    
    def add_subwood(self, data) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.subwood_route}"
        return self._insert_record(url=url, record=data)

    def add_production(self, data) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.production_route}"
        return self._insert_record(url=url, record=data)

    def add_design(self, data) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.design_route}"
        return self._insert_record(url=url, record=data)

    def add_tag(self, data) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.taglist_route}"
        return self._insert_record(url=url, record=data)    

    def set_wood_as_used(self, wood_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_set_used_route}{wood_id}"
        self._check_auth_status()
        headers = {"Authorization": "Bearer " + self.access_token}
        try:
            response = requests.post(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error setting the wood usage status: {response.status_code} - {response.text}")
            return response
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")

    def reserve_wood(self, wood_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_reserve_route}{wood_id}"
        self._check_auth_status()
        headers = {"Authorization": "Bearer " + self.access_token}
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error reserving wood: {response.status_code} - {response.text}")
            return response
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")

    def unreserve_wood(self, wood_id: int) -> requests.Response:
        url = f"{self.base_url}{self.api_blueprints.wood_unreserve_route}{wood_id}"
        self._check_auth_status()
        headers = {"Authorization": "Bearer " + self.access_token}
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error reserving wood: {response.status_code} - {response.text}")
            return response
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")


http_client = DataServiceApiHTTPClient()
