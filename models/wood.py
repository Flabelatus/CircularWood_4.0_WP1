from sqlalchemy.orm import RelationshipProperty
from settings import logger
from db import db


class WoodModel(db.Model):
    """
    Represents a wood entry in the system, including its physical properties and related data.

    :Attributes:
        :id (int): The primary key representing a unique wood entry.
        :name (str): The name of the wood species (e.g., Red oak).
        :length (float): The length of the wood in millimeters.
        :width (float): The width of the wood in millimeters.
        :height (float): The height of the wood in millimeters.
        :weight (float): The weight of the wood in grams.
        :density (float): The density of the wood in grams per cubic centimeter.
        :color (str): The RGB color of the wood (formatted as "255, 255, 255").
        :source (str): Information about the source of the wood.
        :info (str): Additional information about the wood.
        :type (str): The type of wood (e.g., hardwood or softwood).
        :image (str): The path to the image of the wood.
        :paint (str): The paint type on the wood, if applicable.
        :is_fire_treated (bool): A flag indicating whether the wood is fire treated.
        :is_straight (bool): A flag indicating whether the wood is straight.
        :is_planed (bool): A flag indicating whether the wood is planed.
        :has_metal (bool): A flag indicating whether the wood contains metal.
        :intake_id (int): The ID representing the wood intake.
        :storage_location (str): The location where the wood is stored.
        :metal_bbox_coords (str): The bounding box coordinates for any metal detected in the wood.
        :timestamp (str): The timestamp when the wood was created.
        :updated_at (str): The timestamp when the wood was last updated.
        :reserved (bool): A flag indicating whether the wood is reserved.
        :reservation_name (str): The name of the person or entity that reserved the wood.
        :reservation_time (str): The time when the wood was reserved.
        :used (bool): A flag indicating whether the wood has been used.
        :used_by (str): The name of the person or entity that used the wood.
        :deleted (bool): A flag indicating whether the wood has been deleted.
        :deleted_by (str): The name of the person or entity that marked the wood as deleted.
        :deleted_at (str): The timestamp when the wood was deleted.

        :tags (relationship): A many-to-many relationship linking to the `TagModel` table through the `woods_tags` table.
        :requirements (relationship): A many-to-many relationship linking to the `DesignRequirementsModelFromClient` table 
            through the `woods_requirements` table.
        :production (relationship): A one-to-many relationship linking to the `ProductionModel` table.
        :history (relationship): A dynamic one-to-many relationship linking to the `HistoryModel` table.
        :pointcloud (relationship): A dynamic one-to-many relationship linking to the `PointCloudModel` table.
        :impact (relationship): A one-to-many relationship linking to the `ImpactModel` table.
        :sub_wood (relationship): A dynamic one-to-many relationship linking to the `SubWoodModel` table.
    """
        
    __tablename__ = "wood"

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    # Name of wood species such as Red oak
    name = db.Column(db.String(80))

    # Units in mm
    length = db.Column(db.Float(precision=2))
    width = db.Column(db.Float(precision=2))
    height = db.Column(db.Float(precision=2))

    # Unit in grams
    weight = db.Column(db.Float(precision=2))
    # Unit in g/cm3
    density = db.Column(db.Float(precision=2))

    # (RGB) formatted as string (255, 255, 255)
    color = db.Column(db.String(80))
    source = db.Column(db.String(256))
    # price = db.Column(db.Float(precision=2))
    info = db.Column(db.String(256))

    # Wood type such as hardwood or softwood
    type = db.Column(db.String)
    image = db.Column(db.String)

    # Only in case of Derako wood
    # project_label = db.Column(db.String)
    # project_type = db.Column(db.String)

    # In case of waste wood
    paint = db.Column(db.String)
    is_fire_treated = db.Column(db.Boolean)
    is_straight = db.Column(db.Boolean)
    is_planed = db.Column(db.Boolean)
    has_metal = db.Column(db.Boolean)
    intake_id = db.Column(db.Integer)
    storage_location = db.Column(db.String)
    metal_bbox_coords = db.Column(db.String)

    # Information regarding the use of material that needs to be added to partials for regular row data modification
    timestamp = db.Column(db.String)
    updated_at = db.Column(db.String)
    reserved = db.Column(db.Boolean, default=False)
    reservation_name = db.Column(db.String(80))
    reservation_time = db.Column(db.String)
    used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.String)

    # Relationships
    tags = db.relationship("TagModel", back_populates="woods", secondary="woods_tags")
    requirements = db.relationship(
        "DesignRequirementsModelFromClient",
        back_populates="woods",
        secondary="woods_requirements",
    )
    production = db.relationship("ProductionModel")
    history = db.relationship("HistoryModel", back_populates="wood", lazy="dynamic")
    pointcloud = db.relationship(
        "PointCloudModel", back_populates="wood", lazy="dynamic"
    )
    impact = db.relationship("ImpactModel", back_populates="wood", lazy="dynamic")
    sub_wood = db.relationship("SubWoodModel", back_populates="wood", lazy="dynamic")

    def relationship_fields(self):
        """
        Collects all relationship fields of the model and returns them as a list called 'partials'.
        """
        relationship_fields = []
        attr_names = dir(self)
        for attr_name in attr_names:
            if attr_name.startswith("_") or attr_name.endswith("_"):
                continue
            if attr_name == 'metadata':
                continue
            if isinstance(
                getattr(self, attr_name),
                RelationshipProperty,
            ):
                relationship_fields.append(attr_name)
        logger.info(relationship_fields)
        return relationship_fields

    def wood_partials(self):
        partials = (
            [
                "id",
                "timestamp",
                "updated_at",
                "reservation_time",
                "reserved",
                "reservation_name",
                "used",
                "used_by",
                "deleted_by",
                "deleted_at",
                "deleted",
            ],
        )
        return self._get_status_fields(partials[0])

    def _get_status_fields(self, status_fields):
        return {
            field: getattr(self, field)
            for field in status_fields
            if hasattr(self, field)
        }
