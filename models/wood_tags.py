from db import db


class WoodTagsModel(db.Model):
    __tablename__ = 'woods_tags'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wood_id = db.Column(db.Integer, db.ForeignKey('residual_wood.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
