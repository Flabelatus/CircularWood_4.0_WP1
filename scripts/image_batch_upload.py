import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import image_api_client
from settings import logger, app_settings

def batch_upload(base_fp, client):

    base_filenames = []

    try:
        filenames = []

        for file in os.listdir(base_fp):
            logger.debug(f"...Uploading {file}")
            filenames.append(os.path.join(base_fp, file))
            base_filenames.append(file)

        for i in range(len(base_filenames)):
            response = client.upload(filenames[i], base_filenames[i].split(".")[1])
            logger.info(response)

    except KeyboardInterrupt:
        logger.info("\nProgram aborted")


if __name__ == "__main__":

    client = image_api_client.ImageApiClient()

    base_fp = os.path.join(client.params.static_path, client.params.dir[0])
    batch_upload(base_fp=base_fp, client=client)
