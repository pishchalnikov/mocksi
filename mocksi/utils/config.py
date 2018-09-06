import os
import yaml

from mocksi.utils.exceptions import NotFoundFileException
from mocksi.utils.exceptions import ConfigFileEmptyException

CONFIG_FILE = os.getenv(
    'MOCKSI_CONFIG_FILE',
    os.path.normpath(os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir, 'config.yaml')
    )
)


class Config:
    def __init__(self, config_file=CONFIG_FILE):
        if os.path.isfile(config_file):
            with open(config_file, 'r') as file:
                data = file.read()
            self.config_data = yaml.safe_load(data)
            try:
                self.services = self.config_data.get('services', {})
            except AttributeError:
                raise ConfigFileEmptyException(
                    'Config file was empty: {}'.format(config_file)
                )
        else:
            raise NotFoundFileException(
                'Config file was not found: {}'.format(config_file)
            )

    def get_all_services(self):
        return list(self.services.keys())

    def get_service_by_name(self, name):
        return self.services[name] if name in self.services else None
