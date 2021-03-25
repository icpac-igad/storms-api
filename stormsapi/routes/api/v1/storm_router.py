import logging

from flask import jsonify, request

from stormsapi.routes.api.v1 import endpoints, error
from stormsapi.services import StormService


@endpoints.route('/storm', strict_slashes=False, methods=['POST'])
def create_storm():
    """Create storm"""
    logging.info('[ROUTER]: Creating storm')

    body = request.get_json()

    try:
        storm = StormService.create_storm_from_json(body)
    except Exception as e:
        logging.error('[ROUTER]: ' + str(e))
        return error(status=500, detail='Generic Error')

    return jsonify(data=storm.serialize()), 200
