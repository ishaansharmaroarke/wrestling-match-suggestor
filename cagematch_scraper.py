import requests
from bs4 import BeautifulSoup

def create_wrestlers_query(wrestlers):
    participants = [''] * 4
    for i in range(min(4, len(wrestlers))):
        participants[i] = wrestlers[i].replace(' ', '+')
    query = '&'.join([f'sParticipant{i+1}={p}' for i, p in enumerate(participants)])
    return query

def get_wrestling_match(wrestlers, before_year, after_year):
    contains_wrestlers = create_wrestlers_query(wrestlers)

    URL = f"https://www.cagematch.net/?id=112&view=search&{contains_wrestlers}&sEventName=&sEventType=TV-Show%7CPay+Per+View%7CPremium+Live+Event%7COnline+Stream&sDateFromDay=01&sDateFromMonth=01&sDateFromYear={before_year}&sDateTillDay=31&sDateTillMonth=12&sDateTillYear={after_year}&sPromotion=&sLocation=&sArena=&sRegion=&sMatchType=&sConstellation=&sWorkerRelationship=Any&sFulltextSearch="
    print(URL)
