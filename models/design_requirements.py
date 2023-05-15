from db import db


class DesignRequirements(db.Model):
    __tablename__ = "requirements"
    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float(precision=2), nullable=False)
    width = db.Column(db.Float(precision=2), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80), nullable=False)
    