from db import db

class ProductionModel(db.Model):
    """
    Represents the production information for a wood or sub-wood item, including operations and instructions.

    :Attributes:
        :id (int): The primary key representing a unique production entry.
        :operation (str): The type of operation performed (e.g., milling, sawing).
        :instruction (str): The specific instruction for the operation (e.g., RAPID code).
        :instruction_type (str): The type of instruction (e.g., RAPID, mm).
        :timestamp (int): The timestamp when the operation occurred.
        :status (str): The current status of the production (e.g., pending, done, failed).
        :offset (float): A float representing the offset for the operation, in millimeters.
        :wood_id (int): A foreign key linking the production entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
        :sub_wood_id (int): A foreign key linking the production entry to a specific sub-wood entry.
        :sub_wood (relationship): A relationship linking to the associated `SubWoodModel` entry.
    """
    __tablename__ = "production"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String)
    instruction = db.Column(db.String)
    instruction_type = db.Column(db.String)
    timestamp = db.Column(db.Integer)
    status = db.Column(db.String)
    offset = db.Column(db.Float)

    wood = db.relationship("WoodModel", back_populates='production')
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))

    sub_wood = db.relationship("SubWoodModel", back_populates='production')
    sub_wood_id = db.Column(db.Integer, db.ForeignKey('sub_wood.id'))
    