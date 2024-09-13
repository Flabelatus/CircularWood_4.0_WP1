"""_summary_

"""

import datetime
from typing import List, Dict, Union

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ImpactModel
from schema import ImpactSchema


impact_blp = Blueprint(
    "Impact table",
    "impact",
    description="Operations on the impact resource"
)


@impact_blp.route("/impact")
class ImpactList(MethodView):

    @impact_blp.arguments(ImpactSchema)
    @impact_blp.response(201, ImpactSchema)
    def post(self, parsed_data: Dict) -> Union[ImpactModel, None]:
        """Adds new impact model to the database. This method would be used only in occasions where
            the data is entered manually.

        Args:
            parsed_data (Dict): The parsed data from the schema

        Returns:
            Union[ImpactModel, None]: returns the model if successful
        """

        impact = ImpactModel(**parsed_data)
        try:
            db.session.add(impact)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=str(error))
        return impact

    @impact_blp.response(200, ImpactSchema(many=True))
    def get(self) -> List[ImpactModel]:
        """Retrieves all the existing impact records.

        Returns:
            List[ImpactModel]: List of all the impact records
        """
        return ImpactModel.query.all()


@impact_blp.route("/impact/wood/<int:wood_id>")
class ImpactByWoodID(MethodView):

    @impact_blp.response(200, ImpactSchema)
    def get(self, wood_id: int) -> Union[ImpactModel, None]:
        """Fetches the impact data of the specified wood by ID.

        Args:
            wood_id (int): ID of the wood to check the impact data for

        Returns:
            Union[ImpactModel, None]: The impact model data
        """
        impact = ImpactModel.query.filter_by(wood_id=wood_id).first()
        if impact:
            return impact
        else:
            abort(404, message="no impact model with this wood id found")

    @jwt_required()
    @impact_blp.arguments(ImpactSchema)
    @impact_blp.response(200, ImpactSchema)
    def patch(self, parsed_data: Dict, wood_id: int) -> Union[ImpactModel, None]:
        """Method to update the records of the impact row using the wood id of the wood model related to the impact model

        Args:
            parsed_data (Dict): The arguments that is parsed as dictionary from the JSON payload
            wood_id (int): The wood id

        Returns:
            Union[ImpactModel, None]: The impact model once successful, otherwise None.
        """
        impact = ImpactModel.query.filter_by(wood_id=wood_id).first()
        if not impact:
            abort(404, message="impact model with the wood id not found")

        impact.carbon_footprint = parsed_data.get("carbon", "")
        impact.codename = parsed_data.get("code", "")
        impact.eco_costs = parsed_data.get("eco-costs", "")
        impact.eco_toxicity = parsed_data.get("exo-tocicity", "")
        impact.process = parsed_data.get("process", "")
        impact.human_health = parsed_data.get("human_health", "")
        impact.material = parsed_data.get("material", "")
        impact.resource_depletion = parsed_data.get("resource", "")
        impact.footprint = parsed_data.get("footprint", "")

        try:
            db.session.add(impact)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, message=str(err))

        return impact

    @jwt_required()
    def delete(self, wood_id: int) -> tuple[dict[str, str], int]:
        """Delete the impact model using the wood id of the wood model related to the impact model

        Args:
            wood_id (int): ID of the wood that is related to the impact model

        Returns:
            Union[Dict, None]: The dictionary as the message
        """
        impact = ImpactModel.query.filter_by(wood_id=wood_id).first()
        if not impact:
            abort(404, message="the impact model with current wood id not found")

        db.session.delete(impact)
        db.session.commit()

        return {
            "message": "successfully removed the impact model by wood id",
        }, 200


@impact_blp.route("/impact/<int:impact_id>")
class ImpactByID(MethodView):

    @impact_blp.response(200, ImpactSchema)
    def get(self, impact_id: int) -> Union[ImpactModel, None]:
        """Get the impact model using the impact id

        Args:
            impact_id (int): The impact id 

        Returns:
            Union[ImpactModel, None]: The impact model once successful, otherwise None.
        """
        impact = ImpactModel.query.get_or_404(impact_id)
        return impact

    @jwt_required()
    @impact_blp.arguments(ImpactSchema)
    @impact_blp.response(200, ImpactSchema)
    def patch(self, parsed_data: Dict, impact_id: int) -> Union[ImpactModel, None]:
        """Update the impact model using the impact id

        Args:
            parsed_data (Dict): Parsed arguments from the JSON payload as dictionary.
            impact_id (int): Impact id.

        Returns:
            Union[ImpactModel, None]: The impact model once successful, otherwise None.
        """
        impact = ImpactModel.get_or_404(impact_id)

        if impact:
            impact.carbon_footprint = parsed_data.get("carbon", "")
            impact.codename = parsed_data.get("code", "")
            impact.eco_costs = parsed_data.get("eco-costs", "")
            impact.eco_toxicity = parsed_data.get("exo-tocicity", "")
            impact.process = parsed_data.get("process", "")
            impact.human_health = parsed_data.get("human_health", "")
            impact.material = parsed_data.get("material", "")
            impact.resource_depletion = parsed_data.get("resource", "")
            impact.footprint = parsed_data.get("footprint", "")
        try:
            db.session.add(impact)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, message=str(err))
        return impact

    @jwt_required()
    def delete(self, impact_id: int) -> tuple[dict[str, str], int]:
        """Delete the impact model using the impact id

        Args:
            impact_id (int): Impact id

        Returns:
            Dict: The dictionary as the message
        """
        impact = ImpactModel.get_or_404(impact_id)

        db.session.delete(impact)
        db.session.commit()

        return {
            "message": "successfully deleted impact model"
        }, 200
