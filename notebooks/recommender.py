import pandas as pd
import os

def run_recommender():
    print("\n" + "="*50)
    print(" 🚀 Bluestock Mutual Fund Recommender 🚀 ")
    print("="*50)
    
    # Get user input
    risk_appetite = input("\nEnter your risk appetite (Low / Moderate / High): ").strip().capitalize()
    
    if risk_appetite not in ["Low", "Moderate", "High"]:
        print("❌ Invalid input. Defaulting to 'Moderate'.")
        risk_appetite = "Moderate"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Find the Master Fund CSV (usually one folder up)
    fund_master_path = os.path.join(script_dir, "..", "data", "processed", "01_fund_master.csv")
    if not os.path.exists(fund_master_path):
        fund_master_path = os.path.join(script_dir, "data", "processed", "01_fund_master.csv")

    # 2. Find the Scorecard CSV (Checking current folder first, then parent)
    scorecard_path = os.path.join(script_dir, "fund_scorecard.csv")
    if not os.path.exists(scorecard_path):
        scorecard_path = os.path.join(script_dir, "..", "fund_scorecard.csv")

    try:
        # Load the data sheets
        funds = pd.read_csv(fund_master_path)
        scorecard = pd.read_csv(scorecard_path)
        
        # Merge metrics with the master fund data
        merged = pd.merge(scorecard, funds[['amfi_code', 'risk_grade', 'category']], on='amfi_code')
        
        # Filter by the user's exact risk appetite
        filtered = merged[merged['risk_grade'] == risk_appetite]
        
        # Grab the top 3 funds based on their Sharpe Ratio
        top_3 = filtered.sort_values(by='sharpe_ratio', ascending=False).head(3)
        
        print(f"\n✅ Here are the Top 3 Funds for a {risk_appetite} Risk Profile:")
        print("-" * 50)
        
        for index, row in top_3.iterrows():
            print(f"🏆 {row['scheme_name']}")
            print(f"   Category: {row['category']} | Sharpe Ratio: {row['sharpe_ratio']:.2f} | Overall Score: {row['composite_score']:.1f}")
            print("-" * 50)
            
    except FileNotFoundError:
        print("❌ Error: Still could not locate the data files.")
        print(f"   Checked for Master Fund at: {os.path.abspath(fund_master_path)}")
        print(f"   Checked for Scorecard at: {os.path.abspath(scorecard_path)}")

if __name__ == "__main__":
    run_recommender()