"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import logger
from workflow.api_client import image_api_client

if __name__ == "__main__":

    wood_id = input("Enter the wood ID: ")
    filepath = input("Enter the path to the image: ")

    logger.getChild("scripts.image").debug("Uploading {0} ...".format(filepath))

    image_client = image_api_client.ImageApiClient()
    image_client.upload(filepath=filepath, wood_id=wood_id)

    logger.getChild("scripts.image").debug("Image with the name: {0} uploaded".format(wood_id))