import pandas as pd
import requests
import os

def download_data(url, target_path):
    print(f"Downloading data from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        raise Exception(f"Failed to download data. Status code: {response.status_code}")

def clean_data(raw_path, processed_path):
    print("Cleaning data...")
    df = pd.read_csv(raw_path)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Fill missing values for key metrics with 0 (assuming no report means 0 in many contexts)
    # For others like population, we keep them as is or forward fill
    metrics = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
               'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
    df[metrics] = df[metrics].fillna(0)
    
    # Filter out non-country entities (OWID uses some codes for continents/income groups)
    # Continent/Group codes often start with OWID_
    # We want to keep some of them for aggregate analysis but identify them
    
    # Save the cleaned data
    df.to_csv(processed_path, index=False)
    print(f"Cleaned data saved to {processed_path}")

if __name__ == "__main__":
    # Using the archived GitHub source as it's stable and comprehensive up to Aug 2024
    DATA_URLS = [
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
        "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
    ]
    RAW_PATH = "data/raw/owid-covid-data.csv"
    PROCESSED_PATH = "data/processed/cleaned_covid_data.csv"
    
    if not os.path.exists("data/raw"):
        os.makedirs("data/raw")
    if not os.path.exists("data/processed"):
        os.makedirs("data/processed")
    
    success = False
    for url in DATA_URLS:
        try:
            download_data(url, RAW_PATH)
            success = True
            break
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
    
    if success:
        clean_data(RAW_PATH, PROCESSED_PATH)
    else:
        print("All download attempts failed.")
