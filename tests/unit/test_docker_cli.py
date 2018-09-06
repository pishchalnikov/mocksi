from unittest import TestCase, mock

from docker import errors

from mocksi.utils.docker_cli import DockerCli
from mocksi.utils.exceptions import NotFoundImageException
from mocksi.utils.exceptions import NotFoundContainerException


class DockerCliTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_config_patcher = mock.patch(
            'mocksi.utils.docker_cli.Config'
        )
        cls.mock_client_patcher = mock.patch(
            'mocksi.utils.docker_cli.APIClient'
        )

        cls.mock_config = cls.mock_config_patcher.start()
        cls.mock_client = cls.mock_client_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_config_patcher.stop()
        cls.mock_client_patcher.stop()

    service = {
        'image': 'test',
        'version': 'latest',
        'port': 80
    }
    container = {
        'Id': '4024449f1ed5bfb36acf98fb7eaf614c7',
        'Image': 'test:latest',
        'Created': 1534160115,
        'Ports': [
            {
                'IP': '0.0.0.0',
                'PrivatePort': 80,
                'PublicPort': 32264,
                'Type': 'tcp'
            }
        ],
        'State': 'exited',
        'Status': 'Exited (255) 3 days ago'
    }
    expect = {
            'created': container['Created'],
            'id': container['Id'],
            'image': 'test',
            'port': container['Ports'][0]['PublicPort'],
            'state': container['State'],
            'status': container['Status'],
            'version': 'latest'
    }

    def test_docker_cli_init(self):
        docker = DockerCli()
        self.assertIsInstance(docker, DockerCli)

    def test_docker_cli_get_containers(self):
        containers = self.mock_client.return_value.containers
        containers.return_value = [self.container]

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        filters = {'id': self.container['Id']}
        for container in docker._get_containers(filters):
            self.assertDictEqual(self.expect, container)

    def test_docker_cli_get_all_containers(self):
        containers = self.mock_client.return_value.containers
        containers.return_value = [self.container]

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertListEqual([self.expect], docker.get_all_containers())

    def test_docker_cli_get_all_containers_without_filters(self):
        containers = self.mock_client.return_value.containers
        containers.return_value = [self.container]

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = ()
        self.assertListEqual([], docker.get_all_containers())

    def test_docker_cli_get_all_containers_without_service(self):
        self.mock_client.return_value.containers.return_value = [self.container]

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = None

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertListEqual([], docker.get_all_containers())

    def test_docker_cli_get_container(self):
        self.mock_client.return_value.containers.return_value = [self.container]

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertDictEqual(
            self.expect, docker.get_container(self.container['Id'])
        )

    def test_docker_cli_get_container_not_found(self):
        self.mock_client.return_value.containers.return_value = []

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertRaises(
            NotFoundContainerException,
            docker.get_container, 'id123'
        )

    def test_docker_cli_create_container(self):
        self.mock_client.return_value.containers.return_value = [self.container]

        create_container = self.mock_client.return_value.create_container
        create_container.return_value = self.container

        start = self.mock_client.return_value.start
        start.return_value = self.container

        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = self.service

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertDictEqual(
            self.expect, docker.create_container('image')
        )

    def test_docker_cli_create_container_not_found(self):
        get_service_by_name = self.mock_config.return_value.get_service_by_name
        get_service_by_name.return_value = None

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertRaises(
            NotFoundImageException,
            docker.create_container, 'image123'
        )

    def test_docker_cli_remove_container(self):
        remove_container = self.mock_client.return_value.remove_container
        remove_container.return_value = None

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertDictEqual(
            {'status': 'OK'}, docker.remove_container('id123')
        )

    def test_docker_cli_remove_container_not_found(self):
        remove_container = self.mock_client.return_value.remove_container
        remove_container.side_effect = errors.NotFound('Not Found')

        docker = DockerCli()
        docker.filtered_statuses = (self.container['State'],)
        self.assertRaises(
            NotFoundContainerException,
            docker.remove_container, 'id123'
        )
