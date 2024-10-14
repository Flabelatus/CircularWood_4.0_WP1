"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_tag(tag_id):
    tag_modifier = modify_record.TagsModifier()
    # tag_modifier.delete(tag_id)


if __name__ == "__main__":

    delete_tag(tag_id=[100])
