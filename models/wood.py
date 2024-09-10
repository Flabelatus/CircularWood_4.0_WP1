from sqlalchemy.orm import RelationshipProperty

from db import db


class WoodModel(db.Model):
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
            attr_value = getattr(self, attr_name)
            if isinstance(
                self.__mapper__.get_property(attr_name),
                RelationshipProperty,
            ):
                relationship_fields.append(attr_name)
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
        return self._get_status_fields(partials)

    def _get_status_fields(self, status_fields):
        return {
            field: getattr(self, field)
            for field in status_fields
            if hasattr(self, field)
        }
