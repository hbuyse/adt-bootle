import os
import logging
import sqlite3

from urllib import parse

from bottle import Bottle
from bottle import route, run
from bottle import get, post
from bottle import response
from bottle import abort, redirect

import bottle_pgsql

from utils import insert_into, check_if_id_exists
from tournament import parse_tournaments
from exceptions import IdNotFound, NoTournamentInDepartement, NoTournament

# Set the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create the app
app = Bottle()
plugins = list()

if os.environ.get('DATABASE_URL'):
    pgsql_str = str()

    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    pgsql_str += "" if url.path[1:] is None else 'dbname={} '.format(url.path[1:])
    pgsql_str += "" if url.username is None else 'user={} '.format(url.username)
    pgsql_str += "" if url.password is None else 'password={} '.format(url.password)
    pgsql_str += "" if url.hostname is None else 'host={} '.format(url.hostname)
    pgsql_str += "" if url.port is None else 'port={} '.format(url.port)
    plugins =  [
        bottle_pgsql.Plugin(pgsql_str)
    ]
else:
    plugins =  [
        bottle.ext.sqlite.Plugin(dbfile='adt.db')
    ]

@app.get('/')
def get_tournaments(db):
    response.content_type = 'application/json'
    data = dict()

    # fetch all or one we'll go for all
    try:
        db.execute("SELECT * FROM tournaments")
    except AttributeError as e:
        raise NoTournament("No tournament")

    rows = db.fetchall()
    for row in rows:
        tmp = row
        db.execute("SELECT * FROM events WHERE tournament_id = {}".format(tmp['id']))
        tmp['events'] = db.fetchall()
        data.update( { tmp["id"]: tmp })

    return data

@app.get('/dpt/<dpt>')
def get_tournaments(dpt, db):
    response.content_type = 'application/json'
    data = dict()

    # fetch all or one we'll go for all

    try:
        db.execute("SELECT * FROM tournaments WHERE dpt::integer = {}".format(dpt))
    except AttributeError as e:
        raise NoTournamentInDepartement("No tournament in department {}".format(dpt))

    rows = db.fetchall()
    for row in rows:
        tmp = row
        db.execute("SELECT * FROM events WHERE tournament_id = {}".format(tmp['id']))
        tmp['events'] = db.fetchall()
        data.update( { tmp["id"]: tmp })
            
    return data

@app.get('/id/<id_t>')
def get_tournaments(id_t, db):
    response.content_type = 'application/json'

    # fetch all or one we'll go for all
    try:
        db.execute("SELECT * FROM tournaments WHERE id::integer = {}".format(id_t))
    except AttributeError as e:
        raise IdNotFound("ID {} not found".format(id_t))

    data = db.fetchone()
    print(data)
    db.execute("SELECT * FROM events WHERE tournament_id = {}".format(data['id']))
    data['events'] = db.fetchall()
    
    return data

@app.post('/')
def post_tournaments(db):
    tournaments = parse_tournaments()
    for tournament in tournaments:
        if not check_if_id_exists(db=db, table='tournaments', id=tournament['id']):
            events = tournament.pop('events')
            insert_into(db=db, tournament=tournament)

            for event in events:
                insert_into(db=db, event=event, tournament_id=tournament['id'])
