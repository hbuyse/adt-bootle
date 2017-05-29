#! /usr/bin/env python
# code=utf-8

import json

from bottle import route, run
from bottle import get, post
from bottle import response
from bottle import abort

from tournament import parse_tournaments

LIST_TOURNAMENTS = [
    {
        "events": [
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "3x3 Féminin"
                ],
                "level": [
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro"
                ]
            },
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "3x3 Masculin"
                ],
                "level": [
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro"
                ]
            },
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "4x4 Mixte"
                ],
                "level": [
                    "Loisir"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2312/neuvilleauxbois#amobile",
        "ground": "grass",
        "new": False,
        "full": False,
        "night": False,
        "city": "Neuville-aux-Bois",
        "department": 45,
        "id": 2312,
        "name": "Tournoi Albert Hay",
        "address": "10 rue de Ruau, 45170 Neuville-aux-Bois, France",
        "user": "Neuville Sports Volley-Ball",
        "phone": "02.38.75.51.21",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2312/neuvilleauxbois",
        "hour": "10h",
        "terrains": 20,
        "gymnasium": 1,
        "inscription": "Prévente : 8€ par joueur\nSur place : 8€ par joueur\n\nA l'ordre de Neuville Sports Volley-Ball\nA envoyer au 13 rue de Mondame, 45170 Neuville-aux-bois",
        "additional": "Neuville Sports Volley-Ball propose à son habitude son fameux tournoi sur herbe le jeudi de l'Ascension. \nPlusieurs formules disponibles :\n- 3x3 Féminins (8€ par joueur)\n- 3x3 Masculins (8€ par joueur)\n- 4x4 Loisirs Mixte (8€ par joueur)\n- 2x2 M11 - M13 Mixte (5€ par joueur)\n- 1x1 M9 Mixte (3€ par joueur)\nInscription directement sur place de 9h à 9h30.\nRepli en salles en cas de pluie.\nSur place vous trouverez également : \n- Buffet permanent\n- Grillades\n- Frites\n- Buvette \nPossibilité de régler en carte bleue",
        "publisher": "NSVB45"
    },
    {
        "events": [
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "4x4 Mixte"
                ],
                "level": [
                    "Loisir",
                    "Départemental",
                    "Régional",
                    "National"
                ]
            },
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "3x3 Féminin"
                ],
                "level": [
                    "Loisir",
                    "Départemental",
                    "Régional"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2367/rethel#amobile",
        "ground": "indoor",
        "new": False,
        "full": False,
        "night": False,
        "city": "Rethel",
        "department": 8,
        "id": 2367,
        "address": ", 08300 Rethel, France",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2367/rethel",
        "publisher": "Rik"
    },
    {
        "events": [
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "4x4 Mixte"
                ],
                "level": [
                    "Loisir"
                ]
            },
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "3x3 Masculin"
                ],
                "level": [
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro"
                ]
            },
            {
                "day": "25",
                "month": "05",
                "year": "2017",
                "timestamp": 1495663200.0,
                "formats": [
                    "3x3 Féminin"
                ],
                "level": [
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2308/massaguel#amobile",
        "ground": "grass",
        "new": False,
        "full": False,
        "night": False,
        "city": "Massaguel",
        "department": 81,
        "id": 2308,
        "address": "VILLAGE, 81110 Massaguel, France",
        "user": "Pascale VAISSIERE",
        "phone": "06 87 30 80 94",
        "website": "http://www.cmvb.net",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2308/massaguel",
        "terrains": 15,
        "inscription": "Prévente : 24€ par équipe\n\nA l'ordre de CMVB",
        "additional": "Buvette sur place\n1500€ de lots",
        "publisher": "CMVB"
    },
    {
        "events": [
            {
                "day": "27",
                "month": "05",
                "year": "2017",
                "timestamp": 1495836000.0,
                "formats": [
                    "3x3 Masculin"
                ],
                "level": [
                    "National",
                    "Pro"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2376/arles#amobile",
        "ground": "grass",
        "new": False,
        "full": False,
        "night": False,
        "city": "Arles",
        "department": 13,
        "id": 2376,
        "name": "3x3 Green \"TOREROS\" masculin",
        "address": "Stade des cités rue Pierre semard, 13200 Arles, France",
        "phone": "06.18.74.04.32",
        "website": "http://https://www.facebook.com/Volley-Ball-Arl%C3%A9sien-954533104677774/",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2376/arles",
        "hour": "09h30",
        "inscription": "Sur place : 30€ par équipe",
        "additional": "3x3 masculin sur herbe.\nEn cas de pluie gymnase de repli.\nBuvette et grillade sur place. Soirée et apéro après tournoi.",
        "publisher": "YohannVBA"
    },
    {
        "events": [
            {
                "day": "28",
                "month": "05",
                "year": "2017",
                "timestamp": 1495922400.0,
                "formats": [
                    "4x4 Mixte"
                ],
                "level": [
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2315/le-chesnay#amobile",
        "ground": "indoor",
        "new": False,
        "full": True,
        "night": False,
        "city": "Le chesnay",
        "department": 78,
        "id": 2315,
        "name": "Tournoi Cellois Chesnay",
        "address": "Gymnase nouvelle France - gymnase Duchesne, 78150 Le chesnay, France",
        "user": "Élodie Despierre",
        "phone": "06 24 44 04 28",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2315/le-chesnay",
        "hour": "8h30",
        "maxteams": 36,
        "terrains": 6,
        "inscription": "Prévente : 40€ par équipe\nSur place : 44€ par équipe\n\nA l'ordre de Cellois Chesnay Volley Hall \nA envoyer au Despierre Élodie 5 rue Pottier 78150 Le chesnay",
        "additional": "Venez nombreux pour notre 5eme tournoi Cellois-Chesnay.\nUne buvette dans chaque gymnase et de nombreux lots vous attendent.",
        "publisher": "Elodie"
    },
    {
        "events": [
            {
                "day": "28",
                "month": "05",
                "year": "2017",
                "timestamp": 1495922400.0,
                "formats": [
                    "3x3 Masculin"
                ],
                "level": [
                    "Loisir",
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro",
                    "Kids"
                ]
            },
            {
                "day": "28",
                "month": "05",
                "year": "2017",
                "timestamp": 1495922400.0,
                "formats": [
                    "3x3 Féminin"
                ],
                "level": [
                    "Loisir",
                    "Départemental",
                    "Régional",
                    "National",
                    "Pro",
                    "Kids"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2304/harnes#amobile",
        "ground": "indoor",
        "new": False,
        "full": False,
        "night": False,
        "city": "Harnes",
        "department": 62,
        "id": 2304,
        "name": "Squadra Cup Volley 2e édition",
        "address": "128 chemin Valois, 62440 Harnes, France",
        "user": "Harnes Volley-Ball",
        "phone": "0623693535",
        "website": "http://www.harnes-volleyball.fr",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2304/harnes",
        "maxteams": 50,
        "terrains": 10,
        "inscription": "Prévente : 10€ par joueur\nSur place : 15€ par joueur\n\nA l'ordre de Harnes Volley-Ball\nA envoyer au Harnes VB - Squadra Cup Volley - Salle Régionale Maréchal 128 Chemin Valois 62440 Harnes",
        "additional": "- Inscription via le site internet : www.harnes-volleyball.fr\n- 50 équipes max en Masc / 30 en Fém\n- 1 tee-shirt offert à chaque participant\n- Nombreux lots à gagner !\n- Barbeuc le midi et petite restauration : frites, sandwiches..\n- Parking gratuit\n- 3 Gymnases : Salle Régionale Maréchal, Complexe sportif André Bigotte, Gymnase du Collège Victor Hugo (à proximité de la salle Maréchal)\n- Ouverture : 9H rdv à la salle Maréchal\n- Inscription sur place jusqu'à 9H30 le 28/5\n- Début du tournoi à 9H45/10H\n- A 10 Minutes de Lens, accès routiers/autoroutiers à proximité (A1/A26/A21 N17)",
        "publisher": "HVB62"
    },
    {
        "events": [
            {
                "day": "28",
                "month": "05",
                "year": "2017",
                "timestamp": 1495922400.0,
                "formats": [
                    "3x3 Mixte"
                ],
                "level": [
                    "Loisir",
                    "Départemental"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2389/nogentlerotrou#amobile",
        "ground": "grass",
        "new": False,
        "full": False,
        "night": False,
        "city": "Nogent-le-rotrou",
        "department": 28,
        "id": 2389,
        "address": ", 28400 Nogent-le-rotrou, France",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2389/nogentlerotrou",
        "publisher": "Julioguss"
    },
    {
        "events": [
            {
                "day": "28",
                "month": "05",
                "year": "2017",
                "timestamp": 1495922400.0,
                "formats": [
                    "3x3 Mixte"
                ],
                "level": [
                    "Loisir"
                ]
            }
        ],
        "href": "http://www.accro-des-tournois.com/fichetournoi.html/2407/damelevieres#amobile",
        "ground": "grass",
        "new": True,
        "full": False,
        "night": False,
        "city": "Damelevières",
        "department": 54,
        "id": 2407,
        "name": "Tournoi de la Fête des Mères",
        "address": "Rue Doct Drouot, 54360 Damelevières, France",
        "phone": "0660927193",
        "mail": "http://www.accro-des-tournois.com/contactorga.html/2407/damelevieres",
        "hour": "9h00",
        "inscription": "Prévente : 12€ par équipe\nSur place : 14€ par équipe",
        "publisher": "Romane12"
    }
]

@get('/')
def get_tournaments():
    response.content_type = 'application/json'
    # return json.dumps(LIST_TOURNAMENTS, indent=4).encode()
    return LIST_TOURNAMENTS

@get('/department/<dpt:int>')
def get_tournaments(dpt):
    response.content_type = 'application/json'
    # return json.dumps([i for i in LIST_TOURNAMENTS if i["department"] == dpt], indent=4).encode()
    return [i for i in LIST_TOURNAMENTS if i["department"] == dpt]

@get('/id/<id>')
def get_tournaments(id):
    response.content_type = 'application/json'

    if id in LIST_TOURNAMENTS:
        return LIST_TOURNAMENTS[id]

    abort(404, "Tournament not found")


@post('/')
def post_tournaments():
    global LIST_TOURNAMENTS
    LIST_TOURNAMENTS = parse_tournaments()


if __name__ == "__main__":
    post_tournaments()
    run(host='localhost', port=8080, debug=True)