import datetime
from typing import List, Dict

from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import HistoryModel, WoodModel
from schema import HistorySchema

history_blp = Blueprint('History model', 'history', description="Operations on the history resource")


@history_blp.route("/history")
class HistoryList(MethodView):

    @history_blp.response(200, HistorySchema(many=True))
    def get(self) -> List[HistoryModel]:
        """
        Get all the history available in the database.

        Returns:
            List[HistoryModel]: List of history objects in the database.
        """
        history_list = HistoryModel.query.all()
        return history_list

    @history_blp.arguments(HistorySchema)
    @history_blp.response(201, HistorySchema)
    def post(self, parsed_data: Dict) -> HistoryModel:
        """
        Insert a new history into the database.

        Args:
            parsed_data (dict): Parsed data from the request.

        Returns:
            HistoryModel: The newly created history object.
        """

        history = HistoryModel(**parsed_data)
        history.created_at = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        wood = WoodModel.query.get_or_404(parsed_data.get("wood_id"), 0)
        if wood:
            wood.history.append(history)
        try:
            db.session.add(history)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, message=str(err))

        return history


@history_blp.route("/history-by-wood-id/<int:wood_id>")
class HistoryByWoodID(MethodView):

    @history_blp.response(200, HistorySchema(many=True))
    def get(self, wood_id: int) -> List[HistoryModel]:
        """
        Get the list of histories by wood ID descending according to time of creation.

        Args:
            wood_id (int): The ID of the wood record to have its histories retrieved.

        Returns:
            List[HistoryModel]: The list of history objects with the specified wood ID.
        """

        wood = WoodModel.query.get_or_404(wood_id)
        if wood:
            return HistoryModel.query.filter_by(wood_id=wood_id).order_by(HistoryModel.created_at.desc()).all()


@history_blp.route("/history/<int:history_id>")
class HistoryByID(MethodView):

    @history_blp.response(200, HistorySchema)
    def get(self, history_id: int) -> HistoryModel:
        """
        Get history by ID.

        Args:
            history_id (int): The ID of the history record to be retrieved.

        Returns:
            HistoryModel: The history object with the specified ID.
        """

        history = HistoryModel.query.get_or_404(history_id)
        return history

    @jwt_required()
    @history_blp.response(200, HistorySchema)
    def delete(self, history_id: int) -> Dict:
        """
          Delete the history record from the database by ID. (hard delete meaning that the row will be removed from the
          database).

          Args:
              history_id (int): The ID of the history record to be deleted.

          Returns:
              dict: A message indicating the success of the deletion.
          """

        history = HistoryModel.query.get_or_404(history_id)
        db.session.delete(history)
        db.session.commit()
        response = {"message": "successfully deleted the history item"}
        return response
