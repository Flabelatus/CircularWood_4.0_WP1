"""DatabaseHandler summary ...

"""
import sys
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root)
from typing import Union, Dict
from workflow.api_http_client.api_client import http_client
from workflow.production_run import ProductionCore, logger

logger.getChild("db_handler")


class ProductionRunDBHandler(ProductionCore):
    def __init__(self):
        super().__init__()
        self.client = http_client
    
    def material_bundle_data(self, record_id: int) -> Union[Dict, None]:
        """Fetch and deliver the bundled data fromthe api client. The bundle contains all the 
        wood data, design metadata and the production data

        Args:
            record_id (int): The raw material ID

        Returns:
            Union[Dict, None]: The schema of the bundle as a Dict which contians the data fetched
            from the database linked to the wood such as production data, design metadata, and the 
            raw material data.
        """
        logger.debug(self.client.wood_bundle_data(record_id))

