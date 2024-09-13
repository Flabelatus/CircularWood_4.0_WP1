from db import db


class TagModel(db.Model):
    """
    Represents a tag that can be associated with one or more wood entries.

    :Attributes:
        :id (int): The primary key representing a unique tag entry.
        :name (str): The name of the tag, which must be unique and cannot be null.
        
        :woods (relationship): A many-to-many relationship linking to the `WoodModel` table 
            through the `woods_tags` table. This represents the wood entries associated with the tag.
    """
    
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    woods = db.relationship("WoodModel", back_populates='tags', secondary="woods_tags")
