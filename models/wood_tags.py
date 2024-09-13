from db import db


class WoodTagsModel(db.Model):
    """
    Represents the many-to-many relationship between wood entries and tags.

    :Attributes:
        :id (int): The primary key representing a unique wood-tag relationship entry.
        :wood_id (int): A foreign key linking to the wood entry.
        :tag_id (int): A foreign key linking to the tag entry.
    """
    
    __tablename__ = 'woods_tags'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

