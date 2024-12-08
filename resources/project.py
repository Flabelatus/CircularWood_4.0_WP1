from time import time
from typing import List, Union

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ProjectModel
from schema import PlainProjectSchema

project_blp = Blueprint(
    'Project table',
    'projects',
    description='Operations on the project resource'
)


@project_blp.route("/projects")
class Projects(MethodView):
    """
    Resource for managing all projects.
    """

    @project_blp.response(200, PlainProjectSchema(many=True))
    def get(self) -> List[ProjectModel]:
        """
        Retrieve all projects from the database.

        :return: A list of all projects.
        :rtype: List[ProjectModel]
        """
        return ProjectModel.query.all()

    @project_blp.arguments(PlainProjectSchema)
    @project_blp.response(201, PlainProjectSchema)
    def post(self, parsed_data: dict) -> Union[ProjectModel, None]:
        """
        Create a new project entry in the database.

        :param parsed_data: The data for creating a new project, validated by ProjectSchema.
        :type parsed_data: dict
        :return: The newly created project.
        :rtype: ProjectModel
        :raises HTTPException: If there is a database error.
        """
        project = ProjectModel(**parsed_data)
        project.created_at = project.created_at or int(time())

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, exc=err, message="Error creating a new project entry")

        return project


@project_blp.route("/projects/<int:project_id>")
class ProjectByID(MethodView):
    """
    Resource for managing a single project by its ID.
    """

    @project_blp.response(200, PlainProjectSchema)
    def get(self, project_id: int) -> ProjectModel:
        """
        Retrieve a project by its unique ID.

        :param project_id: The unique ID of the project.
        :type project_id: int
        :return: The project with the specified ID.
        :rtype: ProjectModel
        :raises HTTPException: If the project is not found.
        """
        project = ProjectModel.query.get_or_404(project_id)
        return project

    @jwt_required()
    @project_blp.response(200)
    def delete(self, project_id: int) -> dict:
        """
        Delete a project by its unique ID.

        :param project_id: The unique ID of the project to delete.
        :type project_id: int
        :return: A message indicating successful deletion.
        :rtype: dict
        :raises HTTPException: If the project is not found.
        """
        project = ProjectModel.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {
            "message": "Project deleted from database."
        }

    @jwt_required()
    @project_blp.arguments(PlainProjectSchema)
    @project_blp.response(200, PlainProjectSchema)
    def patch(self, parsed_data: dict, project_id: int) -> ProjectModel:
        """
        Update an existing project by its unique ID.

        :param parsed_data: The data for updating the project, validated by ProjectSchema.
        :type parsed_data: dict
        :param project_id: The unique ID of the project to update.
        :type project_id: int
        :return: The updated project.
        :rtype: ProjectModel
        :raises HTTPException: If the project is not found.
        """
        project = ProjectModel.query.get_or_404(project_id)
        if project:
            project.name = parsed_data.get("name", project.name)
            project.client = parsed_data.get("client", project.client)
            project.design_geometry_count = parsed_data.get("design_geometry_count", project.design_geometry_count)
            project.parts_count = parsed_data.get("parts_count", project.parts_count)
        db.session.add(project)
        db.session.commit()

        return project