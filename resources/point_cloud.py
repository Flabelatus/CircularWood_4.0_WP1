"""_summary_

"""

from typing import List, Union

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import PointCloudModel
from schema import PointCloudSchema


pointcloud_blp = Blueprint(
    'Pointcloud table',
    'pointcloud',
    description='Operations on the pointcloud resource'
)


@pointcloud_blp.route("/pointcloud")
class PointClouds(MethodView):
    """
    Handle operations related to point clouds.
    """

    @pointcloud_blp.response(200, PointCloudSchema(many=True))
    def get(self) -> List[PointCloudModel]:
        """
        Retrieve all point cloud entries from the database.

        :return: List of point cloud entries.
        """
        return PointCloudModel.query.all()

    @pointcloud_blp.arguments(PointCloudSchema)
    @pointcloud_blp.response(201)
    def post(self, parsed_data: dict) -> int:
        """
        Create a new point cloud entry using the provided parsed data.

        :param parsed_data: Dictionary of point cloud data.
        :return: The ID of the created point cloud entry.
        """
        pointcloud = PointCloudModel(**parsed_data)
        try:
            db.session.add(pointcloud)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, exc=err, message="error creating pointcloud entry")

        return pointcloud.id


@pointcloud_blp.route("/pointcloud/wood/<int:wood_id>")
class PointCloudByWoodID(MethodView):
    """
    Handle operations related to point clouds based on the associated wood ID.
    """

    @pointcloud_blp.response(200, PointCloudSchema)
    def get(self, wood_id: int) -> Union[PointCloudModel, None]:
        """
        Retrieve the point cloud entry associated with a specific wood ID.

        :param wood_id: ID of the wood item.
        :return: The point cloud entry or None if not found.
        """
        return PointCloudModel.query.filter_by(wood_id=wood_id).first()

    @jwt_required()
    @pointcloud_blp.response(200)
    def delete(self, wood_id: int) -> Union[dict, None]:
        """
        Delete the point cloud entry associated with a specific wood ID.

        :param wood_id: ID of the wood item.
        :return: A message confirming the deletion of the point cloud entry.
        """
        pointcloud = PointCloudModel.query.filter_by(wood_id=wood_id).first()
        db.session.delete(pointcloud)
        db.session.commit()

        response = {
            "message": "successfully removed the pointcloud from the records using wood id"
        }

        return response


@pointcloud_blp.route("/pointcloud/<int:pcd_id>")
class PointCloudByID(MethodView):
    """
    Handle operations related to point clouds based on the point cloud ID.
    """

    @pointcloud_blp.response(200, PointCloudSchema)
    def get(self, pcd_id: int) -> Union[PointCloudModel, None]:
        """
        Retrieve a specific point cloud entry by its ID.

        :param pcd_id: ID of the point cloud entry.
        :return: The point cloud entry or 404 if not found.
        """
        return PointCloudModel.query.get_or_404(pcd_id)

    @jwt_required()
    @pointcloud_blp.response(200)
    def delete(self, pcd_id: int) -> Union[dict, None]:
        """
        Delete a specific point cloud entry by its ID.

        :param pcd_id: ID of the point cloud entry to delete.
        :return: A message confirming the deletion of the point cloud entry.
        """
        pointcloud = PointCloudModel.query.get_or_404(pcd_id)
        db.session.delete(pointcloud)
        db.session.commit()

        response = {
            "message": "successfully removed the pointcloud from the records using pointcloud id"
        }

        return response