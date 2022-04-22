"""
Fetch light intensity values from the hardware sensors.

"""

import json
import logging
import time

from datetime import datetime

import flask
from flask import current_app
from dateutil.relativedelta import relativedelta

from utils import rc_time
import config

api = flask.Blueprint('api', __name__, url_prefix='/api/v1')
logger = logging.getLogger(__name__)


@api.route('/current/', strict_slashes=False)
async def instantaneous():
    """ Fetch the current instantaneous reading from the light sensor """

    logger.info(f'Fetch current light intensity from {flask.request.remote_addr}')

    intensity = {'current': rc_time(config.pin_to_circuit), 'time': datetime.now().isoformat()}

    return flask.jsonify(intensity)


@api.route('/timed/last/<period>', strict_slashes=False)
async def averaged(period):
    """ Average the light intensity over the given period """

    logger.info(f'Average light intensity over {period} seconds')
    period = int(period)
    start = datetime.now()

    cumulative_intensity = 0
    count = 0
    while True:
        count += 1
        now = datetime.now()
        if (now - start).total_seconds() < period:
            cumulative_intensity += rc_time(config.pin_to_circuit)
        else:
            break
    finished = datetime.now()
    duration = (finished - start).total_seconds()

    return flask.jsonify({'average_intensity': cumulative_intensity / count, 'requested_seconds': period, 'actual_seconds': duration, 'time': datetime.now().isoformat()})


