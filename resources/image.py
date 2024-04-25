from typing import Union, List, Dict
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from utils import image_helper
from schema import ImageSchema


img_blp = Blueprint("Image uploads", "images", description="Operations on image upload resources")


@img_blp.route("/image/upload/<int:wood_id>")
class ImageUpload(MethodView): 
   
    @img_blp.arguments(ImageSchema)
    @img_blp.response(201, ImageSchema)
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        image_schema = ImageSchemad()
        data = image_schema.load(request.files)
    
        folder = f"wood_{wood_id}"
        try:
            # save(self, storage, folder=None, name=None)
            image_path = image_helper.save_image(data["image"], folder=folder)
            # here we only return the basename of the image and hide the internal folder structure from our user
            basename = image_helper.get_basename(image_path)
            return {"message": "image successfully uploaded"}
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            abort(400, message="image_illegal_extension")


@img_blp.route("/image/<int:wood_id>")
class Image(MethodView):
    @img_blp.response(200, ImageSchema)
    def get(self, wood_id: int):
        """
        This endpoint returns the requested image if exists.
        """
        filename = str(wood_id)
        folder = f"wood_{wood_id}"
        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            abort(400, message='image_illegal_file_name')
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            abort(404, message="image_not_found")

    @jwt_required()
    def delete(self, wood_id: int):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to authenticate as it is a sensetive action.
        """
        user_id = get_jwt_identity()
        filename = str(wood_id)
        folder = f"wood_{wood_id}"

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            abort(400, message='image_illegal_file_name')

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": "image successfully deleted"}, 200
        except FileNotFoundError:
            abort(404, message="image_not_found")
        except:
            traceback.print_exc()
            abort(500, message="image delete failed")
