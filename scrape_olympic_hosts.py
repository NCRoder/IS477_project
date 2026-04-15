import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://en.wikipedia.org/wiki/List_of_Olympic_Games"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Get all wikitable tables
tables = soup.find_all("table", {"class": "wikitable"})

# First two tables = Summer & Winter
summer_table = tables[0]
winter_table = tables[1]


# Helpers for extracting based on regex
def extract_year(text):
    match = re.search(r"\b(18|19|20|21)\d{2}\b", text)
    return int(match.group()) if match else None


def clean_text(text):
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()


def clean_city(city):
    city = clean_text(city)
    city = re.sub(r"\s*(–|-|,| and )\s*", ";", city)
    return city


def detect_cancelled(text):
    text = text.lower()
    return any(k in text for k in ["cancelled", "canceled", "not held"])


def parse_table(table, season):
    data = []
    rows = table.find_all("tr")

    for row in rows:
        cells = row.find_all(["td", "th"])

        if len(cells) < 3:
            continue

        texts = [cell.get_text(" ", strip=True) for cell in cells]

        full_text = " ".join(texts)

        # Extract year from entire row
        year = extract_year(full_text)

        # Heuristic: first non-year text = city
        city = None
        country = None

        for t in texts:
            if not city and not re.search(r"\d{4}", t):
                city = clean_city(t)
                continue

            if city and not country:
                country = clean_text(t)
                break

        if not year:
            continue

        data.append({
            "year": year,
            "city": city,
            "country": country,
            "season": season,
            "games_label": f"{city} {year}" if city else f"Olympics {year}",
            "is_cancelled": detect_cancelled(full_text),
            "num_hosts": len(city.split(";")) if city else 0
        })

    return data


# Build dataset
data = []
data.extend(parse_table(summer_table, "Summer"))
data.extend(parse_table(winter_table, "Winter"))

df = pd.DataFrame(data)

df = df.drop_duplicates().sort_values(["year", "season"]).reset_index(drop=True)

# Save
df.to_csv("olympic_hosts_clean.csv", index=False)

print("✅ Rows:", len(df))