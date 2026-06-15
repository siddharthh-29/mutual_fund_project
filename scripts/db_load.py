import pandas as pd
from sqlalchemy import create_engine
import os

proc_dir = os.path.join("data", "processed")
db_path = "sqlite:///bluestock_mf.db"
schema_path = os.path.join("sql", "schema.sql")

def load_database():
    print("🚀 Starting Database Build...")
    
    # 1. Create connection
    engine = create_engine(db_path)
    
    # 2. Execute schema.sql to build empty tables
    try:
        with engine.connect() as connection:
            with open(schema_path, 'r') as file:
                sql_script = file.read()
                # SQLite executes scripts separated by semicolons
                for statement in sql_script.split(';'):
                    if statement.strip():
                        connection.exec_driver_sql(statement)
        print("✅ Schema created successfully.")
    except Exception as e:
        print(f"❌ Schema execution error: {e}")
        return

    # 3. Load Datasets into the Database
    files_to_load = {
        "01_fund_master.csv": "dim_fund",
        "02_nav_history.csv": "fact_nav",
        "07_scheme_performance.csv": "fact_performance",
        "08_investor_transactions.csv": "fact_transactions",
        "03_aum_by_fund_house.csv": "fact_aum"
    }

    for filename, table_name in files_to_load.items():
        filepath = os.path.join(proc_dir, filename)
        if os.path.exists(filepath):
            print(f"⏳ Loading {filename} into {table_name}...")
            try:
                # Read CSV
                df = pd.read_csv(filepath)
                
                # Push to SQL (append to existing empty tables, let pandas map columns)
                df.to_sql(table_name, con=engine, if_exists='append', index=False)
                
                # Verify rows
                print(f"  ✅ SUCCESS: {len(df)} rows inserted into '{table_name}'.")
            except Exception as e:
                print(f"  ❌ Error loading {table_name}: {e}")
        else:
            print(f"  ⚠️ Skipping {filename} - file not found.")

    print("\n🎉 Database loading complete! 'bluestock_mf.db' is ready.")

if __name__ == "__main__":
    load_database()