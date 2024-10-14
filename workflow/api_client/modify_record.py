"""_summary_

"""

import os
import sys
import inspect

import requests

from load_dotenv import load_dotenv
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import inspect
from marshmallow import Schema, fields

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

        self.field_type_mapping = {
            fields.Integer: int,
            fields.String: str,
            fields.Float: float,
            fields.Boolean: bool,
            fields.Date: 'datetime.date',
            fields.DateTime: 'datetime.datetime',
        }

    @property
    def fields(self):
        return self._get_fields()
    
    def _get_fields(self):
        response = requests.get(url=f"{self.url}{self.params.fields_endpoint}")
        if response.status_code == 200:
            # logger.debug(response.json())
            return response.json()['modifiable_fields']
        else:
            logger.error(response.json())

    def _get_data(self, record_id):
        assert record_id > 0, "The ID can not be 0"
        assert isinstance(record_id, int), "The record ID must be an integer"

        response = requests.get(url=f"{self.url}{self.params.data_endpoint}/{record_id}")
        if response.status_code == 200:
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

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            return access_token
        else:
            logger.error(response.json())

    def modify_data(self, record_id, data):
        record = self._get_data(record_id)
        updated_data = {}
        if not record:
            logger.error("No valid record with the ID {0} found".format(record_id))

        for field in data:
            record[field] = data[field]

        access_token = self.authenticate()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        for field in self.fields:

            # Handle the Null fields
            if field in record and not record[field]:
                field_type = type(self.schema.declared_fields[field])
                python_supported_type = self.field_type_mapping.get(field_type, 'Unknown')
                
                if python_supported_type == type(str()):
                    record[field] = ""
                elif python_supported_type == type(bool()):
                    record[field] = False
                elif python_supported_type == type(int()):
                    record[field] = 0

            updated_data[field] = record[field]
    
        # Send the API call with the new record
        response = requests.patch(url=f"{self.url}{self.params.data_endpoint}/{record_id}", json=updated_data, headers=headers)
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

    def handle_reservation(self, wood_id_list: list, reserve_wood=True):
        
        action = 'reserve' if reserve_wood else 'unreserve'

        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for wood_id in wood_id_list:
            response = requests.get(
                url=f"{self.url}{self.params.data_endpoint}/{action}/{wood_id}",
                headers=headers
            )
            if action == "reserve" and response.status_code == 200:
                logger.info("Wood with ID: {0} successfully reserved".format(wood_id))
                logger.debug(response.json()['reserved'])
            elif action == "unreserve" and response.status_code == 200:
                logger.info("Wood with ID: {0} successfully un-reserved".format(wood_id))
                logger.debug(response.json()['reserved'])
            else:
                logger.error(response.json())
                continue

    def delete(self, wood_id_list):
        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for wood_id in wood_id_list:
            response = requests.delete(
                url=f"{self.url}{self.params.data_endpoint}/{wood_id}",
                headers=headers
            )
            if response.status_code == 200:
                logger.info("Wood with ID: {0} successfully removed - 200".format(wood_id))
                logger.debug(response.json())
            elif response.status_code == 404:

                logger.error("Wood with ID: {0} not found - 404".format(wood_id))
                continue
            else:
                logger.error(response.json())
                continue

    def set_as_used(self, wood_id_list):

        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for wood_id in wood_id_list:
            response = requests.post(
                url=f"{self.url}{self.params.data_endpoint}/used/{wood_id}",
                headers=headers
            )

            if response.status_code == 200:
                logger.info("Wood with ID: {0} successfully used".format(wood_id))
                logger.debug(response.json()['used'])
            
            else:
                logger.error(response.json())
                continue


class SubWoodModifier(ModelModifier): ...


class DesignMetaDataModifier(ModelModifier): ...


class ProductionModifier(ModelModifier): ...


class UserModifier(ModelModifier): ...


class TagsModifier(ModelModifier): ...


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

    if callable(getattr(model_instance, "wood_partials", None)):
        partials = model_instance.wood_partials()
    else:
        partials = getattr(model_instance, "wood_partials", [])

    # Identify modifiable fields by excluding relationships and partials
    modifiable_fields = [
        field
        for field in all_columns
        if field not in fk_relations and field not in partials
    ]

    return modifiable_fields
