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
    bottle.run(app, host='localhost', port=8080, debug=True)