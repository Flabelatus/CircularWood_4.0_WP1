from db import db


class DesignRequirementsModelFromClient(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.String, nullable=False)
    length = db.Column(db.String, nullable=False)
    width = db.Column(db.String, nullable=False)
    height = db.Column(db.String, nullable=False)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.String(80), nullable=False)

    woods = db.relationship("ResidualWoodModel", back_populates='requirements', secondary='woods_requirements')
