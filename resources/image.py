"""_summary_

"""

import os
import traceback

from flask import request, send_file, jsonify
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_uploads import UploadNotAllowed
from schema import ImageSchema
from utils.file_upload_helpers import FileUploadHandler

image_blueprint = Blueprint(
    "Image Upload", 'images', description="Operations on image upload endpoint")
image_schema = ImageSchema()

img_uploader = FileUploadHandler()
img_uploader.file_type = 'IMAGES'


@image_blueprint.route("/image/upload/<int:wood_id>")
class ImageUpload(MethodView):
    """
    Upload an image associated with a specific wood item.
    """

    @image_blueprint.response(201)
    def post(self, wood_id: int):
        """
        Upload an image for the specified wood ID. The image is saved to the specified folder
        with the name formatted as '{wood_id}.png'.

        :param wood_id: ID of the wood item.
        :return: A message indicating whether the image upload was successful.
        """
        folder = request.args.get('dir')
        if 'image' in request.files:
            try:
                image_data = image_schema.load(request.files)
                filename = f'{wood_id}.png'
                image_path = img_uploader.save_file(
                    image_data["image"], folder=folder, name=filename)
                basename = img_uploader.get_basename(image_path)

                return {
                    'error': False,
                    'message': f'image successfully uploaded - {basename}'
                }

            except UploadNotAllowed as e:
                abort(400, message=str(e))
        else:
            abort(400, message="no file selected")


@image_blueprint.route("/image/<int:wood_id>")
class ImageByWoodID(MethodView):
    """
    Handle image operations for a specific wood item by its ID.
    """

    @image_blueprint.response(200)
    def get(self, wood_id: int):
        """
        Retrieve an image associated with a specific wood item by its ID.

        :param wood_id: ID of the wood item.
        :return: The image file if it exists.
        """
        folder = request.args.get("dir")
        filename = f'{str(wood_id)}.png'

        if not img_uploader.is_filename_safe(filename):
            abort(400, message="image illegal file name")

        try:
            return send_file(img_uploader.get_path(filename=filename, folder=folder))
        except FileNotFoundError as e:
            abort(404, message='image not found')

    @jwt_required()
    def delete(self, wood_id: int):
        """
        Delete an image associated with a specific wood item by its ID.

        :param wood_id: ID of the wood item.
        :return: A message confirming the deletion of the image or an error message if not found.
        """
        folder = request.args.get("dir")
        filename = f'{str(wood_id)}.png'

        if not img_uploader.is_filename_safe(filename):
            abort(400, message="image illegal file name")

        try:
            os.remove(img_uploader.get_path(filename=filename, folder=folder))
            return jsonify({
                "message": "image successfully removed"
            }), 200
        except FileNotFoundError as e:
            abort(404, message='image not found')
        except:
            traceback.print_exc()
            abort(500, message="something went wrong while deleting the image - contact support")