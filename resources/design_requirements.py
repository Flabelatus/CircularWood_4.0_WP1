"""_summary_

"""

from time import time
from typing import List, Union

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignRequirementsModelFromClient, WoodModel
from schema import PlainDesignRequirementSchema, DesignRequirementsAndWoodsSchema

design_blp = Blueprint(
    'Design Elements/Requirements',
    'design requirements',
    description='Operations on the design requirements generated'
)


@design_blp.route("/design/client")
class DesignRequirementsFromClient(MethodView):
    """
    Handle design requirements from the client.
    """

    @design_blp.response(200, PlainDesignRequirementSchema(many=True))
    def get(self) -> List[DesignRequirementsModelFromClient]:
        """
        Retrieve all design requirements in the database, ordered by creation time.
        
        :return: List of design requirements from the client.
        """
        return DesignRequirementsModelFromClient.query.order_by(
            DesignRequirementsModelFromClient.created_at.desc()).all()

    @design_blp.arguments(PlainDesignRequirementSchema)
    @design_blp.response(200, PlainDesignRequirementSchema)
    def post(self, parsed_data: dict) -> Union[DesignRequirementsModelFromClient, None]:
        """
        Create a new design requirement using the provided parsed data.

        :param parsed_data: Dictionary of design requirement details.
        :return: The created design requirement or None if an error occurs.
        """
        design_requirements = DesignRequirementsModelFromClient(**parsed_data)
        design_requirements.created_at = int(time())
        try:
            db.session.add(design_requirements)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, exc=e, message="error creating design requirements")

        return design_requirements


@design_blp.route("/design/client/<int:requirement_id>")
class DesignRequirementsFromClientByID(MethodView):
    """
    Handle operations for a specific design requirement by ID.
    """

    @design_blp.response(200, PlainDesignRequirementSchema)
    def get(self, requirement_id: int) -> Union[DesignRequirementsModelFromClient, None]:
        """
        Retrieve a specific design requirement by its ID.

        :param requirement_id: ID of the design requirement.
        :return: The design requirement or 404 if not found.
        """
        return DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

    @jwt_required()
    @design_blp.response(200, PlainDesignRequirementSchema)
    def delete(self, requirement_id: int) -> dict:
        """
        Delete a design requirement by its ID.

        :param requirement_id: ID of the design requirement to delete.
        :return: A message confirming the deletion.
        """
        design_requirement = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        db.session.delete(design_requirement)
        db.session.commit()

        return {
            "message": "requirement removed"
        }

    @jwt_required()
    @design_blp.arguments(PlainDesignRequirementSchema)
    @design_blp.response(200, PlainDesignRequirementSchema)
    def patch(self, parsed_data, requirement_id: int) -> DesignRequirementsModelFromClient:
        """
        Update a design requirement by its ID with the provided parsed data.

        :param parsed_data: Dictionary of updated requirement data.
        :param requirement_id: ID of the requirement to update.
        :return: The updated design requirement.
        """
        design_req = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        if design_req:
            design_req.part_name = parsed_data.get("part_name", 0)
            design_req.part_file_path = parsed_data.get("part_file_path", "")
            design_req.part = parsed_data.get("part", "")
            design_req.tag = parsed_data.get("tag", "")
            design_req.project_id = parsed_data.get("project_id", 0)
            design_req.wood_id = parsed_data.get("wood_id", 0)

        db.session.add(design_req)
        db.session.commit()

        return design_req


@design_blp.route("/design/client/project/<string:project_id>")
class DesignRequirementsFromClientByProjectID(MethodView):
    """
    Retrieve design requirements for a specific project.
    """

    @design_blp.response(200, PlainDesignRequirementSchema(many=True))
    def get(self, project_id: str) -> List[DesignRequirementsModelFromClient]:
        """
        Retrieve all design requirements for a given project ID, ordered by creation time.

        :param project_id: ID of the project.
        :return: List of design requirements.
        """
        return DesignRequirementsModelFromClient.query.filter_by(project_id=project_id).order_by(
            DesignRequirementsModelFromClient.created_at.desc()).all()


@design_blp.route("/wood/link/<int:wood_id>/design/<int:requirement_id>")
class LinkRequirementsToWood(MethodView):
    """
    Link a design requirement to a specific wood item.
    """

    @design_blp.response(201, DesignRequirementsAndWoodsSchema)
    def get(self, wood_id: int, requirement_id: int) -> dict:
        """
        Link a design requirement to the specified wood by their IDs.

        :param wood_id: ID of the wood item.
        :param requirement_id: ID of the design requirement.
        :return: A dictionary containing the linked design requirement and wood.
        """
        wood = WoodModel.query.get_or_404(wood_id)
        requirement_dashboard = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

        wood.requirements.append(requirement_dashboard)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, exc=e, message="error linking dashboard requirement to wood")

        return {
            "design": requirement_dashboard,
            "wood": wood
        }


@design_blp.route("/wood/unlink/<int:wood_id>/design/<int:requirement_id>")
class UnlinkRequirementsFromWood(MethodView):
    """
    Unlink a design requirement from a specific wood item.
    """

    @design_blp.response(200, DesignRequirementsAndWoodsSchema)
    def get(self, wood_id: int, requirement_id: int) -> dict:
        """
        Unlink a design requirement from the specified wood by their IDs.

        :param wood_id: ID of the wood item.
        :param requirement_id: ID of the design requirement.
        :return: A message confirming the unlinking and the wood and requirement details.
        """
        wood = WoodModel.query.get_or_404(wood_id)
        requirement_dashboard = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

        wood.requirements.remove(requirement_dashboard)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, exc=e, message="error removing dashboard requirement from wood")

        return {
            "message": "wood removed from requirement",
            "wood": wood,
            "requirement": requirement_dashboard
        }


@design_blp.route("/design/wood/<int:wood_id>")
class DesignByWoodID(MethodView):
    """
    Retrieve all design requirements associated with a specific wood item.
    """

    @design_blp.response(200, PlainDesignRequirementSchema(many=True))
    def get(self, wood_id: int) -> List[DesignRequirementsModelFromClient]:
        """
        Retrieve all design requirements linked to a specific wood item by its ID.

        :param wood_id: ID of the wood item.
        :return: List of design requirements associated with the wood.
        """
        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            return DesignRequirementsModelFromClient.query.filter_by(wood_id=wood_id).all()