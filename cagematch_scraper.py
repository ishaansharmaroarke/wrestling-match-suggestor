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


def pick_random_match(matches):
    try:
        soup = BeautifulSoup(matches.content, "html.parser")
        matches_table = soup.find("div", class_="TableContents")
        random_match = random.choice(
            matches_table.find_all("tr", class_=lambda c: c.startswith("TRow"))
        )
        return random_match
    except:
        return None


def extract_match_info(match, showResult=False):
    print(match)
    match_info = {}
    # date
    date = match.find("td", class_="TCol TColSeparator").text.strip()
    match_info["date"] = date

    # promotion
    promotion = match.find("img", class_="ImagePromotionLogoMini")["title"]
    match_info["promotion"] = promotion

    # image link
    image_link = match.find("img", class_="ImagePromotionLogoMini")["src"]
    match_info["image_link"] = "https://www.cagematch.net" + image_link.replace(
        "mini", "normal"
    )
    match_info["image_link"] = quote(match_info["image_link"], safe="/:")

    # match details
    match_details = match.find("span", class_="MatchCard").text.strip()
    match_info["match_details"] = match_details
    match_details_copy = match_details  # Create a copy of the original match_details
    print(match_details_copy)

    if not showResult:
        match_details_copy = (
            match_details_copy.replace("defeats", "vs")
            .replace("defeat", "vs")
            .replace("and", "vs")
            .split(" by ")[0]
            .strip()
        )
        match_details_copy = re.sub(r'\(\d.*', '', match_details_copy).strip()
        match_info["match_details"] = match_details_copy
    else:
        duration = re.search(r"\((.*?)\)", match_details).group(1)
        match_info["duration"] = duration
    # event
    event = match.find("div", class_="MatchEventLine").text.strip()
    match_info["event"] = event
    # winner
    match_info["result"] = match_details.split('defeat')[0].strip()
    return match_info
