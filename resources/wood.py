from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ResidualWoodModel, WasteWoodModel
from schema import WoodSchema, WasteWoodSchema


blp = Blueprint('DataWood', 'wood', description='Operations on the wood')


@blp.route('/residual_wood')
class ResidualWoodList(MethodView):

    @blp.response(200, WoodSchema(many=True))
    def get(self):
        wood = ResidualWoodModel.query.all()
        return wood

    @blp.arguments(WoodSchema)
    @blp.response(201, WoodSchema)
    def post(self, parsed_data):
        wood = ResidualWoodModel(**parsed_data)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return wood


@blp.route('/residual_wood/<int:wood_id>')
class ResidualWood(MethodView):

    @blp.response(200, WoodSchema)
    def get(self, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        return wood

    @blp.response(200, WoodSchema)
    def delete(self, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood deleted from database."
        }


@blp.route('/waste_wood')
class WasteWoodList(MethodView):

    @blp.response(200, WasteWoodSchema(many=True))
    def get(self):
        wood = WasteWoodModel.query.all()
        return wood

    @blp.arguments(WasteWoodSchema)
    @blp.response(201, WasteWoodSchema)
    def post(self, parsed_data):
        wood = WasteWoodModel(**parsed_data)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return wood


@blp.route('/waste_wood/<int:wood_id>')
class WasteWood(MethodView):

    @blp.response(200, WasteWoodSchema)
    def get(self, wood_id):
        wood = WasteWoodModel.query.get_or_404(wood_id)
        return wood

    @blp.response(200, WasteWoodSchema)
    def delete(self, wood_id):
        wood = WasteWoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood deleted from database."
        }
