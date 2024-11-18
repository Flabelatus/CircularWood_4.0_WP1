"""_summary_
"""

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.inspection import inspect

logger = logging.getLogger('cw4.0-api.models')


class DataModelInterface:
    def __init__(self):
        pass

    def relationship_fields(self):
        """
        Collects all relationship fields of the model and returns them as a list.
        """
        relationship_fields = []
        mapper = inspect(self.__class__)
        
        for attr_name, attr in mapper.all_orm_descriptors.items():
            if isinstance(attr.property, RelationshipProperty):
                relationship_fields.append(attr_name)
        
        logger.debug(f"Relationship fields: {relationship_fields}")
        return relationship_fields

    def _get_status_fields(self, status_fields):
        return {
            field: getattr(self, field)
            for field in status_fields
            if hasattr(self, field)
        }
