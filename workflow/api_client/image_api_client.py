import os
import requests
from collections import namedtuple
from os.path import dirname, abspath
import logging
from workflow.api_client import logger, get_default_params

logger.getChild("image_upload")

default_params = get_default_params()


class ImageApiClient:
    """
    To use the image upload endpoint you need to specify the ID of the wood
    as the file name, also you need to set the 'dir' parameter in the request url which indicates what directory the image will be saved in.

    For the directory to save the image in make a choice from the folders depending on your application. The options are:

        0. wood_intake: creates a folder for the images taken from the wood by the  camera (RGB images)
        1. depth_png: creates a folder for the PNG images from Triscpector
        2. metal_region: creates a folder for the visualization from the metal induction gate
    """

    def __init__(self, params=default_params, destination=0, development=False):
        self.params = default_params
        self.destination = destination
        self.dir = (
            f"{input('Directory name: ')}-{self.params.dir[self.destination]}"
            if development is True
            else self.params.dir[self.destination]
        )
        self.base_url = self.params.base_url['url']

    def upload(self, filepath, wood_id):
        auth_endpoint = "/login"
        endpoint = "/image/upload/"
        login_response = requests.post(
            f"{self.base_url}{auth_endpoint}", json=self.params.credentials
        )

        login_response_json = login_response.json()
        token = login_response_json.get("access_token", "")

        if not login_response.status_code == 200:
            logger.error(login_response_json)
            return {
                "error": True,
                "message": f"Error authenticating: {login_response.json()}",
            }

        try:
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return {"error": True, "message": f"File not found: {filepath}"}

            with open(filepath, "rb") as f:
                files = {"image": (filepath, f)}
                url = f"{self.base_url}{endpoint}{str(wood_id)}?dir={self.dir}"
                response = requests.post(url, files=files)
                if not response.status_code == 201:
                    logger.error(response.json())
                return response.json()

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return {"error": True, "message": str(e)}

    def delete_image(self, wood_id):
        auth_endpoint = "/login"
        image_endpoint = "/image/"

        login_response = requests.post(
            f"{self.base_url}{auth_endpoint}", json=self.params.credentials
        )

        login_response_json = login_response.json()
        token = login_response_json.get("access_token", "")

        if not login_response.status_code == 200:
            logger.error(login_response_json)

        logger.debug(login_response_json)

        url = f"{self.base_url}{image_endpoint}{str(wood_id)}?dir={self.dir}"
        response = requests.delete(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        logger.debug(response.json())
