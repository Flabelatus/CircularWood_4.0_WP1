from db import db


class DesignRequirementsModelFromClient(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.Integer)

    features = db.Column(db.String)

    tag = db.Column(db.String(80))
    part = db.Column(db.String(80))
    created_at = db.Column(db.String)
    project_id = db.Column(db.String)
    wood_id = db.Column(db.Integer)

    woods = db.relationship(
        "WoodModel", back_populates='requirements', secondary='woods_requirements')
    sub_wood = db.relationship(
        "SubWoodModel", back_populates='requirements', lazy="dynamic")
