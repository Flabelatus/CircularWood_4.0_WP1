"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_subwood(subwood_id):
    subwood_modifier = modify_record.SubWoodModifier()
    # subwood_modifier.delete(subwood_id)


if __name__ == "__main__":

    delete_subwood(subwood_id=[100])
