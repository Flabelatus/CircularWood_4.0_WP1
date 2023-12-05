from db import db


class DesignRequirementsModelFromClient(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.Integer)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80))
    created_at = db.Column(db.Integer)
    project_id = db.Column(db.String)

    woods = db.relationship("WoodModel", back_populates='requirements', secondary='woods_requirements')
