from flask import jsonify

from mocksi.api import api
from mocksi.utils.config import Config


config = Config()


@api.route('/services')
def get_services():
    return jsonify(config.get_all_services())
