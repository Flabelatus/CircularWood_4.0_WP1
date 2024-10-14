"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_design_metadata(design_id):
    design_modifier = modify_record.DesignMetaDataModifier()
    # design_modifier.delete(design_id)


if __name__ == "__main__":

    delete_design_metadata(design_id=[100])
