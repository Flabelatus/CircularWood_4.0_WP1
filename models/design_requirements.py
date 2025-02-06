from db import db

from models.interface_model import DataModelInterface


class DesignRequirementsModelFromClient(db.Model, DataModelInterface):
    """
    Represents the metadata of a single part, phrased as design requirements. This is submitted from design client after
    all parts are matched with the material resources.

    :Attributes:
        :id (int): The primary key representing a unique design requirement entry.
        :part_name (str): A string representing the part of the design the requirement applies to.
        :part_file_path (str): A string representing specific part_file_path requested in the design.
        :tag (str): A string tag used to categorize or identify the design requirement.
        :part (int): An integer representing the part type or index of the design.
        :created_at (str): A timestamp string representing when the design requirement was created.
        :project_id (str): A string representing the ID of the project the requirement belongs to.
        :design_geometry_id (int): An integer representing the ID of the associated design geometry entry.
        :wood_id (int): An integer representing the ID of the associated wood entry.
        
        :woods (relationship): A many-to-many relationship linking to the `WoodModel` table 
            through the `woods_requirements` table. This represents the wood materials 
            associated with the design requirement.
        
        :sub_wood (relationship): A dynamic relationship linking to the `SubWoodModel` table. 
            This represents the sub-wood components linked to the design requirement.
        
        :project (relationship) A dynamic relationship linking to the `ProjectModel`
            This represents the project which this individual part from the designed product 
            is linked to.

        :design_geometry (relationship) A dynamic relationship linking to the `DesignGeometryModel`
            This represents the 3d geometry of the design which this individual part from that design 
            is linked to.
    """
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String)
    part_file_path = db.Column(db.String)
    tag = db.Column(db.String(80))
    part = db.Column(db.String(80))
    created_at = db.Column(db.String)
    wood_id = db.Column(db.Integer)

    woods = db.relationship(
        "WoodModel", back_populates='requirements', secondary='woods_requirements')
    sub_wood = db.relationship(
        "SubWoodModel", back_populates='requirements', lazy="dynamic")
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship("ProjectModel", back_populates='requirements')

    design_geometry_id = db.Column(db.Integer, db.ForeignKey('design_geometries.id'))
    design_geometries = db.relationship("DesignGeometryModel", back_populates='requirements')

    @property
    def partials(self):
        partials = (
            [
                "id",
                "created_at",
                "status"
            ],
        )

        return self._get_status_fields(partials[0])
