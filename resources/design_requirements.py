from time import time
from typing import List, Union

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignRequirementsModelFromClient, WoodModel
from schema import DesignRequirementSchema, DesignRequirementsAndWoodsSchema

design_blp = Blueprint(
    'Design Requirements',
    'requirements',
    description='Operations on the requirements generated'
)


@design_blp.route("/design/client")
class DesignRequirementsFromClient(MethodView):
    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self) -> List[DesignRequirementsModelFromClient]:
        # get all the requirements in the database descending by created time
        return DesignRequirementsModelFromClient.query.order_by(
            DesignRequirementsModelFromClient.created_at.desc()).all()

    @design_blp.arguments(DesignRequirementSchema)
    @design_blp.response(200, DesignRequirementSchema)
    def post(self, parsed_data: dict) -> Union[DesignRequirementsModelFromClient, None]:
        # create the requirement using the parsed data serialized with the schema
        design_requirements = DesignRequirementsModelFromClient(**parsed_data)
        design_requirements.created_at = int(time())
        # insert the created model into the database
        try:
            db.session.add(design_requirements)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, exc=e, message="error creating design requirements")

        return design_requirements


# Operations on the design element by ID
@design_blp.route("/design/client/<int:requirement_id>")
class DesignRequirementsFromClientByID(MethodView):
    @design_blp.response(200, DesignRequirementSchema)
    def get(self, requirement_id: int) -> Union[DesignRequirementsModelFromClient, None]:
        # get the requirement by ID
        return DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

    @jwt_required()
    @design_blp.response(200, DesignRequirementSchema)
    def delete(self, requirement_id: int) -> dict:
        # get the requirement by ID
        design_requirement = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        # remove the requirement from the database
        db.session.delete(design_requirement)
        db.session.commit()

        return {
            "message": "requirement removed"
        }

    @jwt_required()
    @design_blp.arguments(DesignRequirementSchema)
    @design_blp.response(200, DesignRequirementSchema)
    def patch(self, parsed_data, requirement_id: int) -> DesignRequirementsModelFromClient:
        design_req = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        if design_req:
            design_req.part_index = parsed_data.get("part_index", 0)
            design_req.features = parsed_data.get("features", "")
            design_req.part = parsed_data.get("part", "")
            design_req.tag = parsed_data.get("tag", "")
            design_req.project_id = parsed_data.get("project_id", 0)
            design_req.wood_id = parsed_data.get("wood_id", 0)

        db.session.add(design_req)
        db.session.commit()

        return design_req


# Get the design element by project_id
@design_blp.route("/design/client/project/<string:project_id>")
class DesignRequirementsFromClientByProjectID(MethodView):
    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self, project_id: str) -> List[DesignRequirementsModelFromClient]:
        # get all the requirements in the database descending by created time
        return DesignRequirementsModelFromClient.query.filter_by(project_id=project_id).order_by(
            DesignRequirementsModelFromClient.created_at.desc()).all()


@design_blp.route("/wood/link/<int:wood_id>/design/<int:requirement_id>")
class LinkRequirementsToWood(MethodView):

    @design_blp.response(201, DesignRequirementsAndWoodsSchema)
    def get(self, wood_id: int, requirement_id: int) -> dict:
        # get the wood by ID
        wood = WoodModel.query.get_or_404(wood_id)
        # get the requirement by ID
        requirement_dashboard = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

        # add the requirement to the wood's requirement list
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

    @design_blp.response(200, DesignRequirementsAndWoodsSchema)
    def get(self, wood_id: int, requirement_id: int) -> dict:
        # get the wood by ID
        wood = WoodModel.query.get_or_404(wood_id)
        # get the requirement by ID
        requirement_dashboard = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)

        # remove the requirement from the wood's requirement list
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

    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self, wood_id: int) -> List[DesignRequirementsModelFromClient]:
        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            return DesignRequirementsModelFromClient.query.filter_by(wood_id=wood_id).all()
