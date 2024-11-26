"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client.api_client import http_client


def modify_tag(tag_id, data):
    url = f"{http_client.base_url}{http_client.api_blueprints.tag_by_id_route}{tag_id}"
    http_client._update_record(url=url, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "name": "furniture",
    }

    modify_tag(tag_id=1, data=data)
