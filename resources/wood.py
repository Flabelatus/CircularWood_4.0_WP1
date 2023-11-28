import datetime

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ResidualWoodModel
from schema import WoodSchema, WoodUpdateSchema

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
        wood.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return wood

    @jwt_required()
    @blp.arguments(WoodSchema)
    @blp.response(200, WoodSchema)
    def delete(self, parsed_data):

        wood_id_str = parsed_data['wood_id']
        wood = ResidualWoodModel.query.filter(ResidualWoodModel.wood_id == wood_id_str).first()

        if wood:
            db.session.delete(wood)
            db.session.commit()
            return {
                "message": "wood deleted from database."
            }
        else:
            abort(404)


@blp.route('/residual_wood/<int:wood_id>')
class ResidualWood(MethodView):

    @blp.response(200, WoodSchema)
    def get(self, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        return wood

    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood deleted from database."
        }

    @jwt_required()
    @blp.arguments(WoodUpdateSchema)
    @blp.response(200, WoodUpdateSchema)
    def patch(self, parsed_data, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        if wood:
            wood.name = parsed_data.get('name', "Iroko natural")
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
            wood.type = parsed_data.get('type', "")
            wood.has_metal = parsed_data.get('has_metal', 0)
            wood.weight = parsed_data.get('weight', 0)
            wood.density = parsed_data.get('density', 0.0)
            wood.image = parsed_data.get('image', '/path/to/image.jpg')
            wood.intake_id = parsed_data.get("intake_id", 1)
            wood.project_label = parsed_data.get('label', "")
            wood.paint = parsed_data.get('paint', "")
            wood.project_type = parsed_data.get('project_type', "")
            wood.is_fire_treated = parsed_data.get('is_fire_treated', 0)
            wood.is_straight = parsed_data.get('is_straight', 1)
            wood.is_planed = parsed_data.get('is_planed', 1)
            wood.storage_location = parsed_data.get('storage_location', "")

        db.session.add(wood)
        db.session.commit()

        return wood