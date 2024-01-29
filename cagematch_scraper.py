import requests
from bs4 import BeautifulSoup
import random
import re
from urllib.parse import quote


def create_wrestlers_query(wrestlers):
    participants = [""] * 4
    for i in range(min(4, len(wrestlers))):
        participants[i] = wrestlers[i].replace(" ", "+")
    query = "&".join([f"sParticipant{i+1}={p}" for i, p in enumerate(participants)])
    return query


def get_wrestling_matches(wrestlers, after_year, before_year):
    session = requests.Session()
    session.headers.update({"Accept-Encoding": "identity"})
    contains_wrestlers = create_wrestlers_query(wrestlers)

    URL = f"https://www.cagematch.net/?id=112&view=search&{contains_wrestlers}&sEventName=&sEventType=TV-Show%7CPay+Per+View%7CPremium+Live+Event%7COnline+Stream&sDateFromDay=01&sDateFromMonth=01&sDateFromYear={after_year}&sDateTillDay=31&sDateTillMonth=12&sDateTillYear={before_year}&sPromotion=&sLocation=&sArena=&sRegion=&sMatchType=&sConstellation=&sWorkerRelationship=Any&sFulltextSearch="

    cagematch_results = session.get(URL)
    return cagematch_results


