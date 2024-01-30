from db import db


class ProductionModel(db.Model):
    __tablename__ = "production"

    id = db.Column(db.Integer, primary_key=True)

    # milling / sawing
    operation = db.Column(db.String)

    # RAPID
    instruction = db.Column(db.String)

    # This is a RAPID or mm in length for example
    instruction_type = db.Column(db.String)
    timestamp = db.Column(db.Integer)

    # pending, done , failed
    status = db.Column(db.String)

    wood = db.relationship("WoodModel", back_populates='production')
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
