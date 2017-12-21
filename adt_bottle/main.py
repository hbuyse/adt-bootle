#! /usr/bin/env python
# code=utf-8

__author__ = "hbuyse"

import logging
import sqlite3
import sys
import os

import bottle

from approutes import app, plugins

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":

    for plugin in plugins:
        app.install(plugin)

    # run bottle
    # if os.environ.get('APP_LOCATION') == 'heroku':
    #     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # else:
    import approutes
    bottle.run(app, host='localhost', port=8080, debug=True)