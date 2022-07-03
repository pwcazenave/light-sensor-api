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

from utils import rc_time, MCP3008
import config

api = flask.Blueprint('api', __name__, url_prefix='/api/v1')
logger = logging.getLogger(__name__)


@api.route('/timed/current/', strict_slashes=False)
async def instantaneous():
    """ Fetch the current timed instantaneous reading from the light sensor """

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


@api.route('/analog/current', strict_slashes=False)
async def analog_current():
    """ Fetch the current instantaneous reading from the light sensor """

    logger.info(f'Fetch current analog light intensity from {flask.request.remote_addr}')

    adc = MCP3008()

    intensity = {'current': adc.read(channel=0), 'time': datetime.now().isoformat()}

    adc.close()

    return flask.jsonify(intensity)


@api.route('/analog/last/<period>', strict_slashes=False)
async def analog_averaged(period):
    """ Average the analog light intensity over the given period """

    logger.info(f'Average analog light intensity over {period} seconds')
    period = int(period)
    start = datetime.now()

    cumulative_intensity = 0
    count = 0
    adc = MCP3008()
    while True:
        now = datetime.now()
        if (now - start).total_seconds() < period:
            count += 1
            cumulative_intensity += adc.read(channel=0)
        else:
            break
    finished = datetime.now()
    duration = (finished - start).total_seconds()
    adc.close()

    return flask.jsonify({'average_intensity': cumulative_intensity / count, 'requested_seconds': period, 'actual_seconds': duration, 'time': datetime.now().isoformat()})

