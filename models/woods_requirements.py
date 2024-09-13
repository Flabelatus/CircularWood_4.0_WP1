# requirements id and wood db id relations new table
from db import db


class WoodsAndRequirementsFromClientModel(db.Model):
    """
    Represents the many-to-many relationship between wood entries and design requirements from clients.

    :Attributes:
        :id (int): The primary key representing a unique wood-requirement relationship entry.
        :wood_id (int): A foreign key linking to the wood entry.
        :requirement_id (int): A foreign key linking to the design requirement entry.
    """
    
    __tablename__ = 'woods_requirements'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'))
