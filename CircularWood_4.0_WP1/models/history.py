from db import db


class HistoryModel(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    created_at = db.Column(db.String)

    wood = db.relationship("WoodModel", back_populates="history")
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
