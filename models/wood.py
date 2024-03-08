from db import db


class WoodModel(db.Model):
    __tablename__ = 'wood'

    id = db.Column(db.Integer, primary_key=True, nullable=False)  # 1
    current_id = db.Column(db.Integer)

    # Sub id following the current id 1-1 or 1-2 or ...
    subsequent_id = db.Column(db.String)

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

    # Datetime string formatted as YYYY-MM-DD HH:MM:SS
    timestamp = db.Column(db.String)
    updated_at = db.Column(db.String)
    reservation_time = db.Column(db.String)
    deleted_at = db.Column(db.String)

    source = db.Column(db.String(256))
    price = db.Column(db.Float(precision=2))
    info = db.Column(db.String(256))

    # Wood type such as hardwood or softwood
    type = db.Column(db.String)

    # URL to image
    image = db.Column(db.String)

    # Only in case of Derako wood
    project_label = db.Column(db.String)
    project_type = db.Column(db.String)

    # In case of waste wood
    paint = db.Column(db.String)
    is_fire_treated = db.Column(db.Boolean)
    is_straight = db.Column(db.Boolean)
    is_planed = db.Column(db.Boolean)
    has_metal = db.Column(db.Boolean)

    # 8 points as a string following format -> [(x, y, z), ..., (x, y, z)]
    metal_bbox_coords = db.Column(db.String)

    # Information regarding the use of material
    reserved = db.Column(db.Boolean, default=False)
    reservation_name = db.Column(db.String(80))
    used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)

    intake_id = db.Column(db.Integer)
    storage_location = db.Column(db.String)

    # Relationships
    tags = db.relationship(
        "TagModel", back_populates="woods", secondary="woods_tags")
    requirements = db.relationship(
        "DesignRequirementsModelFromClient",
        back_populates="woods",
        secondary="woods_requirements"
    )
    production = db.relationship('ProductionModel')
    history = db.relationship(
        "HistoryModel", back_populates="wood", lazy="dynamic")
    pointcloud = db.relationship(
        "PointCloudModel", back_populates="wood", lazy="dynamic")
    impact = db.relationship(
        "ImpactModel", back_populates="wood", lazy="dynamic")
