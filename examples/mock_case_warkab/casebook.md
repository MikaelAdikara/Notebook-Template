# MOCK CASEBOOK (fiktif — untuk latihan & QA template)

## Data Analytics Competition — Final Stage 1: "Keeping Policyholders at PT Asuransi Nusantara Sejahtera"

### Background

PT Asuransi Nusantara Sejahtera (ANS) is a fictional multi-line insurer headquartered in Jakarta that sells life, health, motor and property
policies through agents, bancassurance partners, brokers and an online channel. ANS manages around 1.2 million active policies and booked
gross written premium of Rp 4.8 trillion in 2024.

Over the last two years ANS has seen policy non-renewal and lapse rise from 15.2% in 2022 to 20.6% in 2024. Management estimates that every
lost policyholder costs the company about Rp 1.1 million in unrecovered acquisition cost, and that renewal premiums represent 58% of total
premium income. The Board has asked the analytics team to explain who is leaving, when and why, and to propose a retention programme
for 2026 with a budget of Rp 1.5 billion.

ANS plans to launch a new self-service mobile app in Q1 2026 and is negotiating an auto-debit partnership with two national banks. The
company's agents currently receive commission only on new sales; a persistency bonus is being discussed.

### Data

The data cover customers whose policies were active at any time between January 2022 and June 2025 (snapshot date 30 June 2025).

- `train.csv` — 8,015 customers with the target column `churn` (Yes = the policy was not renewed or lapsed within the observation window).
- `test.csv` — 2,000 customers without the target.
- `claims.csv` — one row per claim (customer_id, claim_date, claim_amount, status).
- `sample_submission.csv` — customer_id, churn (probability).

| Column | Meaning |
|---|---|
| customer_id | unique customer identifier |
| age, gender, marital_status, dependents, region | customer profile |
| annual_income | declared annual income (Rp) |
| policy_type, coverage_level | product and coverage tier |
| sales_channel, agent_id | acquisition channel and servicing agent |
| payment_method, payment_frequency, auto_renew | billing set-up |
| policy_start_date, tenure_months | start of relationship and tenure |
| annual_premium, premium_change_pct, sum_insured | price and coverage |
| n_products | number of ANS products held |
| n_claims_3y, n_claims_rejected, avg_claim_settlement_days | claims experience in the last 3 years |
| n_complaints_12m, late_payments_12m | service and payment behaviour in the last 12 months |
| digital_engagement_score | 0–100 index of app/web activity |
| cancellation_reason | reason recorded by the call centre when the customer left |

### Tasks

1. Identify the main drivers of churn and quantify their effect.
2. Determine when during the customer lifecycle churn risk is highest.
3. Build a model that predicts churn for the customers in `test.csv` (evaluation metric: ROC-AUC).
4. Recommend a retention programme within the Rp 1.5 billion budget and estimate its financial impact.

Assume a profit margin of 20% of premium, a contact-and-incentive cost of Rp 150,000 per customer and a retention success rate of 30%
for contacted customers who would otherwise leave.

### Submission rules

Article max. 10 pages (excluding cover and attachments), A4, Times New Roman 12, 1.15 spacing, margins 4/4/3/3 cm, file name
`TeamName_Final Stage 1.pdf`; all files zipped with the same name.
