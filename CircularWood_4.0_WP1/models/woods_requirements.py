# requirements id and wood db id relations new table
from db import db


class WoodsAndRequirementsFromClientModel(db.Model):
    __tablename__ = 'woods_requirements'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'))
