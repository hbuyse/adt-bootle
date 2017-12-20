#! /usr/bin/env python
# coding=utf-8

__author__ = "hbuyse"

import re
import datetime
import time
import sqlite3
import threading
import json

import requests
from bs4 import BeautifulSoup

# Regex that gives us the ID of the tournament
PATTERN_ID = re.compile(".*\/(?P<id>\d*)\/.*")
# Regex that gives us the city and the department of the tournament
PATTERN_CITY_DEP = re.compile("(?P<city>.*) \((?P<dpt>[A-Z0-9]{2})\)")
# Regex that gives us the address of the tournament
PATTERN_ADDRESS = re.compile("\'(?P<address>.*)\'")
#Regex that gives us the day, month and year of the tournament
PATTERN_DATE = re.compile(".* (?P<day>\d{1,2}) (?P<month>.*) (?P<year>\d{4})")
# Patterns that search for the other critical infos
PATTERN_HOUR = re.compile("Début du tournoi : ([0-9h]{2,5})")
PATTERN_GYMNASIUM = re.compile("(\d*) gymnases?/stades?")
PATTERN_TERRAINS = re.compile("(\d*) terrains")
PATTERN_MAXTEAMS = re.compile("(\d*) équipes max.")

LEVELS = {
    "Loisir": "loisir",
    "Départemental": "departemental",
    "Régional": "regional",
    "National": "national",
    "Pro": "pro",
    "Kids": "kids"
}

FORMATS = {
    "2x2 Masculin": "twoma",
    "2x2 Féminin": "twofe",
    "2x2 Mixte": "twomi",
    "3x3 Masculin": "threema",
    "3x3 Féminin": "threefe",
    "3x3 Mixte": "threemi",
    "4x4 Masculin": "fourma",
    "4x4 Féminin": "fourfe",
    "4x4 Mixte": "fourmi",
    "6x6 Masculin": "sixma",
    "6x6 Féminin": "sixfe",
    "6x6 Mixte": "sixmi"
}

def month_alpha_to_number(month):
    if month == "Janvier":
        return str(1)
    elif month == "Février":
        return str(2)
    elif month == "Mars":
        return str(3)
    elif month == "Avril":
        return str(4)
    elif month == "Mai":
        return str(5)
    elif month == "Juin":
        return str(6)
    elif month == "Juillet":
        return str(7)
    elif month == "Août":
        return str(8)
    elif month == "Septembre":
        return str(9)
    elif month == "Octobre":
        return str(10)
    elif month == "Novembre":
        return str(11)
    elif month == "Décembre":
        return str(12)
    else:
        return str(0)


class Tournament(object):
    """
    Class Tournament
    """
    def __init__(self, html_code):
        self.html_code = html_code
        self.infos = dict()

    def parse(self):
        self.infos = {
            'events': list(),

            # Get its URL and ID
            'href': self.html_code.find('a').get('href'),

            # Informations on the tournament
            'ground': self.html_code.find('a').get('class')[0].split('-')[0],
            'new': bool(re.search("new", self.html_code.find('a').get('class')[0])),
            'full': bool(re.search("complet", self.html_code.find('a').get('class')[0])),
            'night': bool(re.search("nuit", self.html_code.find('a').get('class')[0])),

            # Where does it take place?
            'city': re.search(PATTERN_CITY_DEP, self.html_code.find('h3').string).group("city").strip(),
            
            # No conversion to int since in France it can be 2A, 2B (Corsica) or 21
            'dpt': re.search(PATTERN_CITY_DEP, self.html_code.find('h3').string).group("dpt")
        }

        self.infos['id'] = int(re.search(PATTERN_ID, self.infos['href']).group("id"))

        u = requests.get(self.infos['href'])
        self.desc = BeautifulSoup(''.join([i.strip().replace('\t', '') for i in u.text.splitlines()]), 'html.parser')

        # Get the name and the address of the tournament
        try:
            self.infos['name'] = self.desc.find('div', attrs={"id": "libelletournoi"}).string.strip()
        except AttributeError as e:
            pass
        self.infos['address'] = re.search(PATTERN_ADDRESS, self.desc.find('div', attrs={"id": "tgmap"})['onclick']).group("address")

        # Get the name, the number of the person you have to contact
        # Get its website address and the address where to send a mail
        # Get the other informations that can be interesting
        tdetails = self.desc.find('div', attrs={"id": "tdetails"})
        for t in tdetails.find_all('p'):
            if re.search('usericon', str(t)):
                self.infos['user'] = t.get_text()
            elif re.search('phoneicon', str(t)):
                self.infos['phone'] = t.get_text().replace(' ', '')
            elif re.search('mouseicon', str(t)):
                self.infos['website'] = t.a.get('href')
            elif re.search('mailicon', str(t)):
                self.infos['mail'] = t.a.get('href')
            else:
                other_info = str(t).split('<br/>')
                for o in other_info:
                    if re.search(PATTERN_HOUR, o):
                        self.infos['hour'] = re.search(PATTERN_HOUR, o).group(1)
                    elif re.search(PATTERN_GYMNASIUM, o):
                        self.infos['gymnasium'] = int(re.search(PATTERN_GYMNASIUM, o).group(1))
                    elif re.search(PATTERN_TERRAINS, o):
                        self.infos['terrains'] = int(re.search(PATTERN_TERRAINS, o).group(1))
                    elif re.search(PATTERN_MAXTEAMS, o):
                        self.infos['maxteams'] = int(re.search(PATTERN_MAXTEAMS, o).group(1))

        # # Get the dates of the tournament, its formats and levels
        tlist = self.desc.find('ul', attrs={"id": "tlist"})
        for e in tlist.find_all('li', attrs={'class' : "elementtournoi"}):
            d = dict()
            r = re.match(PATTERN_DATE, e.h3.get_text().strip())
            if r:
                d['day'] = int(r.group("day"))
                d['month'] = int(month_alpha_to_number(r.group("month")))
                d['year'] = int(r.group("year"))

                s = "{}/{}/{}".format(r.group("day").zfill(2), month_alpha_to_number(r.group("month")).zfill(2), r.group("year"))
                d['timestamp'] = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())

                levels = [x.strip() for x in e.find('div').contents[2].split(', ')]
                formats =  [x.strip() for x in e.find('div').contents[0].split(', ')]
                for k, v in LEVELS.items():
                    d[v] = True if k in levels else False

                for k, v in FORMATS.items():
                    d[v] = True if k in formats else False

                self.infos['events'].append(d)

            if re.match("Inscriptions", e.h3.get_text().strip()):
                self.infos['inscription'] = BeautifulSoup(str(e.div).replace('<br/>', '\n'), 'html.parser').get_text().strip()

            if re.match("En savoir +", e.h3.get_text().strip()):
                # print("\n".join(e.div.strings))
                self.infos['additional'] = "\n".join([s.capitalize() for s in e.div.strings])

        self.infos['publisher'] = tlist.find('div', attrs={'class' : "align_right"}).a.get_text()


    def __str__(self):
        return "Tournament with ID {} in {} ({})".format(self.infos['id'],self.infos['city'], self.infos['dpt'])

    def __repr__(self):
        return "{}({})".format(self.__class__, self.infos['id'])

    def json(self):
        return self.infos


def download_main_page():
    content = str()
    r = requests.get("http://www.accro-des-tournois.com")
    
    if r.status_code == 200:
        content = ''.join([i.strip().replace('\t', '') for i in r.text.splitlines()])
    
    return content


def parse_tournaments():
    tournaments = list()
    s = BeautifulSoup(download_main_page(), 'html.parser')

    elements = s.find_all('li', attrs={"class" : "elementtournoi"})
    for e in elements:
        tournament = Tournament(e)
        tournament.parse()
        tournaments.append(tournament.json())

    return tournaments

if __name__ == '__main__':
    print(json.dumps(parse_tournaments(), indent=4, sort_keys=True))