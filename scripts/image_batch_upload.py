import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import image_api_client
from settings import logger

def batch_upload(base_fp, client=image_api_client.ImageApiClient()):
    """Script to batch upload the images inside a directory that the path is provideds

    Args:
        base_fp (str): The path of the directory where the images are located in.
        client (_type_): _description_
    """

    base_filenames = []

    try:
        filenames = []

        for file in os.listdir(base_fp):
            logger.debug(f"...Uploading {file}")
            filenames.append(os.path.join(base_fp, file))
            base_filenames.append(file)

        for i in range(len(base_filenames)):
            response = client.upload(
                filenames[i], base_filenames[i].split(".")[0])
            logger.debug(response)

    except KeyboardInterrupt:
        logger.info("\nProgram aborted")
    except FileNotFoundError as err:
        logger.error(err)


if __name__ == "__main__":
    
    client = image_api_client.ImageApiClient()
    base_fp = os.path.join(client.params.static_path, client.params.dir[0])
    # base_fp = input("Paste here the path directory of images: ")
    batch_upload(base_fp=base_fp)
