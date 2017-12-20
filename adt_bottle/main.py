#! /usr/bin/env python
# code=utf-8

__author__ = "hbuyse"

import logging
import sqlite3
import sys

from bottle import run

from utils import create_db

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    create_db()

    # run bottle
    import approutes
    run(host='localhost', port=8080, debug=True)