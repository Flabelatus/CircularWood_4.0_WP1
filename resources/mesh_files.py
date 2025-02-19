"""_summary_

"""

import os
import traceback

from time import time

from flask import request, send_file, jsonify
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_uploads import UploadNotAllowed

from schema import MeshSchema
from db import db
from utils.file_upload_helpers import FileUploadHandler
from models import DesignGeometryModel, ProjectModel, DesignRequirementsModelFromClient

mesh_blueprint = Blueprint(
    "Mesh File Upload", 'mesh', description="Operations on mesh file upload endpoint")
mesh_schema = MeshSchema()

mesh_uploader = FileUploadHandler()
mesh_uploader.file_type = 'MESH'


@mesh_blueprint.route("/mesh/design_geometry/upload/<int:project_id>")
class MeshDesignGeometryUpload(MethodView):
    """
    Upload a mesh file of the design geometry associated with a specific project. The design would be as a whole
    containing several parts
    """
    @mesh_blueprint.response(201)
    def post(self, project_id: int):
        """
        Upload a mesh for the specified project ID and save it as 
        <project_id>_<project_name>.<extension>
        """
        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="The provided mesh extension is not allowed")

        project_data = ProjectModel.query.filter(
            ProjectModel.id == project_id
        ).first()
        if not project_data:
            abort(404, message="The project not found")

        data = {
                "name": project_data.name,
                "created_at": int(time()),
                "project_id": project_id,
                "file_path": "",
                "type": extension,                
            }
        
        # Create the DesignGeometryModel instance
        design_geometry = DesignGeometryModel()
        design_geometry.name = data["name"]
        design_geometry.project_id = data["project_id"]
        design_geometry.type = data["type"]
        design_geometry.created_at = data["created_at"]
        
        # Add and commit
        db.session.add(design_geometry)
        db.session.commit()

        folder = os.path.join(f"{project_id}_{design_geometry.id}")
        filename = f"{project_data.id}_{design_geometry.id}_{project_data.name}.{extension}"

        design_geometry.file_path = os.path.join(".", "static", "design", folder, filename)

        if "mesh" in request.files:
            try:
                # Load and validate the mesh
                mesh_data = mesh_schema.load({"mesh": request.files["mesh"]})
                mesh_path = mesh_uploader.save_file(
                    mesh_data['mesh'], folder=folder, name=filename
                )
                basename = mesh_uploader.get_basename(mesh_path)

                # Update the file_path of the design geometry in the database
                db.session.commit()

                return {
                    "error": False,
                    "message": f"Mesh successfully uploaded - {basename}",
                }
            except UploadNotAllowed as e:
                abort(400, message=str(e))
        else:
            abort(400, message="No file selected")


@mesh_blueprint.route("/mesh/design_geometry/<int:design_geometry_id>")
class MeshDesignGeometryByDesignGeometryID(MethodView):
    """
    Handle mesh operations for a specific design_geometry item by its ID.
    """

    @mesh_blueprint.response(200)
    def get(self, design_geometry_id: int):
        """
        Retrieve a mesh associated with a specific design_geometry item by its ID.

        :param requirement_id: ID of the design_geometry item.
        :return: The mesh file if it exists.
        """
        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="the provided mesh extension is not allowed")
        
        design_geometry = DesignGeometryModel.query.get_or_404(design_geometry_id)
        path = design_geometry.file_path
        if path:
            try:
                return send_file(path)
            except FileNotFoundError as e:
                abort(404, message='mesh not found')
        else:
            abort(404, message='mesh with the specified path does not exist')

    @jwt_required()
    def delete(self, design_geometry_id: int):
        """
        Delete a mesh associated with a specific design geometry item by its ID.

        :param design_geometry_id: ID of the design geometry item.
        :return: A message confirming the deletion of the mesh or an error message if not found.
        """
        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="the provided mesh extension is not allowed")
        
        design_geometry = DesignGeometryModel.query.get_or_404(design_geometry_id)
        path = design_geometry.file_path
        if path:
            try:
                os.remove(path)
                design_geometry.file_path = ""
                db.session.add(design_geometry)
                db.session.commit()
                return jsonify({
                    "message": "mesh successfully removed"
                }), 200
            except FileNotFoundError as e:
                abort(404, message='mesh not found')
            except:
                traceback.print_exc()
                abort(500, message="something went wrong while deleting the mesh file - contact support")
        else:
            abort(404, message='mesh with the specified path does not exist')
 

@mesh_blueprint.route("/mesh/part/upload/<int:requirement_id>")
class MeshPartUpload(MethodView):
    """
    Upload a mesh associated with a specific design requirement item.
    """
    
    @mesh_blueprint.response(201)
    def post(self, requirement_id: int):
        """
        Upload a mesh for the specified requirement ID and save it as 
        <project_id>_<requirement_id>.<extension>
        """
        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="The provided mesh extension is not allowed")

        design_metadata = DesignRequirementsModelFromClient.query.filter(
            DesignRequirementsModelFromClient.id == requirement_id
        ).first()
        if not design_metadata:
            abort(404, message="The design metadata not found")

        # Retrieve the project data
        project_id = design_metadata.project_id
        design_geometry_id = design_metadata.design_geometry_id
        design_geo = DesignGeometryModel.query.get_or_404(design_geometry_id)
        project = ProjectModel.query.filter(ProjectModel.id == project_id).first()
        project_name = project.name if project else "Unknown"

        # Create the dest for saving the file
        folder = os.path.join(f"{project_id}_{design_geometry_id}", "parts")
        filename = f"{project_name}_{requirement_id}.{extension}"

        if "mesh" in request.files:
            try:
                # Load and validate the mesh
                mesh_data = mesh_schema.load({"mesh": request.files["mesh"]})
                mesh_path = mesh_uploader.save_file(
                    mesh_data['mesh'], folder=folder, name=filename
                )
                basename = mesh_uploader.get_basename(mesh_path)

                # Update metadata and design geometry table data
                design_metadata.part_file_path = mesh_path
                design_geo.type = extension

                db.session.add(design_metadata)
                db.session.commit()

                return {
                    "error": False,
                    "message": f"Mesh successfully uploaded - {basename}",
                }
            except UploadNotAllowed as e:
                abort(400, message=str(e))
        else:
            abort(400, message="No file selected")


@mesh_blueprint.route("/mesh/part/<int:requirement_id>")
class MeshPartByRequirementID(MethodView):
    """
    Handle mesh operations for a specific design requirement item by its ID.
    """

    @mesh_blueprint.response(200)
    def get(self, requirement_id: int):
        """
        Retrieve a mesh associated with a specific design requirement item by its ID.

        :param requirement_id: ID of the design requirement item.
        :return: The mesh file if it exists.
        """

        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="the provided mesh extension is not allowed")

        design_metadata = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        path = os.path.join(".", "static", "design", design_metadata.part_file_path)
        if path:
            try:
                return send_file(path)
            except FileNotFoundError as e:
                abort(404, message='mesh not found')
        else:
            abort(404, message='mesh with the specified path does not exist')

    @jwt_required()
    def delete(self, requirement_id: int):
        """
        Delete a mesh associated with a specific design requirement item by its ID.

        :param requirement_id: ID of the design requirement item.
        :return: A message confirming the deletion of the mesh or an error message if not found.
        """

        extension = request.args.get("ext")
        if extension not in mesh_uploader.extensions['MESH']:
            abort(400, message="the provided mesh extension is not allowed")

        design_metadata = DesignRequirementsModelFromClient.query.get_or_404(requirement_id)
        path = os.path.join(".", "static", "design", design_metadata.part_file_path)
        if path:
            try:
                os.remove(path)
                # Update the file path to the part to empty string
                design_metadata.part_file_path = ""
                db.session.add(design_metadata)
                db.session.commit()
                return jsonify({
                    "message": "mesh successfully removed"
                }), 200
            except FileNotFoundError as e:
                abort(404, message='mesh not found')
            except:
                traceback.print_exc()
                abort(500, message="something went wrong while deleting the mesh file - contact support")
        else:
            abort(404, message='mesh with the specified path does not exist')
