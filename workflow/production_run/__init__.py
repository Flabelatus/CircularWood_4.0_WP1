# __init__.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging

from collections import namedtuple

from settings import logger, data_service_config_loader as ds_api_configs
from settings import workflow_manager_config_loader as wrkflow_configs


logger = logging.getLogger('cw4.0-api').getChild('workflows.prod-gateway')
configs = {
    'data_service': ds_api_configs,
    'workflow': wrkflow_configs
}


class ProductionCore:
    def __init__(self, configs=configs):
        self.configs = configs
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def _get_production_run_params(self):
        ProductionRunParameters = namedtuple(
            'ProductionRunParameters',
                field_names=[
                    'root_dir',
                    'lector',
                    'printer',
                    'ftp',
                    'tcp',
                    'mqtt',
                    'http',
                    'database_service'
                ]
            )   

        auxiliary_devices = self.configs.get('workflow').hardware_equipment_configs['auxiliary_devices']
        lector_configs = [cfg for cfg in auxiliary_devices if cfg.get('title') == 'LECTOR'][0]
        printer_configs = [cfg for cfg in auxiliary_devices if cfg.get('title') == 'LABEL_PRINTER'][0]
        http_conf = self.configs.get('workflow').http_network_configs
        running_environment = self.configs.get('data_service').environment
        database_service = http_conf['environments'][running_environment]

        production_run_params = ProductionRunParameters(
            root_dir=self.root,
            lector=lector_configs,
            printer=printer_configs,
            ftp=wrkflow_configs.ftp_network_configs,
            tcp=wrkflow_configs.tcp_network_configs,
            mqtt=wrkflow_configs.mqtt_network_configs,
            http=http_conf,
            database_service=database_service,
        )

        logger.debug("production run parameters loaded")
        return production_run_params

    @property
    def params(self):
        return self._get_production_run_params()
