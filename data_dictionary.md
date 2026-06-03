# Mutual Fund Data Warehouse: Data Dictionary

## Overview
This database uses a Star Schema design to store and analyze historical mutual fund performance, investor transactions, and daily NAV metrics.

---

## 1. Dimension Tables

### `dim_fund`
Stores static metadata and characteristics for every mutual fund scheme.
* **`amfi_code`** (INTEGER) - Primary Key. The unique identifier assigned by AMFI.
* **`fund_house`** (TEXT) - The Asset Management Company (AMC) managing the fund.
* **`scheme_name`** (TEXT) - The full registered name of the mutual fund.
* **`category`** (TEXT) - Broad asset class (e.g., Equity, Debt, Hybrid).
* **`sub_category`** (TEXT) - Specific investment focus (e.g., Large Cap, Liquid).
* **`plan`** (TEXT) - Investment route (Regular or Direct).
* **`launch_date`** (DATE) - The inception date of the scheme.
* **`benchmark`** (TEXT) - The market index used to evaluate the fund's performance.
* **`expense_ratio_pct`** (REAL) - The annual maintenance charge levied by the mutual fund (%).
* **`exit_load_pct`** (REAL) - The fee charged to investors for early redemption (%).
* **`min_sip_amount`** (REAL) - Minimum required investment for Systematic Investment Plans.
* **`min_lumpsum_amount`** (REAL) - Minimum required investment for a one-time purchase.
* **`fund_manager`** (TEXT) - The primary individual responsible for investment decisions.
* **`risk_category`** (TEXT) - Risk classification (e.g., Low, Moderate, Very High).
* **`sebi_category_code`** (TEXT) - The regulatory classification code.

### `dim_date`
Standardized date dimension for time-series analysis (to be populated in future ETL phases).
* **`date_id`** (DATE) - Primary Key. Standard YYYY-MM-DD format.
* **`year`** (INTEGER) - Extract of the year.
* **`month`** (INTEGER) - Extract of the month (1-12).
* **`day`** (INTEGER) - Extract of the day (1-31).
* **`day_of_week`** (TEXT) - Name of the day (Monday, Tuesday, etc.).
* **`is_weekend`** (BOOLEAN) - True if Saturday/Sunday, False otherwise.

---

## 2. Fact Tables

### `fact_nav`
Stores the daily Net Asset Value (NAV) for mutual funds.
* **`nav_id`** (INTEGER) - Primary Key. Auto-incremented identifier.
* **`amfi_code`** (INTEGER) - Foreign Key linking to `dim_fund`.
* **`date`** (DATE) - The date the NAV was recorded.
* **`nav`** (REAL) - The calculated Net Asset Value per unit on that date.

### `fact_transactions`
Logs individual investor purchase and redemption events.
* **`transaction_id`** (INTEGER) - Primary Key. Auto-incremented identifier.
* **`investor_id`** (TEXT) - Unique identifier for the retail investor.
* **`transaction_date`** (DATE) - The execution date of the transaction.
* **`amfi_code`** (INTEGER) - Foreign Key linking to `dim_fund`.
* **`transaction_type`** (TEXT) - Nature of the transaction (Sip, Lumpsum, Redemption).
* **`amount_inr`** (REAL) - The total financial value of the transaction in INR.
* **`state`** (TEXT) - The investor's residential state.
* **`city`** (TEXT) - The investor's residential city.
* **`city_tier`** (TEXT) - Geographic classification (e.g., T30, B30).
* **`age_group`** (TEXT) - Demographic age bracket of the investor.
* **`gender`** (TEXT) - Declared gender of the investor.
* **`annual_income_lakh`** (REAL) - Investor's declared annual income in Lakhs INR.
* **`payment_mode`** (TEXT) - Method of fund transfer (e.g., UPI, Net Banking, Mandate).
* **`kyc_status`** (TEXT) - Regulatory verification status of the investor.

### `fact_performance`
Stores aggregated historical return metrics and risk ratios.
* **`perf_id`** (INTEGER) - Primary Key. Auto-incremented identifier.
* **`amfi_code`** (INTEGER) - Foreign Key linking to `dim_fund`.
* **`scheme_name`** (TEXT) - Name of the fund.
* **`fund_house`** (TEXT) - The managing AMC.
* **`category`** (TEXT) - Broad asset class.
* **`plan`** (TEXT) - Investment route.
* **`return_1yr_pct`** (REAL) - 1-Year trailing return percentage.
* **`return_3yr_pct`** (REAL) - 3-Year annualized return percentage.
* **`return_5yr_pct`** (REAL) - 5-Year annualized return percentage.
* **`benchmark_3yr_pct`** (REAL) - 3-Year annualized return of the benchmark.
* **`alpha`** (REAL) - Measure of the fund's outperformance vs the benchmark.
* **`beta`** (REAL) - Measure of the fund's volatility relative to the market.
* **`sharpe_ratio`** (REAL) - Risk-adjusted return metric.
* **`sortino_ratio`** (REAL) - Downside risk-adjusted return metric.
* **`std_dev_ann_pct`** (REAL) - Annualized standard deviation (volatility).
* **`max_drawdown_pct`** (REAL) - Largest historical peak-to-trough drop.
* **`aum_crore`** (REAL) - Total Assets Under Management for the specific scheme.
* **`expense_ratio_pct`** (REAL) - Annual maintenance charge.
* **`morningstar_rating`** (INTEGER) - Independent 1-5 star rating.
* **`risk_grade`** (TEXT) - Standardized risk assessment.

### `fact_aum`
Tracks the total Assets Under Management aggregated at the Fund House level.
* **`aum_id`** (INTEGER) - Primary Key. Auto-incremented identifier.
* **`date`** (DATE) - The reporting date for the AUM snapshot.
* **`fund_house`** (TEXT) - The AMC managing the aggregated assets.
* **`aum_lakh_crore`** (REAL) - Total AUM formatted in Lakh Crores.
* **`aum_crore`** (REAL) - Total AUM formatted in Crores.
* **`num_schemes`** (INTEGER) - Total number of active schemes managed by the AMC on that date.