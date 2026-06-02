import pandas as pd
import os

raw_data_dir = "data/raw"

def validate_data():
    print("--- Validating AMFI Codes ---")
    try:
        # Load the master list and the historical data
        fund_master = pd.read_csv(os.path.join(raw_data_dir, "fund_master.csv"))
        nav_history = pd.read_csv(os.path.join(raw_data_dir, "nav_history.csv"))
        
        # Extract unique codes
        master_codes = set(fund_master['scheme_code'].unique())
        nav_codes = set(nav_history['scheme_code'].unique())
        
        # Check what is missing
        missing_in_nav = master_codes - nav_codes
        
        print(f"Total AMFI codes in Fund Master: {len(master_codes)}")
        print(f"Total AMFI codes in NAV History: {len(nav_codes)}")
        
        if not missing_in_nav:
            print("Status: SUCCESS - All scheme codes in fund_master exist in nav_history.")
        else:
            print(f"Status: WARNING - {len(missing_in_nav)} codes from fund_master are missing in nav_history.")
            
    except FileNotFoundError as e:
        print(f"Error: Could not find necessary files for validation. {e}")

if __name__ == "__main__":
    validate_data()