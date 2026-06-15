import requests
import pandas as pd
import os

# Ensure raw data directory exists
raw_data_dir = "data/raw"
os.makedirs(raw_data_dir, exist_ok=True)

def fetch_and_save_nav(scheme_code, filename):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for scheme: {scheme_code}...")
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Extract the 'data' payload which contains the historical NAVs
        nav_data = data.get("data", [])
        if nav_data:
            df = pd.DataFrame(nav_data)
            filepath = os.path.join(raw_data_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"Success: Saved to {filepath}")
        else:
            print(f"Warning: No NAV data found for {scheme_code}")
    else:
        print(f"Error: Failed to fetch {scheme_code}. Status code: {response.status_code}")

if __name__ == "__main__":
    # 1. Fetch HDFC Top 100 Direct
    fetch_and_save_nav(125497, "hdfc_top_100_125497.csv")
    
    # 2. Fetch the 5 key schemes
    key_schemes = {
        119551: "sbi_bluechip.csv",
        120503: "icici_bluechip.csv",
        118632: "nippon_large_cap.csv",
        119092: "axis_bluechip.csv",
        120841: "kotak_bluechip.csv"
    }
    
    for code, filename in key_schemes.items():
        fetch_and_save_nav(code, filename)