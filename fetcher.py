import requests
import pandas as pd
from io import StringIO
import json

def fetch_stations():
    CKAN_STATIONS_URL = "https://data.ca.gov/api/3/action/datastore_search"
    STATIONS_RESOURCE_ID = "98e628ff-d012-4982-ad32-b9f9ad8ab524"

    all_records = []
    offset = 0
    limit = 100
    filters = {
        "CountyName": "San Diego",
        "Status": "Active"
    }
    while True:
        params = {
            'resource_id': STATIONS_RESOURCE_ID,
            'filters': json.dumps(filters),
            'limit': limit,
            'offset': offset
        }
        response = requests.get(CKAN_STATIONS_URL, params=params)
        data = response.json()

        records = data['result']['records']
        if not records:
            break

        all_records.extend(records)
        offset += limit

    return all_records

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
