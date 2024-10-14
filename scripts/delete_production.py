"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_production(production_id):
    production_modifier = modify_record.ProductionModifier()
    # production_modifier.delete(production_id)


if __name__ == "__main__":

    delete_production(production_id=[100])
