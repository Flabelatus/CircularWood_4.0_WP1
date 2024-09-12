import sys
import os
import logging

from load_dotenv import load_dotenv
from ruamel.yaml import YAML

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

load_dotenv()


class ApiConfig:
    def __init__(self) -> None:
        self.path = os.getenv("CONFIG_FILE", "./settings.yml")
        self.yaml = YAML()

    @property
    def settings(self):
        with open(self.path, "r") as settings_yml:
            settings = self.yaml.load(settings_yml)['api']
        return settings

    @property
    def api_info(self):
        return {
            "title": self.settings['title'],
            "version": self.settings['version'],
            "description": self.settings['description']
        }
        
    @property
    def external(self):
        return self.settings['external']
        
    @property
    def environment(self):
        return self.settings['server']['environment']['selected_mode']

    @property
    def backend_env(self):
        if self.environment == 'development':
            return self.settings['server']['environment']['modes']['development']
        else:
            return  self.settings['server']['environment']['modes']['production']
        
    @property
    def api_configs(self):
        return self.settings['configs']

    @property
    def db_configs(self):
        return self.settings['database']

    @property
    def doc_configs(self):
        return self.settings['documentation']

    @property
    def server_configs(self):
        return self.settings['server']

    @property
    def security_configs(self):
        return self.settings['security']

    @property
    def logging_configs(self):
        return self.settings['logging']

    @logging_configs.setter
    def set_logging_configs(self, new_logging_configs):
        assert 'format' in new_logging_configs, "format should be specified e.g. json"
        assert 'output' in new_logging_configs, "output field should be specified e.g. stdout"

        self.logging_configs['format'] = new_logging_configs['format']
        self.logging_configs['output'] = new_logging_configs['output']

    @property
    def cache_configs(self):
        return self.settings['cache']


class AppLogger:

    # Debug and Production log formats
    LOG_FORMAT_DEBUG = '%(levelname)-8s: %(name)-5s.%(filename)-30s %(message)s'
    LOG_FORMAT_PROD = '%(asctime)-15s %(levelname)s:%(name)s: %(message)s'
    LOG_LEVEL_PROD = logging.WARNING

    def __init__(self, settings) -> None:
        """Initialize logging configuration based on the environment."""
        self.settings = settings
        self.configure_logging()

    @staticmethod
    def is_color_terminal() -> bool:
        """Check if terminal supports color output."""
        return sys.stdout.isatty() and os.getenv('TERM') not in ('dumb', 'unknown')

    def configure_logging(self) -> None:
        """Configure logging based on the environment setting."""
        if self.is_production():
            self.logging_config_production()
        else:
            self.logging_config_debug()

    def is_production(self) -> bool:
        """Determine if the environment is set to production."""
        if self.settings:
            return self.settings.server_configs['environment']['selected_mode'].lower() == 'production'
        else:
            return False

    def logging_config_debug(self) -> None:
        """Configure logging for the debug environment with optional color support."""
        try:
            import coloredlogs
        except ImportError:
            coloredlogs = None

        log_level = os.getenv('API_LOG_LEVEL', 'DEBUG').upper()
        if coloredlogs and self.is_color_terminal():
            level_styles = {
                'spam': {'color': 'green', 'faint': True},
                'debug': {},
                'notice': {'color': 'magenta'},
                'success': {'bold': True, 'color': 'green'},
                'info': {'bold': True, 'color': 'cyan'},
                'warning': {'color': 'yellow'},
                'error': {'color': 'red'},
                'critical': {'bold': True, 'color': 'red'},
            }
            field_styles = {
                'asctime': {'color': 'green'},
                'hostname': {'color': 'magenta'},
                'levelname': {'color': 8},
                'name': {'color': 8},
                'programname': {'color': 'cyan'},
                'username': {'color': 'yellow'},
            }
            coloredlogs.install(
                level=log_level,
                level_styles=level_styles,
                field_styles=field_styles,
                fmt=self.LOG_FORMAT_DEBUG
            )
        else:
            logging.basicConfig(level=log_level, format=self.LOG_FORMAT_DEBUG)

    def logging_config_production(self) -> None:
        """Configure logging for the production environment."""
        logging.basicConfig(level=self.LOG_LEVEL_PROD,
                            format=self.LOG_FORMAT_PROD)


# Instantiate `app_settings`
app_settings = ApiConfig()
# Instantiate logger
api_logging = AppLogger(app_settings)

logger = logging.getLogger('wood-api')

logger.info(app_settings.server_configs)

if __name__ == "__main__":
    logger.info("API Config settings:", app_settings.settings)
