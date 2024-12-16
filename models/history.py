from db import db

from models.interface_model import DataModelInterface


class HistoryModel(db.Model, DataModelInterface):
    """
    Represents the history of changes or events associated with a specific wood entry.

    :Attributes:
        :id (int): The primary key representing a unique history entry.
        :name (str): The string name representing the action or the process name.
        :event (str): A string describing the event or change.
        :created_at (str): A timestamp string representing when the event was recorded.
        :success (bool): The status for verification of the action taken place in the manufaturing process
        :wood_id (int): A foreign key linking the history entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
        :requirement_id: (int): A foreign key linking the history entry to a specific design requirement entry.
    """
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    event = db.Column(db.String)
    created_at = db.Column(db.String)
    success = db.Column(db.Boolean)

    wood = db.relationship("WoodModel", back_populates="history")
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'))

    @property
    def partials(self):
        partials = (
            [
                "id",
                "created_at"
            ],
        )
        return self._get_status_fields(partials[0])
