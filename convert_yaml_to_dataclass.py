import logging

from utils.yaml_to_dataclass import generate_dataclass_file
from utils.yaml_to_dataclass import generate_dataclasses_from_yaml
import generated_dataclasses as gd

logger = logging.getLogger('cw4.0-api')


def schema_lookup():
    keys = []
    for element in dir(gd):
        if element.startswith("_") or element.endswith("_"):
            continue
        keys.append(element)
    
    if len(keys) < 1:
        generate_dataclass_file('settings.yml', 'generated_dataclasses.py')
        logger.debug('The settings contents serialized successfully into `generated_dataclasses.py`')
    else:
        logger.debug('No new data classes generated as the Settings contents are already serialized')


if __name__ == '__main__':
    schema_lookup()