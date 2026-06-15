import sqlite3
import pandas as pd
from pathlib import Path

# Fix: Avoiding hard-coded paths (avoids common mistake ❌)
base_dir = Path(__file__).parent.parent
data_dir = base_dir / 'data' / 'processed'
db_dir = base_dir / 'data' / 'db'
sql_dir = base_dir / 'sql'

# Create folders if they don't exist
db_dir.mkdir(parents=True, exist_ok=True)
sql_dir.mkdir(parents=True, exist_ok=True)

db_path = db_dir / 'bluestock_mf.db'

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Assuming you have these processed CSVs. Adjust names as needed.
csv_files = {
    'fund_master': data_dir / '01_fund_master.csv',
    'nav_history': data_dir / '02_nav_history.csv'
    # Add your other CSVs here...
}

for table_name, file_path in csv_files.items():
    if file_path.exists():
        print(f"Loading {file_path.name} into table '{table_name}'...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)

# Dump the schema.sql (Fulfills folder structure requirement)
with open(sql_dir / 'schema.sql', 'w') as f:
    for line in conn.iterdump():
        f.write('%s\n' % line)

conn.close()
print(f"Database created at {db_path}")
print(f"Schema dumped to {sql_dir / 'schema.sql'}")