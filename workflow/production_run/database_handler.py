"""DatabaseHandler summary ...

"""
import sys
import os
import json

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root)
from typing import Union, Dict, List
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

    def count_digits(self, num):
        """
        Counts the number of digits in a number.

        Args:
            num (int): The number to count the digits of.

        Returns:
            int: The number of digits in the input number.
        """

        count = 0
        while num != 0:
            num //= 10
            count += 1
        return count
    
    def subwood_list(self, record_id: int = 0):
        return self.client.fetch_subwood_by_wood_id(record_id)
    
    def production_instruction_list(self, record_id: int = 0):
        return self.client.fetch_production_by_wood_id(record_id)
    
    def design_metadata_list(self, record_id: int = 0):
        return self.client.fetch_design_by_wood_id(record_id)
    
    def serialize(self, input_data: List[float]) -> Dict:
        """
        Converts a list of integers representing wood lengths into a JSON string.

        Args:
            input (list): A list of integers representing wood lengths.

        Returns:
            str: A JSON string containing the processed wood length data.
        """
        data = dict()
        data["P_AMOUNT"] = str(len(input_data))

        for i in range(0, len(input_data)):
            field_name = f"P{str(i + 1)}L"
            data[field_name] = str(int(input_data[i]))
            field_name = f"P{str(i + 1)}L_len"
            data[field_name] = str(self.count_digits(input_data[i]))

        jsonified_string = json.dumps(data)
        return jsonified_string
    
    def get_processed_wood_data_by_id(self, record_id: int = 0):
        """
        Retrieves and processes wood data from a specified ID.

        Args:
            input_id (int): The ID of the wood to retrieve data for.

        Returns:
            str: A JSON string containing the processed wood length data.
        """
        lengths_list = []

        id_ = record_id
        data = self.subwood_list(id_)

        for sub_wood in data:
            length_value = sub_wood["length"]
            lengths_list.append(length_value)
        new_lengths_list = lengths_list

        temp = 0
        for i in range(0, len(lengths_list)):
            temp += lengths_list[i]
            new_lengths_list[i] = temp
        
        new_lengths_list_jsonified = self.serialize(new_lengths_list)

        return new_lengths_list_jsonified