from db import db


class DesignRequirementsModelFromClient(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.Integer)
    project_id = db.Column(db.Integer, nullable=False)

    woods = db.relationship("ResidualWoodModel", back_populates='requirements', secondary='woods_requirements')
