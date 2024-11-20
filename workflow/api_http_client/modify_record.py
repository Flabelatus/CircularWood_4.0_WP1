"""_summary_

"""

import os
import sys

from inspect import getmembers, isclass
from collections import defaultdict

import requests

from sqlalchemy.orm import RelationshipProperty
from sqlalchemy import inspect
from marshmallow import Schema, fields

from models.wood import WoodModel
from models.sub_wood import SubWoodModel
from models.production import ProductionModel
from models.tags import TagModel
from models.design_requirements import DesignRequirementsModelFromClient
from models.user import UserModel

from workflow.api_http_client import logger, __resources__, __api__
from workflow.api_http_client.api_client import DataServiceApiHTTPClient

from schema import WoodSchema, SubWoodSchema
from schema import ProductionSchema, UserSchema
from schema import DesignRequirementSchema, TagSchema


_models = [key for key in __api__]
data_endpts = [__resources__.endpoints_by_field(model)[0] for model in _models]
tablenames = [__resources__.tablename_by_field(model) for model in _models]

_data_model_params = {
    _models[i]: { 
        "field_endpoints": f"/{_models[i]}/modifiable-fields",
        "data_endpoint": data_endpts[i],
        "tablename": tablenames[i]
    } for i in range(len(_models))
}


class ModelModifier(DataServiceApiHTTPClient):

    def __init__(self) -> None:
        super().__init__()

        self.data_model_params = defaultdict(field_endpoints="/", data_endpoint="/", tablename="")
        
        self.schema = Schema()
        self.model = "base"
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
        response = requests.get(url=f"{self.base_url}{self.data_model_params.get('field_endpoints')}")
        if response.status_code == 200:
            # logger.debug(response.json())
            return response.json()['modifiable_fields']
        else:
            logger.error(response.json())

    def _get_data(self, record_id):
        assert record_id > 0, "The ID can not be 0"
        assert isinstance(record_id, int), "The record ID must be an integer"

        response = requests.get(url=f"{self.base_url}{self.data_model_params.get('data_endpoint')}/{record_id}")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(response.json())
            return None
        
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

        # Get the data endpoints
        data_endpoint = self.data_model_params["data_endpoint"]
        if self.data_model_params["tablename"] == "users":
            data_endpoint = "/user"

        # Send the API call with the new record
        response = requests.patch(url=f"{self.base_url}{data_endpoint}/{record_id}", json=updated_data, headers=headers)
        if response.status_code == 200:
            logger.info(f"{len(data)} fields updated: {data}")
            # logger.debug(existing_record)
        else: 
            logger.error(response.json())
            return False

    def delete(self, record_id_list):
        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for record_id in record_id_list:
            response = requests.delete(
                url=f"{self.base_url}{self.data_model_params.data_endpoint}/{record_id}",
                headers=headers
            )
            if response.status_code == 200:
                logger.info("Record from {0} table; with ID: {1} successfully removed - 200".format(self.model, record_id))
                logger.debug(response.json())
            elif response.status_code == 404:
                logger.error("Record from {0} table; with ID: {1} not found - 404: message: {2}".format(self.model, record_id, response.json()))
                continue
            else:
                logger.error(response.json())
                continue


class WoodModifier(ModelModifier):
    
    def __init__(self) -> None:
        super().__init__()
        self.model = WoodModel.__tablename__
        self.schema = WoodSchema()
        self.data_model_params = _data_model_params.get("wood")
        assert self.model == self.data_model_params.get("tablename"), "The model is not compatible with wood modifier"

    def handle_reservation(self, wood_id_list: list, reserve_wood=True):
        
        action = 'reserve' if reserve_wood else 'unreserve'

        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for wood_id in wood_id_list:
            response = requests.get(
                url=f"{self.base_url}{self.data_model_params.data_endpoint}/{action}/{wood_id}",
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

    def set_as_used(self, wood_id_list):

        access_token = self.authenticate()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }

        for wood_id in wood_id_list:
            response = requests.post(
                url=f"{self.base_url}{self.data_model_params.data_endpoint}/used/{wood_id}",
                headers=headers
            )

            if response.status_code == 200:
                logger.info("Wood with ID: {0} successfully used".format(wood_id))
                logger.debug(response.json()['used'])
            
            else:
                logger.error(response.json())
                continue

    def update(self, wood_id, data):
        self.modify_data(record_id=wood_id, data=data)


class SubWoodModifier(ModelModifier):
    def __init__(self) -> None:
        super().__init__()
        self.model = SubWoodModel.__tablename__
        self.schema = SubWoodSchema()
        self.data_model_params = _data_model_params.get("sub_wood")
        assert self.model == self.data_model_params.get('tablename'), "The model is not compatible with subwood modifier"

    def update(self, subwood_id, data):
        self.modify_data(record_id=subwood_id, data=data)


class DesignMetaDataModifier(ModelModifier):
    def __init__(self) -> None:
        super().__init__()
        self.model = DesignRequirementsModelFromClient.__tablename__
        self.schema = DesignRequirementSchema()
        self.data_model_params = _data_model_params.get("requirements")
        assert self.model == self.data_model_params.get('tablename'), "The model is not compatible with design requirements modifier"

    def update(self, requirement_id, data):
        self.modify_data(record_id=requirement_id, data=data)


class ProductionModifier(ModelModifier):
    def __init__(self) -> None:
        super().__init__()
        self.model = ProductionModel.__tablename__
        self.schema = ProductionSchema()
        self.data_model_params = _data_model_params.get("production")
        assert self.model == self.data_model_params.get('tablename'), "The model is not compatible with production modifier"

    def update(self, prod_id, data):
        self.modify_data(record_id=prod_id, data=data)


class UserModifier(ModelModifier):
    def __init__(self) -> None:
        super().__init__()
        self.model = UserModel.__tablename__
        self.schema = UserSchema()
        self.data_model_params = _data_model_params.get("users")
        assert self.model == self.data_model_params.get('tablename'), "The model is not compatible with users modifier"

    def update(self, user_id, data):
        self.modify_data(record_id=user_id, data=data)


class TagsModifier(ModelModifier):
    def __init__(self) -> None:
        super().__init__()
        self.model = TagModel.__tablename__
        self.schema = TagSchema()
        self.data_model_params = _data_model_params.get("taglist")
        assert self.model == self.data_model_params.get('tablename'), "The model is not compatible with tags modifier"
    
    def update(self, tag_id, data):
        self.modify_data(record_id=tag_id, data=data)


def get_modifiers_mapping():
    mapped = {}
    current_module = sys.modules[__name__]
    modifiers = [mod for mod in getmembers(current_module, isclass)]
    for _, mod in enumerate(modifiers):
        modifier_name, mdofier_object = mod[0], mod[1]

        if modifier_name != "ModelModifier":
            if "Modifier" in modifier_name:
                mapped[modifier_name] = mdofier_object

    return mapped


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
