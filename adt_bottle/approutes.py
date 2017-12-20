import logging
import sqlite3

from bottle import route, run
from bottle import get, post
from bottle import response
from bottle import abort, redirect

from utils import insert_into, check_if_id_exists, DATABASE_PATH
from tournament import parse_tournaments
from exceptions import IdNotFound, NoTournamentInDepartement, NoTournament

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@get('/')
def get_tournaments():
    response.content_type = 'application/json'
    data = dict()

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # fetch all or one we'll go for all
        rows = cur.execute("SELECT * FROM TOURNAMENTS").fetchall()
        if len(rows) == 0:
            raise NoTournament("No tournament in department {}".format(dpt))

        for row in rows:
            tmp = dict(zip(row.keys(), tuple(row)))
            tmp['events'] = list()
            events = cur.execute("SELECT * FROM events WHERE tournament_id = {}".format(tmp['id'])).fetchall()
            tmp['events'] = [dict(zip(event.keys(), tuple(event))) for event in events]
            data.update( { tmp["id"]: tmp })
        
        conn.close()

        return data
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))

@get('/dpt/<dpt>')
def get_tournaments(dpt):
    response.content_type = 'application/json'
    data = dict()

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # fetch all or one we'll go for all
        rows = cur.execute("SELECT * FROM tournaments WHERE dpt = {}".format(dpt)).fetchall()
        if len(rows) == 0:
            raise NoTournamentInDepartement("No tournament in department {}".format(dpt))

        for row in rows:
            tmp = dict(zip(row.keys(), tuple(row)))
            tmp['events'] = list()
            events = cur.execute("SELECT * FROM events WHERE tournament_id = {}".format(tmp['id'])).fetchall()
            tmp['events'] = [dict(zip(event.keys(), tuple(event))) for event in events]
            data.update( { tmp["id"]: tmp })
            
        conn.close()
        
        return data
    except NoTournamentInDepartement as e:
        abort(404, "{}: {}".format(type(e).__name__, str(e)))
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))

@get('/id/<id_t>')
def get_tournaments(id_t):
    response.content_type = 'application/json'

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # fetch all or one we'll go for all
        row = cur.execute("SELECT * FROM tournaments WHERE id = {}".format(id_t)).fetchone()
        if row is None:
            raise IdNotFound("ID {} not found".format(id_t))

        data = dict(zip(row.keys(), tuple(row)))
        events = cur.execute("SELECT * FROM events WHERE tournament_id = {}".format(data['id'])).fetchall()
        data['events'] = [dict(zip(event.keys(), tuple(event))) for event in events]
        
        conn.close()

        return data
    except IdNotFound as e:
        abort(404, "{}: {}".format(type(e).__name__, str(e)))
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))

@post('/')
def post_tournaments():
    tournaments = parse_tournaments()
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        for tournament in tournaments:
            if not check_if_id_exists(conn=conn, table='tournaments', id=tournament['id']):
                for event in tournament['events']:
                    insert_into(conn=conn, event=event, tournament_id=tournament['id'])
                tournament.pop('events')
                insert_into(conn=conn, tournament=tournament)
    except Exception as e:
        abort(500, "{}: {} (tournament id: {})".format(type(e).__name__, str(e), tournament['id']))
    finally:
        conn.close()

    redirect('/')
