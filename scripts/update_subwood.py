"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def modify_subwood(subwood_id, data):
    subwood_modifier = modify_record.SubWoodModifier()
    subwood_modifier.update(subwood_id, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "length": 340,
    }

    modify_subwood(subwood_id=1, data=data)
