"""DataServiceApiHTTPClient summary ...

"""

import requests
import json
from typing import Dict
from workflow.api_http_client import logger, __configs__
from workflow.api_http_client import HttpClientCore


class DataServiceApiHTTPClient(HttpClientCore):
    
    def __init__(self):
        super().__init__()
        self.base_url = self.params.base_url
        self.username = self.params.credentials['username']
        self.password = self.params.credentials['password']
        self.auth_endpoint = f"{self.base_url}/login"
        self.access_token = None

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

    def _fetch_record(self, url: str) -> Dict:
        """
        Fetch a record from the given URL. Re-authenticates if the token is expired.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers)    
            # If token is expired, re-authenticate and retry
            if response.status_code == 401:
                self.authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Error fetching record: {response.status_code}, {response.text}")
                return {}
            return response.json()

        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return {}

    def wood_bundle_data(self, resource_id=0) -> Dict:
        
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

    def fetch_wood_by_id(self, wood_id=0):
        endpoint = self.api_blueprints.wood_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}")

    def fetch_subwood_by_id(self, subwood_id=0):
        endpoint = self.api_blueprints.subwood_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{subwood_id}")

    def fetch_subwood_by_wood_id(self, wood_id=0):
        endpoint = self.api_blueprints.subwood_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}")
    
    def fetch_subwood_by_design_id(self, design_id=0):
        endpoint = self.api_blueprints.subwood_by_design_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{design_id}")

    def fetch_design_by_id(self, design_id=0):
        endpoint = self.api_blueprints.design_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{design_id}")
    
    def get_design_raw_cad_data(self, design_id=0):
        design_part_data = self.fetch_design_by_id(design_id)
        if design_part_data:
            return design_part_data.get('features')

    def fetch_design_by_wood_id(self, wood_id=0):
        endpoint = self.api_blueprints.design_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}")
    
    def fetch_production_by_id(self, production_id=0):
        endpoint = self.api_blueprints.production_by_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{production_id}")
    
    def fetch_production_by_wood_id(self, wood_id=0):
        endpoint = self.api_blueprints.production_by_wood_id_route
        return self._fetch_record(url=f"{self.base_url}{endpoint}{wood_id}")
    
    def post_wood(self, data):
        endpoint = self.api_blueprints.wood_route
        