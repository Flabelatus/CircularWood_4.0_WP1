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
            the data is entered mannually. 

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

    @impact_blp.response(200, ImpactSchema(many=True))
    def get(self) -> List[ImpactModel]:
        """Retrieves all the existing impact records.

        Returns:
            List[ImpactModel]: List of all the impact records
        """
        return ImpactModel.query.all()


# @impact_blp.route("/impact/wood/<int:wood_id>")
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

    @impact_blp.arguments(ImpactSchema)
    @impact_blp.response(200, ImpactSchema)
    def patch(self, parsed_data: Dict, wood_id: int) -> Union[ImpactModel, None]:
        ...

    @jwt_required()
    def delete(self, wood_id: int) -> Union[Dict, None]:
        ...


# @impact_blp.route("/impact/<int:impact_id>")
class ImpactByID(MethodView):
    pass
