"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client.api_client import http_client


def modify_production(production_id, data):
    url = f"{http_client.base_url}{http_client.api_blueprints.production_by_id_route}{production_id}"
    http_client._update_record(url=url, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "operation": "stool_2.0",
    }

    modify_production(production_id=1, data=data)
