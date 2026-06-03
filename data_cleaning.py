import pandas as pd
import os
import shutil

raw_dir = os.path.join("data", "raw")
proc_dir = os.path.join("data", "processed")

# Ensure processed directory exists
os.makedirs(proc_dir, exist_ok=True)

def clean_nav_history():
    print("🧹 Cleaning 02_nav_history.csv...")
    try:
        df = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))
        
        # Parse dates
        df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['amfi_code', 'date'])
        
        # Sort by amfi_code and date
        df = df.sort_values(['amfi_code', 'date'])
        
        # Validate NAV > 0
        df = df[df['nav'] > 0]
        
        # Forward-fill missing NAV values (grouping by fund)
        df['nav'] = df.groupby('amfi_code')['nav'].ffill()
        
        df.to_csv(os.path.join(proc_dir, "02_nav_history.csv"), index=False)
        print("✅ NAV History cleaned and saved.")
    except Exception as e:
        print(f"❌ Error cleaning NAV History: {e}")

def clean_transactions():
    print("🧹 Cleaning 08_investor_transactions.csv...")
    try:
        df = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))
        
        # Fix date formats
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)
            
        # Standardize transaction_type (e.g., 'sip' -> 'Sip', 'LUMPSUM ' -> 'Lumpsum')
        if 'transaction_type' in df.columns:
            df['transaction_type'] = df['transaction_type'].str.strip().str.title()
            
        # Validate amount > 0
        if 'amount' in df.columns:
            df = df[df['amount'] > 0]
            
        df.to_csv(os.path.join(proc_dir, "08_investor_transactions.csv"), index=False)
        print("✅ Investor Transactions cleaned and saved.")
    except Exception as e:
        print(f"❌ Error cleaning Transactions: {e}")

def clean_performance():
    print("🧹 Cleaning 07_scheme_performance.csv...")
    try:
        df = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
        
        # Check expense_ratio range (0.1% - 2.5%)
        if 'expense_ratio' in df.columns:
            df['expense_ratio'] = pd.to_numeric(df['expense_ratio'], errors='coerce')
            df = df[(df['expense_ratio'] >= 0.1) & (df['expense_ratio'] <= 2.5)]
            
        df.to_csv(os.path.join(proc_dir, "07_scheme_performance.csv"), index=False)
        print("✅ Scheme Performance cleaned and saved.")
    except Exception as e:
        print(f"❌ Error cleaning Performance: {e}")

def transfer_other_files():
    print("📁 Transferring remaining datasets to processed folder...")
    files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    cleaned_files = ["02_nav_history.csv", "08_investor_transactions.csv", "07_scheme_performance.csv"]
    
    for file in files:
        if file not in cleaned_files:
            shutil.copy(os.path.join(raw_dir, file), os.path.join(proc_dir, file))
    print("✅ All 10 datasets are now in data/processed/")

if __name__ == "__main__":
    print("\n--- STARTING DAY 2 DATA CLEANING PIPELINE ---\n")
    clean_nav_history()
    clean_transactions()
    clean_performance()
    transfer_other_files()
    print("\n🎉 Data Cleaning Complete!")