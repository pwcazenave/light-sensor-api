#!/usr/bin/env python3

""" Simple Flask app to server the light sensor data over REST """

import logging
import os

import flask

import api
import config

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 8000))
debug = 'DEBUG' in os.environ
use_reloader = os.environ.get('USE_RELOADER', '1') == '1'

root_logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-4s %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
root_logger.addHandler(flask.logging.default_handler)
if debug:
    root_logger.setLevel(logging.DEBUG)
else:
    root_logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info('Starting app')

app = flask.Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.urandom(32)
app.register_blueprint(api.api)


@app.get("/")
async def root(update=False):
    return flask.Response(status=403, response="Nothing to see here")


def main():
    logger.info('Starting main')
    app.run(host=host,
            port=port,
            debug=debug,
            use_reloader=use_reloader)


if __name__ == '__main__':
    main()
