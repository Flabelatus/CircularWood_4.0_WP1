from time import time
from typing import List, Union

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ProductionModel, WoodModel
from schema import ProductionSchema

production_blp = Blueprint(
    'Production planning table',
    'production',
    description='Operations on the production planning resource'
)


@production_blp.route("/production")
class Productions(MethodView):

    @production_blp.response(200, ProductionSchema(many=True))
    def get(self) -> List[ProductionModel]:
        return ProductionModel.query.all()

    @production_blp.arguments(ProductionSchema)
    @production_blp.response(201, ProductionSchema)
    def post(self, parsed_data: dict) -> Union[ProductionModel, None]:
        prod = ProductionModel(**parsed_data)
        prod.current_id = prod.id
        prod.timestamp = int(time())

        try:
            db.session.add(prod)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, exc=err, message="error creating a new production entry")

        return prod


@production_blp.route("/production/<int:production_id>")
class ProductionByID(MethodView):

    @production_blp.response(200, ProductionSchema)
    def get(self, production_id: int) -> ProductionModel:
        prod = ProductionModel.query.get_or_404(production_id)
        return prod

    @jwt_required()
    @production_blp.response(200)
    def delete(self, production_id: int) -> dict:
        prod = ProductionModel.query.get_or_404(production_id)
        db.session.delete(prod)
        db.session.commit()
        return {
            "message": "production row deleted from database."
        }

    @jwt_required()
    @production_blp.arguments(ProductionSchema)
    @production_blp.response(200, ProductionSchema)
    def patch(self, parsed_data: dict, production_id: int) -> ProductionModel:
        prod = ProductionModel.query.get_or_404(production_id)
        if prod:
            prod.operation = parsed_data.get("operation", "")
            prod.instruction = parsed_data.get("instruction", "")
            prod.instruction_type = parsed_data.get("instruction_type", "")
            prod.status = parsed_data.get("status", "")
        db.session.add(prod)
        db.session.commit()

        return prod


@production_blp.route("/production/wood/<int:wood_id>")
class ProductionByWoodID(MethodView):

    @production_blp.response(200, ProductionSchema(many=True))
    def get(self, wood_id: int) -> List[ProductionModel]:
        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            return ProductionModel.query.filter_by(wood_id=wood_id).all()
