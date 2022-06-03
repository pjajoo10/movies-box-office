import os
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(__file__)

def url_to_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        html = BeautifulSoup(r.text, 'html.parser')
        return html
    return ""

def extract_data(url, year=None):
    if year == None:
        now = datetime.now()
        year = now.year
    
    html = url_to_html(url)
    table = html.find(id='table')
    if len(table) == 1:
        rows = table.find_all('tr')
        data = []
        for row in rows:
            data.append([x.text.strip() for x in row])

        header, values = data[0], data[1:]
        df = pd.DataFrame(values, columns=header)

        path = os.path.join(BASE_DIR, "data")
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join("data", f"{year}.csv")
        df.to_csv(filepath, index=False)


if __name__ == "__main__":
    year = 2022
    past_years = 5
    for i  in range(past_years):
        url = f"https://www.boxofficemojo.com/year/world/{year-i}/"
        extract_data(url, year-i)
