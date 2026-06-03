-- 1. Top 5 Funds by AUM (Required)
SELECT fund_house, aum_crore 
FROM fact_aum 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month for a specific fund (Required)
SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav 
FROM fact_nav 
WHERE amfi_code = 125497 -- HDFC Top 100
GROUP BY strftime('%Y-%m', date)
ORDER BY month DESC;

-- 3. Total SIP Transactions by State (Required)
SELECT state, COUNT(transaction_id) as total_sips, SUM(amount_inr) as total_invested
FROM fact_transactions 
WHERE transaction_type = 'Sip'
GROUP BY state 
ORDER BY total_invested DESC;

-- 4. Funds with an Expense Ratio less than 1% (Required)
SELECT scheme_name, category, expense_ratio_pct 
FROM dim_fund 
WHERE expense_ratio_pct < 1.0 
ORDER BY expense_ratio_pct ASC;

-- 5. Top 5 Best Performing Funds over 3 Years
SELECT scheme_name, fund_house, return_3yr_pct 
FROM fact_performance 
ORDER BY return_3yr_pct DESC 
LIMIT 5;

-- 6. Investor Demographics: Transactions by Age Group
SELECT age_group, COUNT(transaction_id) as transaction_count, SUM(amount_inr) as total_volume
FROM fact_transactions
GROUP BY age_group
ORDER BY total_volume DESC;

-- 7. Lumpsum vs SIP Total Investment Volume
SELECT transaction_type, SUM(amount_inr) as total_amount, AVG(amount_inr) as avg_transaction_size
FROM fact_transactions
GROUP BY transaction_type;

-- 8. Highest Risk Funds with their 1-Year Return
SELECT f.scheme_name, f.risk_category, p.return_1yr_pct
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE f.risk_category = 'Very High'
ORDER BY p.return_1yr_pct DESC
LIMIT 10;

-- 9. Number of active schemes per Fund House
SELECT fund_house, COUNT(amfi_code) as total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;

-- 10. Most preferred Payment Mode for Investments
SELECT payment_mode, COUNT(transaction_id) as usage_count
FROM fact_transactions
GROUP BY payment_mode
ORDER BY usage_count DESC;