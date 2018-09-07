from flask import jsonify, request

from mocksi.api import api, errors
from mocksi.utils.docker_cli import DockerCli
from mocksi.utils.exceptions import NotFoundImageException
from mocksi.utils.exceptions import NotFoundContainerException


docker = DockerCli()


@api.route('/containers')
def get_containers():
    return jsonify(docker.get_all_containers())


@api.route('/containers/<string:id>')
def get_container(id):
    if id:
        try:
            return jsonify(docker.get_container(id))
        except NotFoundContainerException as e:
            return errors.not_found(e)
    return errors.bad_request('Container id is required to get information')


@api.route('/containers', methods=['POST'])
def create_container():
    image = request.get_json().get('image')
    if image:
        try:
            return jsonify(docker.create_container(image))
        except NotFoundImageException as e:
            return errors.not_found(e)
    return errors.bad_request('Image is required to create container')


@api.route('/containers/<string:id>', methods=['DELETE'])
def delete_container(id):
    if id:
        try:
            return jsonify(docker.remove_container(id))
        except NotFoundContainerException as e:
            return errors.not_found(e)
    return errors.bad_request('Container id is required to delete it')
