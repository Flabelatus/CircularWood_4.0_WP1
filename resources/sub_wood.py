import datetime
import os
import json

from typing import Union, List, Dict
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from models import SubWoodModel, UserModel
from schema import SubWoodSchema

sub_wood_blp = Blueprint(
    "Sub Wood Model",
    "sub_wood",
    description="Operations on the sub_wood resource"
)


@sub_wood_blp.route("/subwood")
class SubWoodList(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema(many=True))
    def get(self):
        ...

    @sub_wood_blp.arguments(SubWoodSchema)
    @sub_wood_blp.response(201, SubWoodSchema)
    def post(self, parsed_data: Dict):
        ...


@sub_wood_blp.route("/subwood/<int:subwood_id>")
class SubWoodByID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, subwood_id: int):
        ...

    @jwt_required()
    @sub_wood_blp.arguments(SubWoodSchema)
    @sub_wood_blp.response(200, SubWoodSchema)
    def patch(self, parsed_data: Dict, subwood_id: int):
        ...

    @jwt_required()
    def delete(self, subwood_id: int):
        ...


@sub_wood_blp.route("/subwood/wood/<int:wood_id>")
class SubWoodByWoodID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, wood_id: int):
        ...

    @jwt_required()
    @sub_wood_blp.arguments(SubWoodSchema)
    @sub_wood_blp.response(200, SubWoodSchema)
    def patch(self, parsed_data: Dict, wood_id: int):
        ...

    @jwt_required()
    def delete(self, wood_id: int):
        ...


@sub_wood_blp.route("subwood/design/<int:design_id>")
class SubWoodByDesignID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, design_id: int):
        ...

    @jwt_required()
    @sub_wood_blp.arguments(SubWoodSchema)
    @sub_wood_blp.response(200, SubWoodSchema)
    def patch(self, parsed_data: Dict, design_id: int):
        ...

    @jwt_required()
    def delete(self, design_id: int):
        ...