from db import db
from models.interface_model import DataModelInterface

class DesignGeometryModel(db.Model, DataModelInterface):
    """
    Represents a design geometry associated with a project.

    :Attributes:
        :id (int): The primary key representing a unique design geometry entry.
        :name (str): The name of the design geometry.
        :created_at (str): The timestamp when the design geometry was created.
        :project_id (int): A foreign key linking the design geometry to a specific project.
        :project (relationship): A relationship linking to the associated `ProjectModel` entry.
        :type (str): The type of geometry (e.g., OBJ, STP).
        :file_path (str): Path to the file containing the design geometry.
    """
    __tablename__ = "design_geometries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship("ProjectModel", back_populates='design_geometries')

    requirements = db.relationship("DesignRequirementsModelFromClient", back_populates='design_geometries', lazy='dynamic')

    @property
    def partials(self):
        partials = (
            [
                "id",
                "created_at",
            ],
        )
        return self._get_status_fields(partials[0])