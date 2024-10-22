from db import db

from models.interface_model import DataModelInterface


class ImpactModel(db.Model, DataModelInterface):
    """
    Represents the environmental impact information for specific wood entries.

    :Attributes:
        :id (int): The primary key representing a unique impact entry.
        :carbon_footprint (str): The carbon footprint value associated with the wood material.
        :codename (str): A codename for the material or process.
        :eco_costs (str): The ecological costs of using the material or process.
        :process (str): The type of process used to obtain or treat the material.
        :eco_toxicity (str): The ecological toxicity of the material.
        :footprint (str): The overall environmental footprint of the material.
        :resource_depletion (str): The extent to which resources are depleted in the process.
        :human_health (str): The impact on human health due to the material or process.
        :material (str): The name of the material.
        :wood_id (int): A foreign key linking the impact entry to a specific wood entry.
        :wood (relationship): A relationship linking to the associated `WoodModel` entry.
    """
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

    @property
    def partials(self):
        partials = (
            [
                "id",
            ],
        )
        return self._get_status_fields(partials[0])
