from docker import APIClient, errors

from mocksi.utils.config import Config
from mocksi.utils.exceptions import NotFoundImageException
from mocksi.utils.exceptions import NotFoundContainerException


class DockerCli:

    def __init__(self):
        self.client = APIClient('unix://var/run/docker.sock')
        self.filtered_statuses = ('running', 'restarting', 'paused', 'exited')
        self.config = Config()

    def _get_containers(self, filters=None):
        filters = filters if filters else dict()

        for status in self.filtered_statuses:
            filters.update({'status': status})

            for container in self.client.containers(
                    all=True,
                    filters=filters
            ):
                img_name, _, img_version = container['Image'].partition(':')
                service = self.config.get_service_by_name(img_name)

                if service:
                    instance = dict()
                    instance['created'] = container['Created']
                    instance['id'] = container['Id']
                    instance['image'] = img_name

                    for con_port in container['Ports']:
                        if service['port'] is con_port['PrivatePort']:
                            instance['port'] = con_port.get('PublicPort')
                        else:
                            instance['port'] = None

                    instance['state'] = container['State']
                    instance['status'] = container['Status']
                    instance['version'] = img_version

                    yield instance

        return

    def get_all_containers(self):
        containers = []
        for container in self._get_containers():
            if container:
                containers.append(container)

        return containers

    def get_container(self, by_id):
        for container in self._get_containers({'id': by_id}):
            return container

        raise NotFoundContainerException(
            'Container was not found: {}'.format(by_id)
        )

    def create_container(self, image):
        service = self.config.get_service_by_name(image)
        if service:
            container = self.client.create_container(
                image='{0}:{1}'.format(image, service['version']),
                ports=[service['port']],
                detach=True,
                host_config=self.client.create_host_config(
                    port_bindings={service['port']: None}
                )
            )
            self.client.start(container=container['Id'])
            return self.get_container(container['Id'])

        raise NotFoundImageException('Image was not found: {}'.format(image))

    def remove_container(self, by_id):
        try:
            self.client.remove_container(
                container=by_id,
                force=True,
                v=True
            )
        except errors.NotFound as e:
            raise NotFoundContainerException(e)

        return {'status': 'OK'}
