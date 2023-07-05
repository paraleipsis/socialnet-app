import logging.config
from typing import Dict
from pathlib import Path

import yaml


logger_conf_dir = 'conf/logger_conf.yml'


def load_config() -> Dict:
    """Load logging configuration file.

       :returns: :class:`Dict` of the logging type and the logging object.

    """

    with open(Path(__file__).resolve().parent.parent.parent / logger_conf_dir, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    configs = {
        'error': logging.getLogger('errorLogger'),
        'info': logging.getLogger('infoLogger'),
        'debug': logging.getLogger('debugLogger'),
    }

    return configs


logger = load_config()
