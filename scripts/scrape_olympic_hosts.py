import pandas as pd
import requests
import re
from io import StringIO
from datetime import datetime

def refine_olympic_data():
    """
    Scrapes Wikipedia for Olympic host cities and cleans the data:
    """
    url = "https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities"
    
    # Define headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Fetch the HTML
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Read tables into a list of DataFrames
        html_data = StringIO(response.text)
        tables = pd.read_html(html_data)
        
        # Locate the specific 'Host cities' table
        df = None
        for t in tables:
            cols = [str(c).strip() for c in t.columns.get_level_values(-1)]
            if 'City' in cols and 'Country' in cols:
                df = t
                break

        if df is None:
            print("Error: Could not locate the Olympic Host Cities table.")
            return None

        # 1. Standardize columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(-1)
        
        # Clean header strings and lowercase
        df.columns = [re.sub(r'\[.*?\]', '', str(col)).strip().lower() for col in df.columns]

        # 2. Fix the NaN City extraction
        # Wikipedia often uses a spacer column; we take the first valid 'city' column
        city_cols = [col for col in df.columns if 'city' in col]
        df['temp_city'] = df[city_cols].bfill(axis=1).iloc[:, 0]

        # 3. Clean and parse Year
        df['year_int'] = df['year'].astype(str).apply(
            lambda x: int(re.search(r'\d{4}', x).group()) if re.search(r'\d{4}', x) else None
        )
        df = df.dropna(subset=['year_int'])

        # 4. Identify Season (lowercase)
        def get_season(row):
            s = str(row.get('summer', '')).strip().lower()
            w = str(row.get('winter', '')).strip().lower()
            # Look for Roman Numerals or valid indicators
            if s and s not in ['nan', '—', ''] and any(c in s for c in 'ivxl'):
                return 'summer'
            if w and w not in ['nan', '—', ''] and any(c in w for c in 'ivxl'):
                return 'winter'
            return 'unknown'

        df['season_final'] = df.apply(get_season, axis=1)

        # 5. Assign Status: cancelled, postponed, complete, future
        # Current date: May 2026
        current_year = datetime.now().year 

        def get_status(row):
            row_str = " ".join([str(val) for val in row.values]).lower()
            year = int(row['year_int'])
            
            if 'cancelled' in row_str or '†' in row_str:
                return 'cancelled'
            if 'postponed' in row_str or '§' in row_str:
                return 'postponed'
            
            if year > current_year:
                return 'future'
            elif year < current_year:
                return 'complete'
            else:
                # 2026 Logic: Winter (Feb) is complete, Summer is future
                return 'complete' if row['season_final'] == 'winter' else 'future'

        df['status_final'] = df.apply(get_status, axis=1)

        def format_text(val):
            if pd.isna(val) or str(val).lower() == 'nan':
                return ""
            text = re.sub(r'\[.*?\]', '', str(val)).strip()
            return text

        # Build final dataframe
        df_clean = pd.DataFrame()
        df_clean['year'] = df['year_int'].astype(int)
        df_clean['city'] = df['temp_city'].apply(lambda x: format_text(x))
        df_clean['country'] = df['country'].apply(lambda x: format_text(x))
        df_clean['season'] = df['season_final']
        df_clean['status'] = df['status_final']

        # Filter out metadata rows and failed extractions
        df_clean = df_clean[df_clean['season'] != 'unknown']
        df_clean = df_clean[df_clean['city'] != ""]

        # Sort chronologically
        df_clean = df_clean.sort_values(['year', 'season'], ascending=[True, True])

        # Export
        output_file = "olympic_hosts_clean.csv"
        df_clean.to_csv(output_file, index=False)
        print(f"Success! Data exported to {output_file}")
        return df_clean

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    result = refine_olympic_data()
    if result is not None:
        print("\nFirst 5 rows:")
        print(result.head())
        print("\nLast 5 rows:")
        print(result.tail())