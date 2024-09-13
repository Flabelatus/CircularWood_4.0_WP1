from db import db


class HistoryModel(db.Model):
    """
    Represents the history of changes or events associated with a specific wood entry.

    :Attributes:
        :id (int): The primary key representing a unique history entry.
        :event (str): A string describing the event or change.
        :created_at (str): A timestamp string representing when the event was recorded.
        :wood_id (int): A foreign key linking the history entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
    """
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    created_at = db.Column(db.String)

    wood = db.relationship("WoodModel", back_populates="history")
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))

