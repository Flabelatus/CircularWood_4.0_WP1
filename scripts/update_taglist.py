"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client import modify_record


def modify_tag(tag_id, data):
    tag_modifier = modify_record.TagsModifier()
    tag_modifier.modify_data(tag_id, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "name": "furniture",
    }

    modify_tag(tag_id=1, data=data)
