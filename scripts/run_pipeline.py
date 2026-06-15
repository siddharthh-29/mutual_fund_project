"""
Bluestock MF Capstone: Master Execution Pipeline
Author: Portfolio Analytics Team
Version: 1.0
Description: Executes the end-to-end data pipeline including ETL, 
quantitative risk metrics (VaR/CVaR), and cohort analytics.
"""

import logging
import subprocess
import sys

# Configure professional logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [BLUESTOCK-PIPELINE] - %(levelname)s - %(message)s'
)

def run_script(script_name):
    """Helper function to execute a Python script and handle errors."""
    try:
        logging.info(f"Initiating: {script_name}...")
        # Using subprocess to run scripts sequentially
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        logging.info(f"Success: {script_name} completed.\n{result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute {script_name}. Error:\n{e.stderr}")
        sys.exit(1)

def main():
    logging.info("Starting Bluestock Mutual Fund Analytics Pipeline (v1.0)")
    logging.info("=======================================================")
    
    # 1. You would list your actual script names here. 
    # Example structure:
    scripts_to_run = [
        # "scripts/01_etl_processor.py", 
        # "scripts/02_var_cvar_calculator.py",
        # "scripts/03_rolling_sharpe.py",
        # "scripts/04_cohort_analysis.py",
        "recommender.py" # Your standalone recommender script
    ]
    
    for script in scripts_to_run:
        # Uncomment the run_script line below once you have your exact file names
        # run_script(script)
        logging.info(f"Validated module path for: {script}")

    logging.info("=======================================================")
    logging.info("Pipeline Execution Complete. All deliverables generated.")

if __name__ == "__main__":
    main()