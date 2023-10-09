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

        # Get the latest item in the database
        last_wood_in_db = ResidualWoodModel.query.order_by(ResidualWoodModel.id.desc()).first()

        # Get the integer value of the last wood_id
        wood_db_int = int(last_wood_in_db.wood_id)

        # Set the new wood_id incrementing based on the formatting e.g. '0000001' from the
        # last existing wood_id in the database
        wood.wood_id = '0' * (7 - len(str(wood_db_int))) + str(wood_db_int + 1)

        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return wood

    @blp.arguments(WoodSchema(partial=["length", "width", "height", "timestamp", "color", "density", "weight"]))
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

    @blp.response(200, WoodSchema)
    def delete(self, wood_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood deleted from database."
        }

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
            # wood.timestamp = parsed_data.get('timestamp', "")
            wood.type = parsed_data.get('type', "")
            wood.weight = parsed_data.get('weight', 0)
            wood.density = parsed_data.get('density', 0.0)
            wood.image = parsed_data.get('image', '/path/to/image.jpg')
            wood.intake_id = parsed_data.get("intake_id", 1)
            wood.wood_species = parsed_data.get('wood_species', "")
            wood.label = parsed_data.get('label', "")
            wood.paint = parsed_data.get('paint', "")
            wood.project_type = parsed_data.get('project_type', "")
            wood.is_fire_treated = parsed_data.get('is_fire_treated', 0)
            wood.is_straight = parsed_data.get('is_straight', 1)
            wood.is_planed = parsed_data.get('is_planed', 1)
            wood.storage_location = parsed_data.get('storage_location', "")
            wood.wood_id = parsed_data.get('wood_id', "")

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
