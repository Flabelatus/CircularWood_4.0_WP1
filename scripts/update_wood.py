"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.api_http_client import modify_record


def modify_wood(wood_id, data):
    wood_modifier = modify_record.WoodModifier()
    wood_modifier.update(wood_id, data=data)


def modify_production(production_id, data):
    production_modifier = modify_record.ProductionModifier()
    production_modifier.update(production_id, data=data)


def modify_user(user_id, data):
    user_modifier = modify_record.UserModifier()
    user_modifier.modify_data(user_id, data=data)


def modify_tag(tag_id, data):
    tag_modifier = modify_record.TagsModifier()
    tag_modifier.modify_data(tag_id, data=data)


if __name__ == "__main__":
    
    # Example
    data = {
        "length": 1022,
        "source": "Derako"
    }

    modify_wood(wood_id=1, data=data)
