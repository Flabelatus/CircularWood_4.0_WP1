import datetime

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import WoodModel, UserModel
from schema import WoodSchema

blp = Blueprint('DataWood', 'wood', description='Operations on the wood resource')

"""
Overview of the routes in this resource
routes:
    /wood
    /wood/{wood_id}
    /wood/delete-record/{wood_id}
    /woods/delete-all-records
    /wood/reserve/{wood_id}
    /wood/unreserve/{wood_id}
"""


@blp.route('/wood')
class WoodList(MethodView):

    @blp.response(200, WoodSchema(many=True))
    def get(self):
        """
        Get all the woods available in the database.

        Returns:
            List[WoodModel]: List of wood objects in the database.
        """

        wood = WoodModel.query.all()
        return wood

    @blp.arguments(WoodSchema)
    @blp.response(201, WoodSchema)
    def post(self, parsed_data):
        """
        Insert a new wood into the database.

        Args:
            parsed_data (dict): Parsed data from the request.

        Returns:
            WoodModel: The newly created wood object.
        """

        wood = WoodModel(**parsed_data)
        wood.subsequent_id = 0
        wood.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Calculate density upfront
        wood.density = wood.weight / (wood.length * wood.height * wood.width) * 1000000

        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))

        wood.current_id = wood.id
        db.session.add(wood)
        db.session.commit()

        return wood


@blp.route('/wood/delete-record/<int:wood_id>')
class WoodHardDeleteByID(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self, wood_id: int) -> dict:
        """
        Delete the wood record from the database by ID. (hard delete meaning that the row will be removed from the
        database).

        Args:
            wood_id (int): The ID of the wood record to be deleted.

        Returns:
            dict: A message indicating the success of the deletion.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood is deleted from the records"
        }


@blp.route('/woods/delete-all-records')
class DeleteWoodRecords(MethodView):
    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self):
        """
        Delete all the wood records from the database. (hard delete meaning that all the rows will be removed from
        the database).

        Returns:
            dict: A message indicating the success of the deletion.
        """
        woods = WoodModel.query.all()
        if len(woods) > 0:
            for wood in woods:
                db.session.delete(wood)
            db.session.commit()
        return {
            "message": "all woods records are deleted from the database"
        }


@blp.route('/wood/<int:wood_id>')
class WoodByID(MethodView):

    @blp.response(200, WoodSchema)
    def get(self, wood_id):
        """
        Get wood by ID.

        Args:
            wood_id (int): The ID of the wood record to be retrieved.

        Returns:
            WoodModel: The wood object with the specified ID.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        return wood

    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self, wood_id):
        """
        Delete wood by ID (soft delete meaning that the record stays in the database).

        Args:
            wood_id (int): The ID of the wood record to be soft-deleted.

        Returns:
            dict: A message indicating the success of the soft deletion.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        user = UserModel.query.get_or_404(get_jwt_identity())

        deleted_at = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if wood and user:
            wood.deleted = True
            wood.deleted_at = deleted_at
            wood.deleted_by = user

        db.session.add(wood)
        db.session.commit()

        return {
            "message": f"wood deleted from database by {user} at {deleted_at}"
        }

    @jwt_required()
    @blp.arguments(WoodSchema)
    @blp.response(200, WoodSchema)
    def patch(self, parsed_data, wood_id):
        """
        Update the wood data in a row by ID.

        Args:
            parsed_data (dict): Parsed data from the request.
            wood_id (int): The ID of the wood record to be updated.

        Returns:
            WoodModel: The updated wood object.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            wood.current_id = parsed_data.get('current_id', wood_id)
            wood.subsequent_id = parsed_data.get('subsequent_id', None)
            wood.name = parsed_data.get('name', "")
            wood.reserved = parsed_data.get('reserved', 0)
            wood.reservation_name = parsed_data.get('reservation_name', "")
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
            wood.metal_bbox_coords = parsed_data.get('metal_bbox_coords', "")
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
            wood.used = parsed_data.get("used", 0)
            wood.used_by = parsed_data.get("used_by", "")
            wood.deleted = parsed_data.get("deleted", 0)
            wood.deleted_by = parsed_data.get("deleted_by", "")
            wood.deleted_at = parsed_data.get("deleted_at", "")
        db.session.add(wood)
        db.session.commit()

        return wood


@blp.route("/wood/reserve/<int:wood_id>")
class WoodReservation(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema)
    def get(self, wood_id: int) -> WoodModel:
        """
        Reserve wood by ID.

        Args:
            wood_id (int): The ID of the wood record to be reserved.

        Returns:
            WoodModel: The reserved wood object.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            wood.reserved = True
            wood.reservation_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            user_id = get_jwt_identity()
            user = UserModel.query.get_or_404(user_id)
            wood.reservation_name = user.username

        db.session.add(wood)
        db.session.commit()

        return wood


@blp.route("/wood/unreserve/<int:wood_id>")
class WoodUnreservation(MethodView):

    @blp.response(200, WoodSchema)
    def get(self, wood_id):
        """
        Unreserve wood by ID.

        Args:
            wood_id (int): The ID of the wood record to be unreserved.

        Returns:
            WoodModel: The unreserved wood object.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        if wood and wood.reserved:
            wood.reserved = False
            wood.reservation_time = ""
            wood.reservation_name = ""

        db.session.add(wood)
        db.session.commit()

        return wood
