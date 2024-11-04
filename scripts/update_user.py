"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client import modify_record


def modify_user(user_id, data):
    user_modifier = modify_record.UserModifier()
    user_modifier.modify_data(user_id, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "username": "robotlab-admin-2",
    }

    modify_user(user_id=1, data=data)
