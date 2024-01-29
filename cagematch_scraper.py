import requests
from bs4 import BeautifulSoup

def create_wrestlers_query(wrestlers):
    participants = [''] * 4
    for i in range(min(4, len(wrestlers))):
        participants[i] = wrestlers[i].replace(' ', '+')
    query = '&'.join([f'sParticipant{i+1}={p}' for i, p in enumerate(participants)])
    return query

