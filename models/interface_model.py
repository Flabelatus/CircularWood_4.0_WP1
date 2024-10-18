"""_summary_
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import RelationshipProperty

from settings import logger


class DataModelInterface:
    def __init__(self):
        pass

    def relationship_fields(self):
        """
        Collects all relationship fields of the model and returns them as a list called 'partials'.
        """
        relationship_fields = []
        attr_names = dir(self)
        for attr_name in attr_names:
            if attr_name.startswith("_") or attr_name.endswith("_"):
                continue
            if attr_name == 'metadata':
                continue
            if isinstance(
                getattr(self, attr_name),
                RelationshipProperty,
            ):
                relationship_fields.append(attr_name)
        logger.info(relationship_fields)
        return relationship_fields

    def _get_status_fields(self, status_fields):
        return {
            field: getattr(self, field)
            for field in status_fields
            if hasattr(self, field)
        }
