from unittest import TestCase, mock

from mocksi import mocksi_server
from mocksi.utils.config import Config


class ServiceTest(TestCase):

    services = {
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

    def setUp(self):
        self.app = mocksi_server.app.test_client()

    @mock.patch.object(Config, 'get_all_services')
    def test_service_get_services(self, mock_services):
        services = list(self.services.keys())
        mock_services.return_value = services

        resp = self.app.get('/api/services')
        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        self.assertListEqual(services, resp.json)

    @mock.patch.object(Config, 'get_all_services')
    def test_service_get_services_empty(self, mock_services):
        services = []
        mock_services.return_value = services

        resp = self.app.get('/api/services')
        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        self.assertListEqual(services, resp.json)
