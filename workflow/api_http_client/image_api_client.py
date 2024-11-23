"""ImageApiClient summary ...

"""

import os
import requests
from workflow.api_http_client import logger
from workflow.api_http_client.api_client import DataServiceApiHTTPClient

logger.getChild("image_upload")


class ImageApiClient(DataServiceApiHTTPClient):
    """
    To use the image upload endpoint you need to specify the ID of the wood
    as the file name, also you need to set the 'dir' parameter in the request url which indicates what directory the image will be saved in.

    For the directory to save the image in make a choice from the folders depending on your application. The options are:

        0. wood_intake: creates a folder for the images taken from the wood by the  camera (RGB images)
        1. depth_png: creates a folder for the PNG images from Triscpector
        2. metal_region: creates a folder for the visualization from the metal induction gate
    """

    def __init__(self, destination=0, development=False):
        super().__init__()
        self.destination = destination
        self.dir = (
            f"{input('Directory name: ')}-{self.params.dir[self.destination]}"
            if development is True
            else self.params.dir[self.destination]
        )
        self.base_url = self.params.base_url

    def upload(self, filepath, wood_id):
        endpoint = "/image/upload/"       
        _ = self.authenticate()
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
        image_endpoint = "/image/"
        token = self.authenticate()

        url = f"{self.base_url}{image_endpoint}{str(wood_id)}?dir={self.dir}"
        response = requests.delete(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        logger.debug(response.json())
