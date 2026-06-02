import pandas as pd
import os

raw_data_dir = "data/raw"

def validate_data():
    print("--- Validating AMFI Codes ---")
    try:
        # Load files
        fund_master = pd.read_csv(os.path.join(raw_data_dir, "01_fund_master.csv"))
        nav_history = pd.read_csv(os.path.join(raw_data_dir, "02_nav_history.csv"))
        
        # Print actual columns so we can visually inspect them if it fails
        print("\n🔍 Actual columns in Fund Master:", list(fund_master.columns))
        print("🔍 Actual columns in NAV History:", list(nav_history.columns))
        
        # Dynamically scan for any column containing 'scheme' or 'code' (case-insensitive)
        master_col_matches = [c for c in fund_master.columns if 'scheme' in c.lower() or 'code' in c.lower()]
        nav_col_matches = [c for c in nav_history.columns if 'scheme' in c.lower() or 'code' in c.lower()]
        
        # Pick the best match found, fallback to 'scheme_code' if none
        m_col = master_col_matches[0] if master_col_matches else 'scheme_code'
        n_col = nav_col_matches[0] if nav_col_matches else 'scheme_code'
        
        print(f"\n🎯 Using Column '{m_col}' for Master and '{n_col}' for NAV History...")
        
        # Extract unique codes
        master_codes = set(fund_master[m_col].unique())
        nav_codes = set(nav_history[n_col].unique())
        
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
    except KeyError as e:
        print(f"❌ Column Error: Could not find the column name {e}. Check the exact spelling above.")

if __name__ == "__main__":
    validate_data()