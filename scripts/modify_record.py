"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from load_dotenv import load_dotenv
from marshmallow import Schema, fields

from workflow.api_client import modify_wood_rows
from models.wood import WoodModel
from schema import WoodSchema
from settings import logger


load_dotenv()


class Endpoints:

    def __init__(self, fields_endpoint, data_endpoint, tabelname) -> None:
        self.fields_endpoint = fields_endpoint
        self.data_endpoint = data_endpoint
        self.tablename = tabelname


class ModelModifier:

    def __init__(self) -> None:
        self.url = os.environ.get("URL")
        self.params = Endpoints("/", "/", "")
        self.schema = Schema()

    @property
    def fields(self):
        return self._get_fields()
    
    def _get_fields(self):
        response = requests.get(url=f"{self.url}{self.params.fields_endpoint}")
        if response.status_code == 200:
            # logger.debug(response.json())
            return response.json()
        else:
            logger.error(response.json())

    def _get_data(self, record_id):
        assert record_id > 0, "The ID can not be 0"
        assert isinstance(record_id, int), "The record ID must be an integer"

        response = requests.get(url=f"{self.url}{self.params.data_endpoint}/{record_id}")
        if response.status_code == 200:
            logger.debug(response.json())
            return response.json()
        else:
            logger.error(response.json())
            return None
        
    def authenticate(self):
        username = input("Username: ")
        password = input("Password: ")
        auth_endpoint = f"{self.url}/login"
        payload = {
            "username": username,
            "password": password
        }
        access_token = ""
        response = requests.post(url=auth_endpoint, json=payload)
        logger.debug(response.json())
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            return access_token
        else:
            logger.error(response.json())

    def modify_data(self, record_id, data):
        record = self._get_data(record_id)

        if not record:
            logger.error("No valid record with the ID {0} found".format(record_id))

        for field in data:
            record[field] = data[field]

        access_token = self.authenticate()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        # TODO: CHECK FOR DYNAMIC SCHEMA MAKING SURE NO NULL FIELDS ARE MODIFIED
        for field in record:
            if record[field] == None:
                print(self.schema.filed)

        # Send the API call with the new record
        response = requests.patch(url=f"{self.url}{self.params.data_endpoint}/{record_id}", json=record, headers=headers)
        if response.status_code == 200:
            logger.info(f"{len(data)} fields updated: {data}")
            # logger.debug(existing_record)
        else: 
            logger.error(response.json())
            return False

class WoodModifier(ModelModifier):
    
    def __init__(self) -> None:
        super().__init__()
        self.model = WoodModel.__tablename__
        self.schema = WoodSchema()
        self.params = Endpoints(fields_endpoint="/wood/modifiable-fields", data_endpoint="/wood", tabelname="wood")
        assert self.model == self.params.tablename, "The model is not compatible with wood modifier"

    def reserve(self, wood_id):
        existing_wood = self._get_data(wood_id)
        if not existing_wood:
            logger.error("No valid wood data with the wood ID {0} found".format(wood_id))
        if not existing_wood["reserved"]:
            ...
        

    def unreserve(self, wood_id):
        ...

    def delete(self, wood_id):
        ...

    def set_to_used(self, wood_id):
        ...

    def set_to_unused(self, wood_id):
        ...


if __name__ == "__main__":
    w = WoodModifier()

    data = {
        "length": 1022,
        "source": "Derako"
    }

    w.modify_data(1, data=data)

