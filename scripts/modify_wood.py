"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def modify_wood(wood_id, data):
    wood_modifier = modify_record.WoodModifier()
    wood_modifier.modify_data(wood_id, data=data)


if __name__ == "__main__":

    data = {
        "length": 1022,
        "source": "Derako"
    }

    modify_wood(wood_id=1, data=data)
