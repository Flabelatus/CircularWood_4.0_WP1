from db import db


class ResidualWoodModel(db.Model):
    __tablename__ = 'residual_wood'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80))
    # intake_id = db.Column(db.Integer)
    length = db.Column(db.Float(precision=2), nullable=False)
    width = db.Column(db.Float(precision=2), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    weight = db.Column(db.Float(precision=2), nullable=False)
    density = db.Column(db.Float(precision=2), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    reserved = db.Column(db.Boolean, default=False)
    reservation_name = db.Column(db.String(80))
    reservation_time = db.Column(db.String(80))
    source = db.Column(db.String(256))
    price = db.Column(db.Float(precision=2))
    info = db.Column(db.String(256))
    type = db.Column(db.String)
    image = db.Column(db.String)

    wood_species = db.Column(db.String)
    label = db.Column(db.String)
    paint = db.Column(db.String)
    project_type = db.Column(db.String)
    is_fire_treated = db.Column(db.Boolean, default=False)
    is_straight = db.Column(db.Boolean, default=True)
    is_planed = db.Column(db.Boolean, default=True)

    tags = db.relationship("TagModel", back_populates="woods", secondary="woods_tags")

    requirements = db.relationship(
        "DesignRequirementsModelFromClient",
        back_populates="woods",
        secondary="woods_requirements"
    )


class WasteWoodModel(db.Model):
    __tablename__ = 'waste_wood'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    length = db.Column(db.Float(precision=2), nullable=False)
    width = db.Column(db.Float(precision=2), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    weight = db.Column(db.Float(precision=2), nullable=False)
    density = db.Column(db.Float(precision=2), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    damaged = db.Column(db.Boolean, nullable=False)
    stained = db.Column(db.Boolean, nullable=False)
    contains_metal = db.Column(db.Boolean, nullable=False, default=False)
    reserved = db.Column(db.Boolean, default=False)
    reservation_name = db.Column(db.String(80))
    reservation_time = db.Column(db.String(80))
    source = db.Column(db.String(256))
    price = db.Column(db.Float(precision=2))
    info = db.Column(db.String(256))
    type = db.Column(db.String)
