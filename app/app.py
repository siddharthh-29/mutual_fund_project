import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Bluestock MF Portfolio Optimizer")

# Get the path to the root folder (one level up from the 'app' folder)
root_dir = Path(__file__).resolve().parent.parent
data_path = root_dir / 'data' / 'processed' / '07_scheme_performance.csv'

# Load data
try:
    df = pd.read_csv(data_path)
    st.dataframe(df)
except FileNotFoundError:
    st.error(f"Could not find the file at: {data_path}. Please check your folder structure.")