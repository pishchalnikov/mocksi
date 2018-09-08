from unittest import TestCase, mock

from mocksi import mocksi_server
from mocksi.utils.docker_cli import DockerCli


class ContainerTest(TestCase):
    container = {
        'created': 1534160115,
        'id': '4024449f1ed5bfb36acf98fb7eaf614c7',
        'image': 'http_image',
        'port': 32264,
        'state': 'running',
        'status': 'Up 2 days',
        'version': 'latest'
    }
    config = {
        'services': {
            'http_mock': {
                'image': 'http_image',
                'version': 'latest',
                'port': 80
            }
        }
    }

    def setUp(self):
        self.app = mocksi_server.app.test_client()

    @mock.patch.object(DockerCli, '_get_containers')
    def test_containers(self, mock_get_containers):
        mock_get_containers.return_value = (self.container,)

        resp = self.app.get('/api/containers')
        self.assertEqual(200, resp.status_code,)
        self.assertEqual('application/json', resp.content_type)
        self.assertEqual([self.container], resp.json)

    @mock.patch.object(DockerCli, '_get_containers')
    def test_containers_id(self, mock_get_containers):
        mock_get_containers.return_value = (self.container,)

        resp = self.app.get('/api/containers/{}'.format(self.container['id']))
        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        self.assertEqual(self.container, resp.json)

    @mock.patch.object(DockerCli, 'create_container')
    def test_containers_create_container(self, mock_create_container):
        mock_create_container.return_value = self.container

        resp = self.app.post(
            '/api/containers',
            json={
                'image': self.container['image']
            }
        )
        self.assertEqual(200, resp.status_code, resp.json)
        self.assertEqual('application/json', resp.content_type)
        self.assertEqual(self.container, resp.json)

    @mock.patch.object(DockerCli, 'remove_container')
    def test_containers_delete_container(self, mock_remove_container):
        ok = {'status': 'OK'}
        mock_remove_container.return_value = ok

        resp = self.app.delete(
            '/api/containers/' + self.container['id']
        )
        self.assertEqual(200, resp.status_code, resp.json)
        self.assertEqual('application/json', resp.content_type)
        self.assertEqual(ok, resp.json)
