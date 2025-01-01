import sys
import os
import logging

from typing import Dict, List, Any, Union

import generated_dataclasses as gd
from utils.yaml_to_dataclass import generate_dataclass_file, generate_dataclasses_from_yaml
from utils.yaml_to_dataclass import convert_commented_map_to_dict
from load_dotenv import load_dotenv
from ruamel.yaml import YAML
from terminal_settings import *
from generated_dataclasses import *

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

load_dotenv()

logger = logging.getLogger('cw4.0-api')


class ConfigLoader:
    def __init__(self):
        self.yaml = YAML()
        self.path = os.getenv("CONFIG_FILE", "./settings.yml")
        
        with open(self.path, 'r') as conf_file:
            self.parsed_yml_settings = convert_commented_map_to_dict(
                YAML().load(conf_file)
            )

    def load_settings(self):
        with open(self.path, 'r') as settings_file:
            settings_content = self.yaml.load(settings_file)
            return settings_content
        

class DataServiceConfigLoader(ConfigLoader):
    def __init__(self):
        """Initializes the DataServiceConfigLoader with the base configuration from the parent class."""
        super().__init__()

    # Getters
    @property
    def settings(self) -> DataServiceApi:
        """Retrieves the main settings for the API.

        :Returns:
            (class) DataServiceApi: The configuration dictionary for the 'api' section.
        """
        parent_node = RootSchema(**self.parsed_yml_settings).data_service_api
        return DataServiceApi(**parent_node)

    @property
    def api_info(self) -> Dict[str, Any]:
        """Retrieves basic API information including title, version, and description.

        :Returns:
            Dict[str, Any]: A dictionary containing API metadata.
        """
        # api_conf = DataServiceApi(**self.settings)
        return {
            "title": self.settings.title,
            "version": self.settings.version,
            "description": self.settings.description
        }

    @property
    def external(self) -> External:
        """Retrieves external configurations related to external APIs and tools.

        :Returns:
            (class) External: External API and tool configuration.
        """
        # parent_node = 
        return self.settings.external

    @property
    def environment(self) -> Environment:
        environment = Server(**self.settings.server).environment
        return Environment(**environment)

    @property
    def environment_selected_mode(self) -> str:
        """Gets the current selected environment mode.

        :Returns:
            str: The selected environment mode ('development' or 'production').
        """
        return self.environment.selected_mode

    @property
    def backend_env(self) -> Union[DevelopmentEnv, ProductionEnv]:
        """Retrieves the backend environment configurations based on the selected mode.

        :Returns:
            Union[DevelopmentEnv, ProductionEnv]: The configuration for the current backend environment mode.
        """
        modes = Modes(**self.environment.modes)

        if self.environment_selected_mode == 'development':
            return DevelopmentEnv(**modes.development_env)
        else:
            return ProductionEnv(**modes.production_env)

    @property
    def api_configs(self) -> Configs:
        """Retrieves general API configuration settings.

        :Returns:
            (class) Configs: The configuration for API settings.
        """
        return Configs(**self.settings.configs)

    @property
    def db_configs(self) -> Database:
        """Retrieves the database configuration settings.

        :Returns:
            Dict[str, Any]: The configuration for database settings.
        """
        return Database(**self.settings.database)

    @property
    def doc_configs(self) -> Documentation:
        """Retrieves the documentation configuration settings.

        :Returns:
           (class) Documentation: The configuration for documentation settings.
        """
        return Documentation(**self.settings.documentation)

    @property
    def server_configs(self) -> Server:
        """Retrieves the server configuration settings.

        :Returns:
            (class) Server: The configuration for server settings.
        """
        return Server(**self.settings.server)

    @property
    def security_configs(self) -> Security:
        """Retrieves the security configuration settings.

        :Returns:
            (class) Security: The configuration for security settings.
        """
        return Security(**self.settings.security)

    @property
    def cookie_configs(self) -> CookieSettings:
        """Retrieves the cookie configuration settings.

        :Returns:
            (class) CookieSettings: The configuration for coockie settings.
        """
        return CookieSettings(**self.security_configs.cookie_settings)

    @property
    def logging_configs(self) -> Logging:
        """Retrieves the logging configuration settings.

        :Returns:
            (class) Logging: The configuration for logging settings.
        """
        return Logging(**self.settings.logging)

    @property
    def cache_configs(self) -> Cache:
        """Retrieves the cache configuration settings.

        :Returns:
            (class) Cache: The configuration for cache settings.
        """
        return Cache(**self.settings.cache)


class WorkflowManagerConfigLoader(ConfigLoader):
    def __init__(self):
        super().__init__()
    
    @property
    def workflow_settings(self) -> WorkflowManager:
        parent_node = RootSchema(**self.parsed_yml_settings).workflow_manager
        return WorkflowManager(**parent_node)

    @property
    def api_http_client_configs(self) -> ApiHttpClient:
        http_conf = self.workflow_settings.api_http_client
        return ApiHttpClient(**http_conf)
    
    @property
    def production_run_configs(self) -> ProductionRun:
        prod_conf = self.workflow_settings.production_run
        return ProductionRun(**prod_conf)

    @property
    def network_configuration(self) -> NetworkConfiguration:
        """Get the network configuration settings."""
        net_conf = self.production_run_configs.network_configuration
        return NetworkConfiguration(**net_conf)
    
    @property
    def hardware_configs(self) -> HardwareComponents:
        hardware_comps = self.production_run_configs.hardware_components
        return HardwareComponents(**hardware_comps)

    @property
    def control_system_configs(self) -> ControlSystem:
        """Get the control system configurations."""
        return ControlSystem(**self.hardware_configs.control_system)

    @property
    def hardware_equipment_configs(self) -> Equipment:
        """Get the hardware equipment configurations."""
        return Equipment(**self.hardware_configs.equipment)

    @property
    def communication_protocols(self) -> CommunicationProtocols:
        return CommunicationProtocols(
            **self.production_run_configs.communication_protocols
        )

    @property
    def ftp_network_configs(self) -> Ftp:
        """Get the FTP network configurations."""
        return Ftp(**self.communication_protocols.ftp)
    
    @property
    def ftp_net_robot_configurations(self) -> RobotConfiguration:
        return RobotConfiguration(**self.ftp_network_configs.robot_configuration)

    @property
    def ftp_net_robot_red(self) -> RedRobot:
        return RedRobot(**self.ftp_net_robot_configurations.red_robot)

    @property
    def tcp_network_configs(self) -> Tcp:
        """Get the TCP network configurations."""
        return Tcp(**self.communication_protocols.tcp)

    @property
    def tcp_net_connections(self) -> Connections:
        return Connections(**self.tcp_network_configs.connections)

    @property
    def tcp_net_label_printer(self) -> LabelPrinter:
        return LabelPrinter(**self.tcp_net_connections.label_printer)

    @property
    def tcp_net_lector(self) -> Lector:
        return Lector(**self.tcp_net_connections.lector)

    @property
    def mqtt_network_configs(self) -> Mqtt:
        """Get the MQTT network configurations."""
        return Mqtt(**self.communication_protocols.mqtt)

    @property
    def http_network_configs(self) -> DatabaseService:
        """Get the HTTP database service configurations."""
        return DatabaseService(**Http(**self.communication_protocols.http).database_service)

    @property
    def profinet_network_configs(self) -> Profinet:
        """Get the PROFINET network configurations."""
        print(Profinet(**self.communication_protocols.profinet))
        return Profinet(**self.communication_protocols.profinet)


class CustomLogFormatter(logging.Formatter):
    
    def format(self, record):
        """Manually replace log parts and color them based on log level."""
        
        # Adjust the format dynamically based on log level
        if record.levelname == "DEBUG":
            log_format = f'{DIM}%(asctime)-5s{RESET} {DIM}-{RESET} {BOLD}{WHITE}{DIM}%(levelname)-10s{RESET}' \
                 f' | {DIM}%(name)-5s{RESET}.%(filename)-5s {RESET} {MAGENTA}::{RESET} {WHITE}%(message)s{RESET}'

        elif record.levelname == "ERROR":
            log_format = f'{RED}%(asctime)-5s{RESET} {RED}**{RESET} {BOLD}{BRIGHT_RED}%(levelname)-9s{RESET}' \
            f' | {DIM}%(name)-5s{RESET}.{BRIGHT_RED}%(filename)-5s{RESET}  {BRIGHT_RED}::{RESET} {BRIGHT_RED}%(message)s{RESET}'

        elif record.levelname == "WARNING":
            log_format = f'{YELLOW}%(asctime)-5s{RESET} {YELLOW}!!{RESET} {BOLD}{BRIGHT_YELLOW}%(levelname)-9s{RESET}' \
                 f' | {DIM}%(name)-5s{RESET}.{BRIGHT_YELLOW}%(filename)-5s{RESET}  {BRIGHT_YELLOW}::{RESET} {BRIGHT_YELLOW}%(message)s{RESET}'
        
        elif record.levelname == "INFO":
            log_format = f'{CYAN}%(asctime)-5s{RESET} {CYAN}|__{RESET} {BOLD}{BRIGHT_CYAN}%(levelname)-8s{RESET}' \
                 f' | {DIM}%(name)-5s{RESET}.%(filename)-5s {RESET} {MAGENTA}::{RESET} {BRIGHT_CYAN}%(message)s{RESET}'
        
        else:
            log_format = '%(asctime)-5s : %(levelname)-8s | %(name)-5s.%(filename)-5s ___ %(message)s'

        self._style._fmt = log_format

        return super().format(record)
    

class AppLogger:
    LOG_FORMAT_DEBUG = '%(asctime)-5s : %(levelname)-8s | %(name)-5s.%(filename)-5s :: %(message)s'
    LOG_FORMAT_PROD = '%(asctime)-15s %(levelname)s:%(name)s: %(message)s'
    LOG_LEVEL_PROD = logging.INFO

    def __init__(self, settings) -> None:
        """Initialize logging configuration based on the environment."""
        self.settings = settings
        self.console_handler = logging.StreamHandler()
        self.date_format = "%Y-%m-%d %H:%M:%S"

        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.INFO)

        # Remove all existing handlers
        if werkzeug_logger.hasHandlers():
            werkzeug_logger.handlers.clear()

        if self.is_production():
            formatter = CustomLogFormatter(self.LOG_FORMAT_PROD, datefmt=self.date_format)
            self.console_handler.setFormatter(formatter)
            logging.basicConfig(level=self.LOG_LEVEL_PROD, handlers=[self.console_handler])
        else:
            formatter = CustomLogFormatter(self.LOG_FORMAT_DEBUG, datefmt=self.date_format)
            self.console_handler.setFormatter(formatter)
            logging.basicConfig(level=logging.DEBUG, handlers=[self.console_handler])

    def is_production(self) -> bool:
        """Determine if the environment is set to production."""
        return self.settings.server_configs.environment['selected_mode'].lower() == 'production'
    
    @staticmethod
    def disable_external_package_logging(package_names):
        for name in package_names:
            logging.getLogger(name).setLevel(logging.WARNING)

    @staticmethod
    def is_color_terminal() -> bool:
        """Check if terminal supports color output."""
        print(sys.stdout.isatty() and os.getenv('TERM') not in ('dumb', 'unknown'))
        return True


# Instantiate data service API configurations loader
data_service_config_loader = DataServiceConfigLoader()

# Instantiate workflow config settings loader
workflow_manager_config_loader = WorkflowManagerConfigLoader()

# Instantiate logger
api_logging = AppLogger(data_service_config_loader)

package_names = ['urllib3', 'tzlocal', 'passlib']
api_logging.disable_external_package_logging(package_names)


if __name__ == "__main__":
    logger.info(f"API Config settings: {data_service_config_loader.api_configs}")
