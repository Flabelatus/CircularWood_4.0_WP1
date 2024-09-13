import sys
import os
import logging
import textwrap

from load_dotenv import load_dotenv
from ruamel.yaml import YAML

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

load_dotenv()

# Text Reset
RESET = "\033[0m"

# Text Styles
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
INVERT = "\033[7m" 

# Foreground Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright Foreground Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background Colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright Background Colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"


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
    LOG_LEVEL_PROD = logging.WARNING

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
            formatter = logging.Formatter(self.LOG_FORMAT_PROD, datefmt=self.date_format)
            self.console_handler.setFormatter(formatter)
            logging.basicConfig(level=self.LOG_LEVEL_PROD, handlers=[self.console_handler])
        else:
            formatter = CustomLogFormatter(self.LOG_FORMAT_DEBUG, datefmt=self.date_format)
            self.console_handler.setFormatter(formatter)
            logging.basicConfig(level=logging.DEBUG, handlers=[self.console_handler])

    def is_production(self) -> bool:
        """Determine if the environment is set to production."""
        return self.settings.server_configs['environment']['selected_mode'].lower() == 'production'
    
    @staticmethod
    def disable_external_package_logging(package_names):
        for name in package_names:
            logging.getLogger(name).setLevel(logging.WARNING)

    @staticmethod
    def is_color_terminal() -> bool:
        """Check if terminal supports color output."""
        print(sys.stdout.isatty() and os.getenv('TERM') not in ('dumb', 'unknown'))
        return True


# Instantiate `app_settings`
app_settings = ApiConfig()

# Instantiate logger
api_logging = AppLogger(app_settings)

package_names = ['urllib3', 'tzlocal', 'passlib']
api_logging.disable_external_package_logging(package_names)
logger = logging.getLogger('wood-api')


if __name__ == "__main__":
    logger.info("API Config settings:", app_settings.settings)
