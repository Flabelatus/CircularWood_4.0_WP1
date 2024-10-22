from db import db

from models.interface_model import DataModelInterface


class PointCloudModel(db.Model, DataModelInterface):
    """
    Represents the point cloud data associated with a specific wood entry.

    :Attributes:
        :id (int): The primary key representing a unique point cloud entry.
        :pcd (str): The point cloud data in string format.
        :wood_id (int): A foreign key linking the point cloud entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
    """
    __tablename__ = 'pointcloud'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pcd = db.Column(db.String)

    wood = db.relationship("WoodModel", back_populates='pointcloud')
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    
    @property
    def partials(self):
        partials = (
            [
                "id",
            ],
        )
        return self._get_status_fields(partials[0])
