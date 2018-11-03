import gevent

from locust import HttpLocust, TaskSet, task


class MocksiAppApi(TaskSet):

    def get_services(self):
        self.client.get('/api/services', name='get_services')

    def get_containers(self):
        self.client.get('/api/containers', name='get_containers')

    def get_container(self, id):
        self.client.get(
            '/api/containers/' + id,
            name='get_container'
        )

    def create_container(self, image):
        with self.client.post(
                '/api/containers',
                json={'image': image},
                name='create_container',
                catch_response=True
        ) as response:
            if response.status_code == 500:
                response.failure(response.content)
                return
            return response.json()

    def delete_container(self, id):
        with self.client.delete(
            '/api/containers/' + id,
            name='delete_container',
            catch_response=True
        ) as response:
            if response.status_code == 500:
                response.failure('Internal Server Error')


class NormalBehavior(MocksiAppApi):
    test_image = 'httpd'

    @task(10)
    def do_get_services(self):
        self.get_services()

    @task(10)
    def do_get_containers(self):
        self.get_containers()

    @task(5)
    def do_utilize_containers(self):
        container = self.create_container(self.test_image)
        gevent.sleep(3)
        if container:
            self.get_container(container['id'])
            self.delete_container(container['id'])


class NormalBehaviorLocust(HttpLocust):
    task_set = NormalBehavior
    weight = 10
    min_wait = 100
    max_wait = 500
