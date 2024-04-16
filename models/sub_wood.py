from db import db


class SubWoodModel(db.Model):
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
    