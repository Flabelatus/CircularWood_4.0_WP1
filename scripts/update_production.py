"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def modify_production(production_id, data):
    production_modifier = modify_record.ProductionModifier()
    production_modifier.update(production_id, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "operation": "stool_2.0",
    }

    modify_production(production_id=1, data=data)
