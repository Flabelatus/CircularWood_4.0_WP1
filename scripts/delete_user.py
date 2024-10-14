"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_client import modify_record


def delete_user(user_id):
    user_modifier = modify_record.UserModifier()
    # user_modifier.delete(user_id)


if __name__ == "__main__":

    delete_user(user_id=[100])
