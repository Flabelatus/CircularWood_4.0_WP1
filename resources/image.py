import os
import traceback

from flask import request, send_file, jsonify
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from schema import ImageSchema
from utils.image_helpers import save_image, get_basename, is_filename_safe, get_path

image_blueprint = Blueprint(
    "Image Upload", 'images', description="Operations on image upload endpoint")
image_schema = ImageSchema()


@image_blueprint.route("/image/upload/<int:wood_id>")
class ImageUpload(MethodView):
    @image_blueprint.response(201)
    def post(self, wood_id):
        folder = request.args.get('dir')
        if 'image' in request.files:
            try:
                image_data = image_schema.load(request.files)
                # folder = "wood_intake"
                filename = f'{wood_id}.png'
                image_path = save_image(
                    image_data["image"], folder=folder, name=filename)
                basename = get_basename(image_path)

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

    @image_blueprint.response(200)
    def get(self, wood_id):

        folder = request.args.get("dir")
        filename = f'{str(wood_id)}.png'

        if not is_filename_safe(filename):
            abort(400, message="image illegal file name")

        try:
            return send_file(get_path(filename=filename, folder=folder))

        except FileNotFoundError as e:
            abort(404, message='image not found')

    @jwt_required()
    def delete(self, wood_id):
        folder = request.args.get("dir")
        filename = f'{str(wood_id)}.png'

        if not is_filename_safe(filename):
            abort(400, message="image illegal file name")

        try:
            os.remove(get_path(filename=filename, folder=folder))
            return jsonify({
                "message": "image successfully removed"
            }), 200
        except FileNotFoundError as e:
            abort(404, message='image not found')
        except:
            traceback.print_exc()
            abort(
                500, message="something went wrong while deleting the image - contact support"
            )
