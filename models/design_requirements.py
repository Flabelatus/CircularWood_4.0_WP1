from db import db

from models.interface_model import DataModelInterface


class DesignRequirementsModelFromClient(db.Model, DataModelInterface):
    """
    Represents the design requirements submitted by a client for a specific wood project.

    :Attributes:
        :id (int): The primary key representing a unique design requirement entry.
        :part_index (int): An integer index representing the part of the design the requirement applies to.
        :features (str): A string representing specific features requested in the design.
        :tag (str): A string tag used to categorize or identify the design requirement.
        :part (str): A string representing the part or section of the design.
        :created_at (str): A timestamp string representing when the design requirement was created.
        :project_id (str): A string representing the ID of the project the requirement belongs to.
        :wood_id (int): An integer representing the ID of the associated wood entry.
        
        :woods (relationship): A many-to-many relationship linking to the `WoodModel` table 
            through the `woods_requirements` table. This represents the wood materials 
            associated with the design requirement.
        
        :sub_wood (relationship): A dynamic relationship linking to the `SubWoodModel` table. 
            This represents the sub-wood components linked to the design requirement.
    """
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_index = db.Column(db.Integer)
    features = db.Column(db.String)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80))
    created_at = db.Column(db.String)
    project_id = db.Column(db.String)
    wood_id = db.Column(db.Integer)

    woods = db.relationship(
        "WoodModel", back_populates='requirements', secondary='woods_requirements')
    sub_wood = db.relationship(
        "SubWoodModel", back_populates='requirements', lazy="dynamic")