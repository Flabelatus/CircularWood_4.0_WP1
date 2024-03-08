import json
from os import path
from db import db


class ImpactModel(db.Model):
    __tablename__ = "idemat"

    id = db.Column(db.Integer, primary_key=True)
    carbon_footprint = db.Column(db.String(80))
    codename = db.Column(db.String(80))
    eco_costs = db.Column(db.String(80))
    process = db.Column(db.String(80))
    eco_toxicity = db.Column(db.String(80))
    footprint = db.Column(db.String(80))
    resource_depletion = db.Column(db.String(80))
    human_health = db.Column(db.String(80))
    material = db.Column(db.String(80))

    wood = db.relationship("WoodModel", back_populates='impact')
    wood_id = db.Column(db.Integer, db.ForeignKey('wood.id'))
