import requests
import pandas as pd
from sqlalchemy import create_engine

##Step 1: Importing data

url = 'https://restcountries.com/v3.1/independent?status=true&fields=name,cca2,independent,languages,capital,region,subregion,borders,area,population,gini,timezones,continents,flags'

try:
    r = requests.get(url, timeout=10)  # timeout in seconds
    r.raise_for_status()  # raising error for bad responses
    json_data = r.json()
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
    exit(1)
except ValueError as e:
    print(f"❌ Failed to parse JSON: {e}")
    exit(1)

rows = []

for i, country in enumerate(json_data):
    
    gini_data = country.get('gini', {}) ##extracting the last available gini year
    if gini_data:
        latest_year = max(gini_data, key=lambda year: int(year))
        latest_value = gini_data[latest_year]
        gini_combined = f"{latest_year}: {latest_value}"
    else:
        gini_combined = "N/A"

    country_dict = {
        "id": i,
        "name": country.get('name', {}).get('common', 'N/A'),
        "official_name": country.get('name', {}).get('official', 'N/A'),
        "country_code": country.get('cca2', 'N/A'),
        "is_independent": country.get('independent', 'N/A'),
        "capital": country.get('capital', ['N/A'])[0],
        "region": country.get('region', 'N/A'),
        "subregion": country.get('subregion', 'N/A'),
        "bordering_countries": ', '.join(country.get('borders', [])) or 'None',  ## .join is used because of multiple possible values
        "area_in_km2": country.get('area', 'N/A'), 
        "population": country.get('population', 'N/A'),
        "gini": gini_combined,
        "timezones": ', '.join(country.get('timezones', [])), ## .join is used because of multiple possible values
        "continents": ', '.join(country.get('continents', [])),
        "languages": ', '.join(country.get('languages', {}).values()), ## .values() is used because in the API, languages returns a dict of languages such as  "eng": "English" etc.
        "flag_description": country.get('flags', {}).get('alt', 'N/A'),
        "flag_url": country.get('flags', {}).get('png', 'N/A')
    }

    rows.append(country_dict)

df = pd.DataFrame(rows)

##Step 2 : Loading the data frame to the Postgres db after creating the docker file

engine = create_engine('postgresql://clarkkent:superman@localhost:5432/countriesdb')

try:
    df.to_sql('countries', engine, if_exists='replace', index=False)
    print("Data written to the DB")
except Exception as e:
    print(f"Errow writing to the DB")

