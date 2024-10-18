import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import json

from typing import Union, List
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from models import WoodModel, UserModel, ImpactModel
from schema import WoodSchema
from settings import logger
from resources.routes import Resources


blp = Blueprint('Wood Data Table', 'wood',
                description='Operations on the wood resource')


@blp.route('/admin/wood')
class AdminWoodList(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema(many=True))
    def get(self) -> Union[List[WoodModel], None]:
        """
        Retrieves the list of all available wood in the database. This action can be performed only if you are admin

        Returns:
            Union[List[WoodModel], None]: a list of all the wood existing in the database, this list includes the wood that
            is reserved or soft deleted as well. 
        """
        user_id = get_jwt_identity()
        if user_id != 1:
            abort(
                403, message="you are unauthorized to perform this action. you need admin rights"
            )
        wood = WoodModel.query.all()
        return wood


@blp.route('/admin/wood/<int:wood_id>')
class AdminWoodByID(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema)
    def get(self, wood_id: int) -> Union[WoodModel, None]:
        """
        Get wood by ID as admin. You can retrieve (soft) deleted and reserved wood as well 

        Args:
            wood_id (int): The ID of the unreserved wood record to be retrieved.

        Returns: 
            WoodModel: The unreserved wood object with the specified ID.
        """

        user_id = get_jwt_identity()
        if user_id != 1:
            abort(
                403, message="you are unauthorized to perform this action. you need admin rights"
            )
        wood = WoodModel.query.get_or_404(wood_id)
        return wood

    @jwt_required()
    @blp.arguments(WoodSchema)
    @blp.response(200, WoodSchema)
    def patch(self, parsed_data: dict, wood_id: int) -> Union[WoodModel, None]:
        """
        Update the wood data in a row by ID.

        Args:
            parsed_data (dict): Parsed data from the request.
            wood_id (int): The ID of the wood record to be updated.

        Returns:
            WoodModel: The updated wood object.
        """

        user_id = get_jwt_identity()
        if user_id != 1:
            abort(
                403, message="you are unauthorized to perform this action. you need admin rights"
            )

        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            # wood.current_id = parsed_data.get('current_id', wood_id)
            # wood.subsequent_id = parsed_data.get('subsequent_id', None)
            wood.name = parsed_data.get('name', "")
            wood.reserved = parsed_data.get('reserved', 0)
            wood.reservation_name = parsed_data.get('reservation_name', "")
            wood.reservation_time = parsed_data.get('reservation_time', "")
            wood.length = parsed_data.get('length', 0)
            wood.width = parsed_data.get('width', 0)
            wood.height = parsed_data.get('height', 0)
            wood.color = parsed_data.get('color', "")
            wood.source = parsed_data.get('source', "")
            # wood.price = parsed_data.get('price', 0.0)
            wood.info = parsed_data.get('info', "")
            wood.type = parsed_data.get('type', "")
            wood.has_metal = parsed_data.get('has_metal', 0)
            wood.metal_bbox_coords = parsed_data.get('metal_bbox_coords', "")
            wood.weight = parsed_data.get('weight', 0)
            wood.density = parsed_data.get('density', 0.0)
            wood.image = parsed_data.get('image', '/path/to/image.jpg')
            wood.intake_id = parsed_data.get("intake_id", 1)
            # wood.project_label = parsed_data.get('label', "")
            wood.paint = parsed_data.get('paint', "")
            # wood.project_type = parsed_data.get('project_type', "")
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


@blp.route('/admin/wood/delete-record/<int:wood_id>')
class WoodHardDeleteByID(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self, wood_id: int) -> dict:
        """
        Delete the wood record from the database by ID. (hard delete meaning that the row will be removed from the
        database). This action can be done only via admin

        Args:
            wood_id (int): The ID of the wood record to be deleted.

        Returns:
            dict: A message indicating the success of the deletion.
        """
        user_id = get_jwt_identity()
        if user_id != 1:
            abort(
                403, message="you are unauthorized to perform this action. you need admin rights"
            )
        wood = WoodModel.query.get_or_404(wood_id)
        db.session.delete(wood)
        db.session.commit()
        return {
            "message": "wood is deleted from the records"
        }


@blp.route('/admin/woods/delete-all-records')
class DeleteWoodRecords(MethodView):
    @jwt_required()
    @blp.response(200, WoodSchema)
    def delete(self):
        """
        Delete all the wood records from the database. (hard delete meaning that all the rows will be removed from
        the database). This action can only be done if you are admin

        Returns:
            dict: A message indicating the success of the deletion.
        """
        user_id = get_jwt_identity()
        if user_id != 1:
            abort(
                403, message="you are unauthorized to perform this action. you need admin rights"
            )
        woods = WoodModel.query.all()
        if len(woods) > 0:
            for wood in woods:
                db.session.delete(wood)
            db.session.commit()
        return {
            "message": "all woods records are deleted from the database"
        }


@blp.route('/wood')
class WoodList(MethodView):

    @blp.response(200, WoodSchema(many=True))
    def get(self):
        """
        Get all the woods that are not reserved or deleted in the database.

        Returns:
            List[WoodModel]: List of wood objects in the database.
        """

        wood = WoodModel.query.filter_by(deleted=False).all()
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
        wood.density = wood.weight / \
                       (wood.length * wood.height * wood.width) * 1000000

        try:
            db.session.add(wood)
            db.session.commit()
            wood.current_id = wood.id
            db.session.add(wood)
            db.session.commit()

            # Create the impact entry
            root_path = os.getcwd()
            path_to_idemat = os.path.join(
                root_path, "idemat", "idenmat_2023_wood_simplified.json"
            )

            impact = ImpactModel()

            with open(path_to_idemat) as idemat_database:
                idemat_rows = json.load(idemat_database)
                wood_found = False
                if wood.name is not None:
                    for row in idemat_rows:
                        if wood.name not in row["process"]:
                            continue
                        else:
                            wood_found = True
                            impact.carbon_footprint = float(
                                row["carbon"]) * (float(wood.weight) / 1000)
                            impact.codename = row["code"]
                            impact.eco_costs = float(
                                row["eco-costs"]) * (float(wood.weight) / 1000)
                            impact.footprint = float(
                                row["footprint"]) * (float(wood.weight) / 1000)
                            impact.human_health = float(
                                row["human_health"]) * (float(wood.weight) / 1000)
                            impact.eco_toxicity = float(
                                row["exo-tocicity"]) * (float(wood.weight) / 1000)
                            impact.process = row["process"]
                            impact.resource_depletion = float(
                                row["resource"]) * (float(wood.weight) / 1000)
                            impact.wood_id = wood.id
                    if not wood_found:
                        return wood

                    db.session.add(impact)
                    db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))

        return wood


@blp.route('/wood/<int:wood_id>')
class WoodByID(MethodView):

    @blp.response(200, WoodSchema)
    def get(self, wood_id):
        """
        Get wood by ID as long as it is not reserved or deleted.

        Args:
            wood_id (int): The ID of the unreserved wood record to be retrieved.

        Returns: 
            WoodModel: The unreserved wood object with the specified ID.
        """
        wood = WoodModel.query.get_or_404(wood_id)
        # if wood.reserved is True:
        #     abort(
        #         400,
        #         message="the wood is currently reserved, if you made the reservation on this item and would \
        #         like to retrieve the info about it, you can login and use this endpoint instead: /logged_in/wood/<int:wood_id>")

        if wood.deleted is True:
            abort(404, message="this wood is deleted from the database")

        return wood

    @jwt_required()
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

        def delete_wood(w, u):
            w.deleted = True
            w.deleted_at = deleted_at
            w.deleted_by = u.username

        if wood and user:
            if not wood.deleted:
                if not wood.reserved:
                    delete_wood(w=wood, u=user)
                else:
                    if wood.reservation_name == user.username:
                        delete_wood(w=wood, u=user)
                        wood.reserved = False
                        wood.reservation_name = ""
                        wood.reservation_time = ""
                    else:
                        abort(
                            404, message="this wood is currently reserved by another user")
            else:
                abort(404, message="this wood is already deleted from the database")
        db.session.add(wood)
        db.session.commit()

        return {
                   "message": f"wood deleted from database by {user.username} at {deleted_at}",
               }, 200

    @jwt_required()
    @blp.arguments(WoodSchema)
    @blp.response(200, WoodSchema)
    def patch(self, parsed_data, wood_id):
        """
        Update the details of a wood item, including its dimensions, location, treatment, etc.,
        identified by its unique wood ID. If you've already reserved the wood, you're allowed to
        adjust its information. However, others cannot modify the details of a wood item that you've
        reserved, and likewise, you cannot alter the details of wood items reserved by others.
        Information such as reservation, deletion, usability would not be adjusted
        in this method.

        Args:
            parsed_data (dict): Parsed data from the request.
            wood_id (int): The ID of the wood record to be updated.

        Returns:
            WoodModel: The updated wood object.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        user = UserModel.query.get_or_404(get_jwt_identity())
        if wood:
            if wood.deleted is True:
                abort(400, message="this wood is deleted from the database")
            if wood.reserved and wood.reservation_name != user.username:
                abort(
                    400,
                    message="this wood is reserved by another user, you do not have permission to make changes to it")
            # wood.current_id = parsed_data.get('current_id', wood_id)
            # wood.subsequent_id = parsed_data.get('subsequent_id', None)
            wood.name = parsed_data.get('name', "")
            wood.length = parsed_data.get('length', 0)
            wood.width = parsed_data.get('width', 0)
            wood.height = parsed_data.get('height', 0)
            wood.color = parsed_data.get('color', "")
            wood.source = parsed_data.get('source', "")
            # wood.price = parsed_data.get('price', 0.0)
            wood.info = parsed_data.get('info', "")
            wood.type = parsed_data.get('type', "")
            wood.has_metal = parsed_data.get('has_metal', 0)
            wood.metal_bbox_coords = parsed_data.get('metal_bbox_coords', "")
            wood.weight = parsed_data.get('weight', 0)
            wood.density = parsed_data.get('density', 0.0)
            wood.image = parsed_data.get('image', '/path/to/image.jpg')
            # wood.project_label = parsed_data.get('label', "")
            wood.paint = parsed_data.get('paint', "")
            # wood.project_type = parsed_data.get('project_type', "")
            wood.is_fire_treated = parsed_data.get('is_fire_treated', 0)
            wood.is_straight = parsed_data.get('is_straight', 1)
            wood.is_planed = parsed_data.get('is_planed', 1)
            wood.storage_location = parsed_data.get('storage_location', "")

        db.session.add(wood)
        db.session.commit()

        return wood


@blp.route('/wood/used/<int:wood_id>')
class SetWoodToUsedByID(MethodView):

    @jwt_required()
    @blp.response(200, WoodSchema)
    def post(self, wood_id: int) -> Union[WoodModel, None]:
        """
        Set the status of the wood to be as 'Used'. This is more in the sense of the occasions that the wood 
        is consumed for a specific design or project. The user can set it to used.

        Args:
            wood_id (int): The ID of the wood that needs to be set to used. 

        Returns:
            Union[WoodModel, None]: The model of the wood that was set to 'Used'
        """
        wood = WoodModel.query.get_or_404(wood_id)
        user = UserModel.query.get_or_404(get_jwt_identity())

        if wood.deleted is True:
            abort(404, message="the wood is deleted from the database")
        if wood.reserved and wood.reservation_name != user.username:
            abort(
                400, message="wood is reserved by another user, you can not make changes to it")
        if wood.used is True:
            abort(400, message="wood is already set to used")

        wood.used = True
        wood.used_by = user.username

        db.session.add(wood)
        db.session.commit()

        return wood


@blp.route("/logged_in/wood/<int:wood_id>")
class WoodByIDAsLoggedInUser(MethodView):
    @jwt_required()
    @blp.response(200, WoodSchema)
    def get(self, wood_id: int) -> Union[WoodModel, None]:
        """
        Retrieve the wood by ID, this will show the reserved wood if you are the user who reserved it.

        Args:
            wood_id (int): _description_

        Returns:
            Union[WoodModel, None]: _description_
        """
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        wood = WoodModel.query.get_or_404(wood_id)

        if wood.reserved and wood.reservation_name != user.username:
            abort(400, message="This wood is reserved by another user")
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
            if wood.reserved is True:
                abort(400, message="this wood is already reserved")
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
        Unreserve wood by ID as long as it is not deleted.

        Args:
            wood_id (int): The ID of the wood record to be unreserved.

        Returns:
            WoodModel: The unreserved wood object.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            if wood.reserved is False:
                abort(400, message="did not do anything since the wood was not reserved")
            wood.reserved = False
            wood.reservation_time = ""
            wood.reservation_name = ""

        db.session.add(wood)
        db.session.commit()

        return wood


wood_resources = Resources().__routes__["wood"]
wood_endpoints = wood_resources["endpoints"]

view_func_routes_mapping = list(zip(blp._endpoints, wood_endpoints))

for view_func in view_func_routes_mapping:
    blp.add_url_rule(rule="/", endpoint=view_func[1], view_func=view_func[0])

wood_endpoints = [endpoint for endpoint in blp._endpoints if endpoint.startswith("/")]