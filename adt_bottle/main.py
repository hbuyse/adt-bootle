#! /usr/bin/env python
# code=utf-8

import json
import sqlite3

from bottle import route, run
from bottle import get, post
from bottle import response
from bottle import abort

from tournament import parse_tournaments

from sqlite3 import Error

DATABASE_PATH = "./tournaments.db"

LIST_DEPARTEMENT = {
    "1": {
        "department": "Ain",
        "region": "Rhône-Alpes"
    },
    "2": {
        "department": "Aisne",
        "region": "Picardie"
    },
    "3": {
        "department": "Allier",
        "region": "Auvergne"
    },
    "4": {
        "department": "Alpes de Haute-Provence",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "5": {
        "department": "Hautes-Alpes",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "6": {
        "department": "Alpes-Maritimes",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "7": {
        "department": "Ardèche",
        "region": "Rhône-Alpes"
    },
    "8": {
        "department": "Ardennes",
        "region": "Champagne"
    },
    "9": {
        "department": "Ariège",
        "region": "Midi-Pyrénées"
    },
    "10": {
        "department": "Aube",
        "region": "Champagne"
    },
    "11": {
        "department": "Aude",
        "region": "Languedoc"
    },
    "12": {
        "department": "Aveyron",
        "region": "Midi-Pyrénées"
    },
    "13": {
        "department": "Bouches du Rhône",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "14": {
        "department": "Calvados",
        "region": "Basse-Normandie"
    },
    "15": {
        "department": "Cantal",
        "region": "Auvergne"
    },
    "16": {
        "department": "Charente",
        "region": "Poitou-Charente"
    },
    "17": {
        "department": "Charente Maritime",
        "region": "Poitou-Charente"
    },
    "18": {
        "department": "Cher",
        "region": "Centre"
    },
    "19": {
        "department": "Corrèze",
        "region": "Limousin"
    },
    "2A": {
        "department": "Corse du Sud",
        "region": "Corse"
    },
    "2B": {
        "department": "Haute-Corse",
        "region": "Corse"
    },
    "21": {
        "department": "Côte d'Or",
        "region": "Bourgogne"
    },
    "22": {
        "department": "Côtes d'Armor",
        "region": "Bretagne"
    },
    "23": {
        "department": "Creuse",
        "region": "Limousin"
    },
    "24": {
        "department": "Dordogne",
        "region": "Aquitaine"
    },
    "25": {
        "department": "Doubs",
        "region": "Franche-Comté"
    },
    "26": {
        "department": "Drôme",
        "region": "Rhône-Alpes"
    },
    "27": {
        "department": "Eure",
        "region": "Haute-Normandie"
    },
    "28": {
        "department": "Eure-et-Loir",
        "region": "Centre"
    },
    "29": {
        "department": "Finistère",
        "region": "Bretagne"
    },
    "30": {
        "department": "Gard",
        "region": "Languedoc"
    },
    "31": {
        "department": "Haute-Garonne",
        "region": "Midi-Pyrénées"
    },
    "32": {
        "department": "Gers",
        "region": "Midi-Pyrénées"
    },
    "33": {
        "department": "Gironde",
        "region": "Aquitaine"
    },
    "34": {
        "department": "Hérault",
        "region": "Languedoc"
    },
    "35": {
        "department": "Ille-et-Vilaine",
        "region": "Bretagne"
    },
    "36": {
        "department": "Indre",
        "region": "Centre"
    },
    "37": {
        "department": "Indre-et-Loire",
        "region": "Centre"
    },
    "38": {
        "department": "Isère",
        "region": "Rhône-Alpes"
    },
    "39": {
        "department": "Jura",
        "region": "Franche-Comté"
    },
    "40": {
        "department": "Landes",
        "region": "Aquitaine"
    },
    "41": {
        "department": "Loir-et-Cher",
        "region": "Centre"
    },
    "42": {
        "department": "Loire",
        "region": "Rhône-Alpes"
    },
    "43": {
        "department": "Haute-Loire",
        "region": "Auvergne"
    },
    "44": {
        "department": "Loire-Atlantique",
        "region": "Pays-de-la-Loire"
    },
    "45": {
        "department": "Loiret",
        "region": "Centre"
    },
    "46": {
        "department": "Lot",
        "region": "Midi-Pyrénées"
    },
    "47": {
        "department": "Lot-et-Garonne",
        "region": "Aquitaine"
    },
    "48": {
        "department": "Lozère",
        "region": "Languedoc"
    },
    "49": {
        "department": "Maine-et-Loire",
        "region": "Pays-de-la-Loire"
    },
    "50": {
        "department": "Manche",
        "region": "Normandie"
    },
    "51": {
        "department": "Marne",
        "region": "Champagne"
    },
    "52": {
        "department": "Haute-Marne",
        "region": "Champagne"
    },
    "53": {
        "department": "Mayenne",
        "region": "Pays-de-la-Loire"
    },
    "54": {
        "department": "Meurthe-et-Moselle",
        "region": "Lorraine"
    },
    "55": {
        "department": "Meuse",
        "region": "Lorraine"
    },
    "56": {
        "department": "Morbihan",
        "region": "Bretagne"
    },
    "57": {
        "department": "Moselle",
        "region": "Lorraine"
    },
    "58": {
        "department": "Nièvre",
        "region": "Bourgogne"
    },
    "59": {
        "department": "Nord",
        "region": "Nord"
    },
    "60": {
        "department": "Oise",
        "region": "Picardie"
    },
    "61": {
        "department": "Orne",
        "region": "Basse-Normandie"
    },
    "62": {
        "department": "Pas-de-Calais",
        "region": "Nord"
    },
    "63": {
        "department": "Puy-de-Dôme",
        "region": "Auvergne"
    },
    "64": {
        "department": "Pyrénées-Atlantiques",
        "region": "Aquitaine"
    },
    "65": {
        "department": "Hautes-Pyrénées",
        "region": "Midi-Pyrénées"
    },
    "66": {
        "department": "Pyrénées-Orientales",
        "region": "Languedoc"
    },
    "67": {
        "department": "Bas-Rhin",
        "region": "Alsace"
    },
    "68": {
        "department": "Haut-Rhin",
        "region": "Alsace"
    },
    "69": {
        "department": "Rhône",
        "region": "Rhône-Alpes"
    },
    "70": {
        "department": "Haute-Saône",
        "region": "Franche-Comté"
    },
    "71": {
        "department": "Saône-et-Loire",
        "region": "Bourgogne"
    },
    "72": {
        "department": "Sarthe",
        "region": "Pays-de-la-Loire"
    },
    "73": {
        "department": "Savoie",
        "region": "Rhône-Alpes"
    },
    "74": {
        "department": "Haute-Savoie",
        "region": "Rhône-Alpes"
    },
    "75": {
        "department": "Paris",
        "region": "Ile-de-France"
    },
    "76": {
        "department": "Seine-Maritime",
        "region": "Haute-Normandie"
    },
    "77": {
        "department": "Seine-et-Marne",
        "region": "Ile-de-France"
    },
    "78": {
        "department": "Yvelines",
        "region": "Ile-de-France"
    },
    "79": {
        "department": "Deux-Sèvres",
        "region": "Poitou-Charente"
    },
    "80": {
        "department": "Somme",
        "region": "Picardie"
    },
    "81": {
        "department": "Tarn",
        "region": "Midi-Pyrénées"
    },
    "82": {
        "department": "Tarn-et-Garonne",
        "region": "Midi-Pyrénées"
    },
    "83": {
        "department": "Var",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "84": {
        "department": "Vaucluse",
        "region": "Provence-Alpes-Côte d'Azur"
    },
    "85": {
        "department": "Vendée",
        "region": "Pays-de-la-Loire"
    },
    "86": {
        "department": "Vienne",
        "region": "Poitou-Charente"
    },
    "87": {
        "department": "Haute-Vienne",
        "region": "Limousin"
    },
    "88": {
        "department": "Vosges",
        "region": "Lorraine"
    },
    "89": {
        "department": "Yonne",
        "region": "Bourgogne"
    },
    "90": {
        "department": "Territoire-de-Belfort",
        "region": "Franche-Comté"
    },
    "91": {
        "department": "Essonne",
        "region": "Ile-de-France"
    },
    "92": {
        "department": "Hauts-de-Seine",
        "region": "Ile-de-France"
    },
    "93": {
        "department": "Seine-St-Denis",
        "region": "Ile-de-France"
    },
    "94": {
        "department": "Val-de-Marne",
        "region": "Ile-de-France"
    },
    "95": {
        "department": "Val-d'Oise",
        "region": "Ile-de-France"
    }
}

SQL_CREATE_TOURNAMENT_TABLE = """ CREATE TABLE IF NOT EXISTS tournaments (
                                        id integer PRIMARY KEY,
                                        name text,
                                        city text NOT NULL,
                                        href text,
                                        ground text,
                                        new BOOLEAN,
                                        full BOOLEAN,
                                        night BOOLEAN,
                                        dpt text
                                    ); """


SQL_CREATE_EVENTS_TABLE = """ CREATE TABLE IF NOT EXISTS tournaments (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """


def dict_factory(cursor, row):
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@get('/')
def get_tournaments():
    response.content_type = 'application/json'
    d = dict()

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # fetch all or one we'll go for all
        cur.execute("SELECT * FROM TOURNAMENTS")
        results = cur.fetchall()

        for int_d in results:
            d[int_d["id"]] = int_d
            d[int_d["id"]].pop('id', None)
        
        conn.close()
        return d
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))
        pass

@get('/dpt/<dpt>')
def get_tournaments(dpt):
    response.content_type = 'application/json'
    d = dict()

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # fetch all or one we'll go for all
        cur.execute("SELECT * FROM tournaments WHERE dpt = {}".format(dpt))
        results = cur.fetchall()

        for int_d in results:
            d[int_d["id"]] = int_d
            d[int_d["id"]].pop('id', None)
        
        conn.close()        
        return d
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))
        pass

@get('/id/<id_t>')
def get_tournaments(id_t):
    response.content_type = 'application/json'

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # fetch all or one we'll go for all
        cur.execute("SELECT * FROM tournaments WHERE id = {}".format(id_t))
        result = cur.fetchone()

        result.pop('id', None)
        
        conn.close()
        return result
    except Exception as e:
        abort(500, "{}: {}".format(type(e).__name__, str(e)))
        pass

@post('/')
def post_tournaments():
    d = parse_tournaments()
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()

        for k, v in d.items():
            cur.execute("INSERT INTO tournaments(id, name, city, href, ground, new, full, night, dpt) VALUES (?,?,?,?,?,?,?,?,?)" , (k, v['name'] if "name" in v else str(), v['city'], v['href'], v['ground'], v['new'], v['full'], v['night'], v['dpt']))
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(type(e).__name__, str(e), int(k))
    finally:
        conn.close()


if __name__ == "__main__":
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute(SQL_CREATE_TOURNAMENT_TABLE)
        conn.execute(SQL_CREATE_EVENTS_TABLE)
    except Error as e:
        print(e)
    finally:
        conn.close()

    # run bottle
    run(host='localhost', port=8080, debug=True)