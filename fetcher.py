import requests
import pandas as pd
from io import StringIO
import json
from bs4 import BeautifulSoup

def fetch_stations():
    station_url = "https://beachwatch.waterboards.ca.gov/public/getstation.php"
    
    station_response = requests.post(
        station_url,
        data={'county': '10'}
    )
    
    soup = BeautifulSoup(station_response.text, 'html.parser')
    options = soup.find_all("option")
    
    stations = []
    for option in options:
        name = option.text.strip()
        if name == "All Stations":
            continue
        stations.append(name)
    
    return stations

def fetch_advisories():
    session = requests.Session()
    search_url = "https://beachwatch.waterboards.ca.gov/public/advisory.php"
    export_url = "https://beachwatch.waterboards.ca.gov/public/export.php"

    search_response = session.post(
        search_url,
        data={
            'County': '10',
            'year': '',
            'type': '',
            'cause': '',
            'source': '',
            'substance': '',
            'created': '',
            'sort': '`Start Date`',
            'sortOrder': 'DESC',
            'submit': 'Search'
        }
    )


    export_response = session.get(export_url)

    content = export_response.content.decode('utf-8')
    df = pd.read_csv(StringIO(content), sep='\t')
    df.columns = df.columns.str.strip()

    json_str = df.to_json(orient='records')
    if json_str is None:
        return []

    advisories = json.loads(json_str)

    filtered_advisories = []
    for advisory in advisories:
        if advisory.get('Station Name') is not None:
            filtered_advisories.append(advisory)

    return filtered_advisories
