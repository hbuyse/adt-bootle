#! /usr/bin/env python
# code=utf-8

__author__ = "hbuyse"

import logging
import logging.config
import sqlite3
import sys
import os
import json

import bottle

from approutes import app, plugins

def setup_logging(configpath='logging.json', level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = configpath
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)

    for plugin in plugins:
        app.install(plugin)

    import approutes
    if os.environ.get('APP_LOCATION') == 'heroku':
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        run(host='localhost', port=8080, debug=True)