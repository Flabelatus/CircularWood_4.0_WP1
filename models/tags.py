from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    woods = db.relationship("ResidualWoodModel", back_populates='tags', secondary='woods_tags')
