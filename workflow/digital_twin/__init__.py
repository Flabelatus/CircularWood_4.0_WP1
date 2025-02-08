# TODO: Complete it with the dashboard parameters etc.

# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from collections import namedtuple

from generated_dataclasses import *
from settings import data_service_config_loader as ds_api_configs
from settings import workflow_manager_config_loader as wrkflow_configs


logger = logging.getLogger('cw4.0-api').getChild('workflows.digital_twin')
__configs__ = {
    'data_service': ds_api_configs,
    'workflow': wrkflow_configs
}


class DigitalTwinCore:
    def __init__(self, configs=__configs__):
        self.configs = configs
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def _digital_twin_params(self):
        DigitalTwinParameters = namedtuple(
            'DigitalTwinParameters',
                field_names=[
                    'root_dir',
                    'idemat',
                ]
            )
           
    @property
    def params(self):
        return self._digital_twin_params()
