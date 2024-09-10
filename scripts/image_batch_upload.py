import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import image_api_client


def batch_upload(base_fp, client):

    base_filenames = []

    try:
        filenames = []

        for file in os.listdir(base_fp):
            clients.logger.debug(f"...Uploading {file}")
            filenames.append(os.path.join(base_fp, file))
            base_filenames.append(file)

        for i in range(len(base_filenames)):
            response = client.upload(filenames[i], base_filenames[i].split(".")[0])
            clients.logger.info(response)

    except KeyboardInterrupt:
        clients.logger.info("\nProgram aborted")


if __name__ == "__main__":

    client = clients.ImageApiClient(development=True)

    base_fp = os.path.join(client.params.static_path, client.params.dir[0])
    batch_upload(base_fp=base_fp, client=client)
