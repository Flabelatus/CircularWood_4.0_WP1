from db import db


class WoodModel(db.Model):
    __tablename__ = 'wood'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    current_id = db.Column(db.Integer)
    subsequent_id = db.Column(db.String)

    name = db.Column(db.String(80))

    length = db.Column(db.Float(precision=2))
    width = db.Column(db.Float(precision=2))
    height = db.Column(db.Float(precision=2))
    weight = db.Column(db.Float(precision=2))
    density = db.Column(db.Float(precision=2))
    color = db.Column(db.String(80))

    timestamp = db.Column(db.String)
    updated_at = db.Column(db.String)

    reserved = db.Column(db.Boolean, default=False)
    reservation_name = db.Column(db.String(80))
    reservation_time = db.Column(db.String(80))

    source = db.Column(db.String(256))
    price = db.Column(db.Float(precision=2))
    info = db.Column(db.String(256))
    type = db.Column(db.String)
    image = db.Column(db.String)
    project_label = db.Column(db.String)
    paint = db.Column(db.String)
    project_type = db.Column(db.String)
    is_fire_treated = db.Column(db.Boolean)
    is_straight = db.Column(db.Boolean)
    is_planed = db.Column(db.Boolean)

    used = db.Column(db.Boolean)

    has_metal = db.Column(db.Boolean)
    metal_bbox_coords = db.Column(db.String)  # 8 points as a string following format -> [(x, y, z), ..., (x, y, z)]

    intake_id = db.Column(db.Integer)
    storage_location = db.Column(db.String)

    tags = db.relationship("TagModel", back_populates="woods", secondary="woods_tags")

    requirements = db.relationship(
        "DesignRequirementsModelFromClient",
        back_populates="woods",
        secondary="woods_requirements"
    )

    production = db.relationship('ProductionModel')


