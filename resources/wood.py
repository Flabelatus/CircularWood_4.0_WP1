from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ResidualWoodModel, WasteWoodModel
from schema import WoodSchema, WasteWoodSchema, WoodUpdateSchema


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

    @blp.arguments(WoodSchema)
    @blp.response(200, WoodUpdateSchema)
    def put(self, parsed_data, wood_id):
        wood = ResidualWoodModel.query.filter_by(id=wood_id).first()
        if wood:
            wood.reserved = parsed_data.get('reserved', 0)
            wood.reservation_name = parsed_data.get('reservation_name', "_")
            wood.reservation_time = parsed_data.get('reservation_time', "")
            wood.length = parsed_data.get('length', 0)
            wood.width = parsed_data.get('width', 0)
            wood.height = parsed_data.get('height', 0)
            wood.color = parsed_data.get('color', "")
            wood.source = parsed_data.get('source', "")
            wood.price = parsed_data.get('price', 0.0)
            wood.info = parsed_data.get('info', "")
            wood.timestamp = parsed_data.get('timestamp', "")
            wood.type = parsed_data.get('type', "")
            wood.weight = parsed_data.get('weight', 0)
            wood.density = parsed_data.get('density', 0.0)

        else:
            wood = ResidualWoodModel(id=wood_id, **parsed_data)

        db.session.add(wood)
        db.session.commit()

        return wood


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
