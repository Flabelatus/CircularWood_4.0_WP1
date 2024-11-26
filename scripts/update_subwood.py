"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client.api_client import http_client


def modify_subwood(subwood_id, data):
    http_client.update_subwood_by_id(subwood_id, data)


if __name__ == "__main__":
    
    # Example
    data = {
        "length": 340,
    }

    modify_subwood(subwood_id=1, data=data)
