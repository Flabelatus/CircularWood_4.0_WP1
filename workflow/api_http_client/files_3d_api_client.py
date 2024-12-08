"""ThreeDFilesApiClient summary ...

"""

import os
import requests
from workflow.api_http_client import logger
from workflow.api_http_client.api_client import DataServiceApiHTTPClient

logger.getChild("image_upload")


class ThreeDFilesApiClient(DataServiceApiHTTPClient):

    def __init__(self, destination=0, development=False):
        super().__init__()
        
