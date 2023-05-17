from typing import List, Union

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignRequirementModel
from schema import DesignRequirementSchema

design_blp = Blueprint(
    'Design Requirements',
    'requirements',
    description='Operations on the requirements'
)


@design_blp.route("/requirements")
class DesignRequirements(MethodView):
    # Get all method
    @design_blp.response(200, DesignRequirementSchema(many=True))
    def get(self) -> List[DesignRequirementModel]:
        return DesignRequirementModel.query.all()

    @design_blp.arguments(DesignRequirementSchema)
    @design_blp.response(201, DesignRequirementSchema)
    def post(self, parsed_data: dict) -> DesignRequirementModel:
        design_requirements = DesignRequirementModel(**parsed_data)
        try:
            db.session.add(design_requirements)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, exc=e, message="error creating design requirements")

        return design_requirements


@design_blp.route("/requirement/<int:requirement_id>")
class DesignRequirementByID(MethodView):
    # Get by ID
    @design_blp.response(200, DesignRequirementSchema)
    def get(self, requirement_id: int) -> Union[DesignRequirementModel, None]:
        return DesignRequirementModel.query.get_or_404(requirement_id)

    # Delete
    @design_blp.response(200, DesignRequirementSchema)
    def delete(self, requirement_id: int) -> dict:
        design_requirement = DesignRequirementModel.query.get_or_404(requirement_id)

        db.session.delete(design_requirement)
        db.session.commit()

        return {
            "message": "requirement removed"
        }
