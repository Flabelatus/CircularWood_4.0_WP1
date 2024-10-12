"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_wood(wood_id):
    wood_modifier = modify_record.WoodModifier()
    wood_modifier.delete(wood_id)


if __name__ == "__main__":

    delete_wood(wood_id=[100])
