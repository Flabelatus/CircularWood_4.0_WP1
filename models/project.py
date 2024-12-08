from db import db
from models.interface_model import DataModelInterface
from datetime import datetime

class ProjectModel(db.Model, DataModelInterface):
    """
    Represents a project with associated metadata and counts of design geometries and parts.

    :Attributes:
        :id (int): The primary key representing a unique project entry.
        :name (str): The name of the project.
        :created_at (datetime): The timestamp when the project was created.
        :client (str): The client associated with the project.
        :design_geometry_count (int): The count of design geometries as a sub module within the project.
        :parts_count (int): The count of parts in the sub module design geometry.
    """
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String)
    client = db.Column(db.String)
    design_geometry_count = db.Column(db.Integer, default=0)
    parts_count = db.Column(db.Integer, default=0)

    requirements = db.relationship(
        "DesignRequirementsModelFromClient",
        back_populates="project", 
    )

    design_geometries = db.relationship(
        "DesignGeometryModel", 
        back_populates='project', 
        cascade="all, delete-orphan"
    )

    @property
    def partials(self):
        partials = (
            [
                "id",
                "created_at",
            ],
        )
        return self._get_status_fields(partials[0])