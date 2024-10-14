"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Callable
from __init__ import Scripts
from settings import logger
from workflow.api_client import modify_record


class DeleteDataRow(Scripts):
    def __init__(self, script_file):
        super().__init__(script_file)
        

def _get_mapping():
    mapping = {
        "wood": delete_wood,
        "subwood": delete_subwood,
        "tag": delete_tag,
        "user": delete_user,
        "production": delete_production,
        "design_metadata": delete_design_metadata
    }

    menu = {i + 1: key for i, key in enumerate(mapping)}
    logger.info("Available selection for the script")
    logger.info(menu)

    return mapping


def map_data(choice: int = 0):
    mapping = _get_mapping()
    logger.info(mapping[choice])
        

def delete_wood(wood_id):
    wood_modifier = modify_record.WoodModifier()
    wood_modifier.delete(wood_id)


def delete_subwood(subwood_id):
    subwood_modifier = modify_record.SubWoodModifier()
    # subwood_modifier.delete(subwood_id)


def delete_tag(tag_id):
    tag_modifier = modify_record.TagsModifier()
    # tag_modifier.delete(tag_id)


def delete_user(user_id):
    user_modifier = modify_record.UserModifier()
    # user_modifier.delete(user_id)


def delete_production(production_id):
    production_modifier = modify_record.ProductionModifier()
    # production_modifier.delete(production_id)


def delete_design_metadata(design_id):
    design_modifier = modify_record.DesignMetaDataModifier()
    # design_modifier.delete(design_id)


def delete_tag(tag_id):
    tag_modifier = modify_record.TagsModifier()
    # tag_modifier.delete(tag_id)


# choice = int(input("select the script: "))

# if 0 < choice < len(_get_mapping()):
#     __script__ = map_data(choice=choice)
#     print(__script__)


s = DeleteDataRow(__file__)

print(s._methods())
# if __row__ == ""


# if __name__ == "__main__":
#     map_data(1)
# #     delete_wood(wood_id=[100])
