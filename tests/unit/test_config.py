from unittest import TestCase, mock

from mocksi.utils.config import Config
from mocksi.utils.exceptions import ConfigFileEmptyException


class ConfigTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_safe_load_patcher = mock.patch(
            'mocksi.utils.config.yaml.safe_load'
        )
        cls.mock_safe_load = cls.mock_safe_load_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_safe_load_patcher.stop()

    conf_data = {
        'services': {
            'http_mock': {
                'image': 'http_image',
                'version': 'latest',
                'port': 80
            },
            'ftp_mock': {
                'image': 'ftp_image',
                'version': 'latest',
                'port': 21
            }
        }
    }

    def test_config_init(self):
        conf = Config()
        self.assertIsInstance(conf, Config)

    def test_config_get_all_services(self):
        self.mock_safe_load.return_value = self.conf_data

        conf = Config()
        self.assertEqual(
            list(self.conf_data['services'].keys()), conf.get_all_services()
        )

    def test_config_get_all_services_empty(self):
        self.mock_safe_load.return_value = {}

        conf = Config()
        self.assertListEqual(
            list({}), conf.get_all_services()
        )

    def test_config_get_service_by_name(self):
        self.mock_safe_load.return_value = self.conf_data

        conf = Config()
        for service in iter(self.conf_data['services']):
            self.assertDictEqual(
                self.conf_data['services'][service],
                conf.get_service_by_name(service)
            )

    def test_config_get_service_by_name_empty(self):
        self.mock_safe_load.return_value = {}

        conf = Config()
        for service in iter(self.conf_data['services']):
            self.assertIsNone(conf.get_service_by_name(service))

    def test_config_file_empty(self):
        self.mock_safe_load.return_value = None

        self.assertRaises(
            ConfigFileEmptyException, Config
        )
