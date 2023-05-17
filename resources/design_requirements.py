from time import time
from typing import List, Union

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignRequirementModelFromGH, DesignRequirementsModelFromDashboard, ResidualWoodModel
from schema import DesignRequirementSchema, GHRequirementAndWoodSchema

design_blp = Blueprint(
    'Design Requirements',
    'requirements',
    description='Operations on the requirements generated'
)


@design_blp.route("/requirements/grasshopper")
class DesignRequirements(MethodView):
    # Get all method
    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self) -> List[DesignRequirementModelFromGH]:
        return DesignRequirementModelFromGH.query.order_by(DesignRequirementModelFromGH.created_at.desc()).all()

    @design_blp.arguments(DesignRequirementSchema)
    @design_blp.response(201, DesignRequirementSchema)
    def post(self, parsed_data: dict) -> DesignRequirementModelFromGH:
        design_requirements = DesignRequirementModelFromGH(**parsed_data)
        design_requirements["created_at"] = int(time())
        try:
            db.session.add(design_requirements)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, exc=e, message="error creating design requirements")

        return design_requirements


@design_blp.route("/requirement/grasshopper/<int:requirement_id>")
class DesignRequirementByID(MethodView):
    # Get by ID
    @design_blp.response(200, DesignRequirementSchema)
    def get(self, requirement_id: int) -> Union[DesignRequirementModelFromGH, None]:
        return DesignRequirementModelFromGH.query.get_or_404(requirement_id)

    # Delete
    @design_blp.response(200, DesignRequirementSchema)
    def delete(self, requirement_id: int) -> dict:
        design_requirement = DesignRequirementModelFromGH.query.get_or_404(requirement_id)

        db.session.delete(design_requirement)
        db.session.commit()

        return {
            "message": "requirement removed"
        }


@design_blp.route("/requirements/dashboard")
class DesignRequirementsDashboard(MethodView):
    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self) -> List[DesignRequirementsModelFromDashboard]:
        return DesignRequirementModelFromGH.query.order_by(DesignRequirementModelFromGH.created_at.desc()).all()

    @design_blp.arguments(DesignRequirementSchema)
    @design_blp.response(200, DesignRequirementSchema)
    def post(self, parsed_data: dict) -> Union[DesignRequirementsModelFromDashboard, None]:
        design_requirements = DesignRequirementsModelFromDashboard(**parsed_data)
        design_requirements["created_at"] = int(time())
        try:
            db.session.add(design_requirements)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, exc=e, message="error creating design requirements")

        return design_requirements


@design_blp.route("/requirement/dashboard/<int:requirement_id>")
class DesignRequirementDashboardByID(MethodView):
    @design_blp.response(200, DesignRequirementSchema)
    def get(self, requirement_id: int) -> Union[DesignRequirementsModelFromDashboard, None]:
        return DesignRequirementsModelFromDashboard.query.get_or_404(requirement_id)

    @design_blp.response(200, DesignRequirementSchema)
    def delete(self, requirement_id: int) -> dict:
        design_requirement = DesignRequirementsModelFromDashboard.query.get_or_404(requirement_id)
        db.session.delete(design_requirement)
        db.session.commit()

        return {
            "message": "requirement removed"
        }


@design_blp.route("/gh/residual_wood/<int:wood_id>/requirement/<int:requirement_id>")
class LinkGHRequirementsToWood(MethodView):

    @design_blp.response(201, GHRequirementAndWoodSchema)
    def post(self, wood_id, requirement_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        requirement_gh = DesignRequirementModelFromGH.query.get_or_404(requirement_id)

        wood.requirements_gh.append(requirement_gh)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, exc=e, message="error linking gh requirement to wood")

        return {
            "requirement": requirement_gh,
            "wood": wood
        }

    @design_blp.response(200, GHRequirementAndWoodSchema)
    def delete(self, wood_id, requirement_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        requirement_gh = DesignRequirementModelFromGH.query.get_or_404(requirement_id)

        wood.requirements_gh.remove(requirement_gh)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, exc=e, message="error removing gh requirement from wood")

        return {
            "message": "wood removed from requirement",
            "wood": wood,
            "requirement": requirement_gh
        }


@design_blp.route("/dashboard/residual_wood/<int:wood_id>/requirement/<int:requirement_id>")
class LinkDashboardRequirementsToWood(MethodView):

    @design_blp.response(201, GHRequirementAndWoodSchema)
    def post(self, wood_id, requirement_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        requirement_dashboard = DesignRequirementModelFromGH.query.get_or_404(requirement_id)

        wood.requirements_gh.append(requirement_dashboard)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, exc=e, message="error linking dashboard requirement to wood")

        return {
            "requirement": requirement_dashboard,
            "wood": wood
        }

    @design_blp.response(200, GHRequirementAndWoodSchema)
    def delete(self, wood_id, requirement_id):
        wood = ResidualWoodModel.query.get_or_404(wood_id)
        requirement_dashboard = DesignRequirementsDashboard.query.get_or_404(requirement_id)

        wood.requirements_gh.remove(requirement_dashboard)
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

