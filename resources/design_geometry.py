from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignGeometryModel
from schema import PlainDesignGeometrySchema

design_geometry_blp = Blueprint(
    'Design Geometries',
    'design_geometries',
    description='Operations on design geometry resources'
)


@design_geometry_blp.route("/design_geometries")
class DesignGeometries(MethodView):
    """
    Resource for managing all design geometries.
    """

    @design_geometry_blp.response(200, PlainDesignGeometrySchema(many=True))
    def get(self):
        """
        Retrieve all design geometries.

        :return: A list of all design geometries.
        :rtype: List[DesignGeometryModel]
        """
        return DesignGeometryModel.query.all()

    @design_geometry_blp.arguments(PlainDesignGeometrySchema)
    @design_geometry_blp.response(201, PlainDesignGeometrySchema)
    def post(self, parsed_data):
        """
        Create a new design geometry entry.

        :param parsed_data: The data for creating a new design geometry, validated by DesignGeometrySchema.
        :type parsed_data: dict
        :return: The newly created design geometry.
        :rtype: DesignGeometryModel
        :raises HTTPException: If there is a database error.
        """
        geometry = DesignGeometryModel(**parsed_data)
        try:
            db.session.add(geometry)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, exc=err, message="Error creating a new design geometry entry")
        return geometry


@design_geometry_blp.route("/design_geometries/<int:geometry_id>")
class DesignGeometryByID(MethodView):
    """
    Resource for managing a single design geometry by its ID.
    """

    @design_geometry_blp.response(200, PlainDesignGeometrySchema)
    def get(self, geometry_id: int):
        """
        Retrieve a design geometry by its unique ID.

        :param geometry_id: The unique ID of the design geometry.
        :type geometry_id: int
        :return: The design geometry with the specified ID.
        :rtype: DesignGeometryModel
        :raises HTTPException: If the design geometry is not found.
        """
        return DesignGeometryModel.query.get_or_404(geometry_id)

    @jwt_required()
    @design_geometry_blp.response(200)
    def delete(self, geometry_id: int):
        """
        Delete a design geometry by its unique ID.

        :param geometry_id: The unique ID of the design geometry to delete.
        :type geometry_id: int
        :return: A message indicating successful deletion.
        :rtype: dict
        :raises HTTPException: If the design geometry is not found.
        """
        geometry = DesignGeometryModel.query.get_or_404(geometry_id)
        db.session.delete(geometry)
        db.session.commit()
        return {"message": "Design geometry deleted from database."}

    @jwt_required()
    @design_geometry_blp.arguments(PlainDesignGeometrySchema)
    @design_geometry_blp.response(200, PlainDesignGeometrySchema)
    def patch(self, parsed_data, geometry_id):
        """
        Update an existing design geometry by its unique ID.

        :param parsed_data: The data for updating the design geometry, validated by DesignGeometrySchema.
        :type parsed_data: dict
        :param geometry_id: The unique ID of the design geometry to update.
        :type geometry_id: int
        :return: The updated design geometry.
        :rtype: DesignGeometryModel
        :raises HTTPException: If the design geometry is not found.
        """
        geometry = DesignGeometryModel.query.get_or_404(geometry_id)
        if geometry:
            geometry.name = parsed_data.get("name", geometry.name)
            geometry.type = parsed_data.get("type", geometry.type)
            geometry.file_path = parsed_data.get("file_path", geometry.file_path)
            geometry.project_id = parsed_data.get("project_id", geometry.project_id)
        db.session.add(geometry)
        db.session.commit()
        return geometry


@design_geometry_blp.route("/design_geometries/project/<int:project_id>")
class DesignGeometriesByProjectID(MethodView):
    """
    Resource for managing design geometries associated with a specific project.
    """

    @design_geometry_blp.response(200, PlainDesignGeometrySchema(many=True))
    def get(self, project_id: int):
        """
        Retrieve all design geometries associated with a specific project ID.

        :param project_id: The unique ID of the project.
        :type project_id: int
        :return: A list of design geometries associated with the given project.
        :rtype: List[DesignGeometryModel]
        :raises HTTPException: If no design geometries are found for the given project ID.
        """
        geometries = DesignGeometryModel.query.filter_by(project_id=project_id).all()
        if not geometries:
            abort(404, message=f"No design geometries found for project ID {project_id}")
        return geometries