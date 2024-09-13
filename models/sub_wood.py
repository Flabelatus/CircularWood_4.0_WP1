from db import db


class SubWoodModel(db.Model):
    """
    Represents the sub-wood components linked to the main wood entries.

    :Attributes:
        :id (int): The primary key representing a unique sub-wood entry.
        :name (str): The name of the sub-wood.
        :length (float): The length of the sub-wood in millimeters.
        :width (float): The width of the sub-wood in millimeters.
        :height (float): The height of the sub-wood in millimeters.
        :density (float): The density of the sub-wood in grams per cubic centimeter.
        :color (str): The color of the sub-wood in RGB format (e.g., "255, 255, 255").
        :timestamp (str): A timestamp string representing when the sub-wood was created.
        :updated_at (str): A timestamp string representing when the sub-wood was last updated.
        :deleted_at (str): A timestamp string representing when the sub-wood was deleted.
        :source (str): Information about the source of the sub-wood.
        :info (str): Additional information about the sub-wood.
        :type (str): The type of wood (e.g., hardwood, softwood).
        :project_label (str): A label identifying the project the sub-wood is linked to.
        :deleted (bool): A flag indicating whether the sub-wood has been deleted.
        :deleted_by (str): The user who marked the sub-wood as deleted.
        :wood_id (int): A foreign key linking the sub-wood entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
        :design_id (int): A foreign key linking the sub-wood entry to a specific design requirement.
        :requirements (relationship): A relationship linking to the associated `DesignRequirementsModelFromClient` entry.
        :production (relationship): A relationship linking to the associated `ProductionModel` entry.
    """
    
    __tablename__ = "sub_wood"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80))

    # Units in mm
    length = db.Column(db.Float(precision=2))
    width = db.Column(db.Float(precision=2))
    height = db.Column(db.Float(precision=2))
    # Unit in g/cm3
    density = db.Column(db.Float(precision=2))
    # (RGB) formatted as string (255, 255, 255)
    color = db.Column(db.String(80))
    # Datetime string formatted as YYYY-MM-DD HH:MM:SS
    timestamp = db.Column(db.String)
    updated_at = db.Column(db.String)
    deleted_at = db.Column(db.String)
    source = db.Column(db.String(256))
    info = db.Column(db.String(256))
    # Wood type such as hardwood or softwood
    type = db.Column(db.String)
    project_label = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)

    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
    wood = db.relationship("WoodModel", back_populates="sub_wood")

    design_id = db.Column(db.Integer, db.ForeignKey('requirements.id'))
    requirements = db.relationship(
        "DesignRequirementsModelFromClient", back_populates="sub_wood")

    production = db.relationship("ProductionModel", back_populates="sub_wood")
    