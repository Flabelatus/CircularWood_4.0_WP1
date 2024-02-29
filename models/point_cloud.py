from db import db


class PointCloudModel(db.Model):
    __tablename__ = 'pointcloud'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pcd = db.Column(db.String)

    wood = db.relationship("WoodModel", back_populates='pointcloud')
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))