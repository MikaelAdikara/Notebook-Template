# Auto-generated insights

## Data

- The training data contains 8,000 customers with an overall churn rate of 20.6% (moderate class imbalance).
- Post-event variables (cancellation_reason) were excluded to prevent target leakage.

## Drivers

- premium_change_pct: churned customers have a median of 6.20 vs 3.50 for retained customers (higher → more churn; rank-biserial r = 0.22, small effect, IV = 0.16). Highest-risk bin 12.9–29.5 churns at 31.7% (1.5x the average).
- tenure_months: churned customers have a median of 19.00 vs 24.00 for retained customers (higher → less churn; rank-biserial r = -0.19, small effect, IV = 0.13). Highest-risk bin 0.999–6 churns at 28.2% (1.4x the average).
- fe_claims_per_year: churned customers have a median of 0.24 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.16, small effect, IV = 0.11). Highest-risk bin 1.39–16 churns at 32.5% (1.6x the average).
- payment_method: customers in 'Cash' churn at 26.2% (1.3x the overall rate of 20.6%) versus 13.8% for 'Auto-debit' (χ² p <0.001, Cramér's V = 0.13, IV = 0.10).
- n_complaints_12m: churned customers have a median of 0.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.13, small effect, IV = 0.09). Highest-risk bin ≥2 churns at 39.3% (1.9x the average).
- late_payments_12m: churned customers have a median of 1.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.14, small effect, IV = 0.09). Highest-risk bin ≥3 churns at 43.6% (2.1x the average).
- auto_renew: customers in '0' churn at 26.0% (1.3x the overall rate of 20.6%) versus 16.3% for '1' (χ² p <0.001, Cramér's V = 0.12, IV = 0.09).
- fe_claim_reject_rate: churned customers have a median of 0.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.10, negligible effect, IV = 0.08). Highest-risk bin 0.5 churns at 34.4% (1.7x the average).
- claims_status_nunique: customers in '1' churn at 36.8% (1.8x the overall rate of 20.6%) versus 17.3% for 'Missing' (χ² p <0.001, Cramér's V = 0.11, IV = 0.07).
- avg_claim_settlement_days: churned customers have a median of 14.00 vs 13.00 for retained customers (higher → more churn; rank-biserial r = 0.08, negligible effect, IV = 0.07). Highest-risk bin 18–22 churns at 30.9% (1.5x the average).
- No statistically significant association with churn after FDR correction for: claims_days_since_last, claims_days_since_first, claims_claim_amount_min, claims_claim_amount_mean, claims_claim_amount_max, claims_claim_amount_std, age, annual_premium, marital_status, sum_insured, fe_sum_insured_to_premium, policy_start_date_month.
- Among churned customers, the most frequently stated reasons (cancellation_reason) were Moved (22%), Competitor offer (22%), Price (19%).
- Most robust actionable churn drivers (consistent across statistical tests, regression and SHAP): payment_method, auto_renew, premium_change_pct, n_products, late_payments_12m.
- Key non-actionable risk indicators useful for targeting: fe_claims_per_year, digital_engagement_score, policy_start_date_days_since.

## Segments

- High-risk segment: IF fe_claims_per_year > 0.44 AND payment_method ≠ Auto-debit AND n_complaints_12m > 0.50 AND auto_renew = 0 THEN churn rate = 57.9% (2.8x average; 221 customers, 2.8% of base, capturing 7.8% of all churners).
- High-risk segment: IF fe_claims_per_year > 0.44 AND payment_method ≠ Auto-debit AND n_complaints_12m > 0.50 AND auto_renew = 1 THEN churn rate = 37.8% (1.8x average; 286 customers, 3.6% of base, capturing 6.5% of all churners).
- High-risk segment: IF fe_claims_per_year > 0.44 AND payment_method ≠ Auto-debit AND n_complaints_12m ≤ 0.50 AND auto_renew = 0 THEN churn rate = 37.3% (1.8x average; 453 customers, 5.7% of base, capturing 10.2% of all churners).
- Most loyal segment: IF fe_claims_per_year ≤ 0.44 AND premium_change_pct ≤ 5.25 AND tenure_months > 61.50 AND n_products > 1.50 THEN churn rate = 1.4% (210 customers).

## Survival

- Estimated probability of retaining a customer beyond 6 months: 96.7% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 12 months: 92.7% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 24 months: 83.7% (Kaplan-Meier).
- Churn hazard is highest in tenure interval [18, 24) months: about 0.95% of active customers churn per month in this period (vs 0.71% on average).
- Cox model: payment_method = Bank Transfer has a hazard ratio of 1.75 (95% CI 1.54–1.99, p <0.001), i.e. +75% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: payment_method = Credit Card has a hazard ratio of 1.73 (95% CI 1.52–1.98, p <0.001), i.e. +73% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: payment_method = Cash has a hazard ratio of 1.67 (95% CI 1.40–1.98, p <0.001), i.e. +67% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: auto_renew has a hazard ratio of 0.63 (95% CI 0.57–0.70, p <0.001), i.e. -37% churn hazard (binary (0→1)), holding other factors constant.
- Cox model: premium_change_pct has a hazard ratio of 1.31 (95% CI 1.25–1.37, p <0.001), i.e. +31% churn hazard (per 1 SD (= 6.8)), holding other factors constant.

## Interpretable model

- Holding other factors constant, payment_method = Credit Card (vs 'Auto-debit') changes the odds of churn by +114% (OR = 2.14, 95% CI 1.83–2.51, p <0.001; average marginal effect +10.7 pp).
- Holding other factors constant, payment_method = Bank Transfer (vs 'Auto-debit') changes the odds of churn by +112% (OR = 2.12, 95% CI 1.82–2.47, p <0.001; average marginal effect +10.6 pp).
- Holding other factors constant, payment_method = Cash (vs 'Auto-debit') changes the odds of churn by +103% (OR = 2.03, 95% CI 1.65–2.51, p <0.001; average marginal effect +10.0 pp).
- Holding other factors constant, auto_renew (binary (0→1)) changes the odds of churn by -49% (OR = 0.51, 95% CI 0.45–0.57, p <0.001; average marginal effect -9.6 pp).
- Holding other factors constant, claims_status_nunique (binary (0→1)) changes the odds of churn by +77% (OR = 1.77, 95% CI 1.32–2.38, p <0.001; average marginal effect +8.0 pp).
- Holding other factors constant, tenure_months (per 1 SD (= 22.8)) changes the odds of churn by -37% (OR = 0.63, 95% CI 0.59–0.68, p <0.001; average marginal effect -6.5 pp).

## Model

- The final model (hill_climb) achieves a cross-validated roc_auc of 0.7488 (ROC-AUC 0.7488) versus 0.50 for a random baseline.
- At the selected threshold (0.24) the model identifies 60.9% of churners (recall) with a precision of 39.3%, i.e. 1.9x better targeting than random selection.
- Final model ROC-AUC = 0.749 (95% bootstrap CI 0.735–0.761).
- The final model is not significantly different from the interpretable logistic regression (Δroc_auc = +0.0025, 95% CI -0.0000 to +0.0057).

## Explainability

- Partial dependence: moving premium_change_pct from -7.40 to 15.50 changes average predicted churn from 15.7% to 24.8%.
- Partial dependence: moving n_products from 1.00 to 3.00 changes average predicted churn from 21.1% to 14.0%.
- Partial dependence: moving late_payments_12m from 0.00 to 2.00 changes average predicted churn from 17.6% to 26.0%.
- Partial dependence: moving fe_claims_per_year from 0.00 to 2.40 changes average predicted churn from 18.3% to 23.2%.
- Partial dependence: moving digital_engagement_score from 21.00 to 88.00 changes average predicted churn from 21.1% to 17.8%.
- Partial dependence: moving policy_start_date_days_since from 61.00 to 2.31K changes average predicted churn from 21.1% to 15.4%.
- For policy_type = 'Auto', the top churn drivers are payment_method (11%), auto_renew (10%), premium_change_pct (9%).
- For policy_type = 'Health', the top churn drivers are payment_method (11%), auto_renew (10%), premium_change_pct (9%).
- For policy_type = 'Life', the top churn drivers are payment_method (11%), auto_renew (10%), premium_change_pct (9%).
- For policy_type = 'Property', the top churn drivers are payment_method (11%), auto_renew (10%), premium_change_pct (9%).

## Business

- Targeting the top 20% highest-risk customers captures 44.5% of all churners (2.2x lift over random targeting); the top decile churns at 53.0% vs 4.0% in the bottom decile. KS = 0.37.
- The High-risk tier (20% of customers, p ≥ 0.31) has an actual churn rate of 45.9% and contains 44.5% of all churners.
- Expected annual premium at risk from churn is 9.83B IDR (20.5% of the annual premium base); the High-risk tier alone accounts for 41.8% of it.
- 'Priority Save' customers (high risk & above-median value) are 9.6% of the base but hold 28.3% of the value at risk — the first target for personalised retention.
- Simulated retention campaign (assumed success rate 30%, cost 150.00K IDR per contact): targeting the top 50% ranked by 'Model: expected loss (p × value)' maximises net profit at 792.88M (ROI 1.3x), versus 207.55M for random targeting of the same size.
- What-if: 'Move all 'payment_method' customers to 'Auto-debit'' affects 66% of customers and lowers their predicted churn from 22.8% to 14.9%; at 30% adoption this avoids ≈16 churners per 1,000 customers (model-based, associational).
- What-if: 'Set auto_renew = 1 for everyone' affects 44% of customers and lowers their predicted churn from 24.0% to 17.0%; at 30% adoption this avoids ≈9 churners per 1,000 customers (model-based, associational).
- What-if: 'Cap premium_change_pct at median (4)' affects 48% of customers and lowers their predicted churn from 23.9% to 19.9%; at 30% adoption this avoids ≈6 churners per 1,000 customers (model-based, associational).

## Personas

- Persona P1 (55% of at-risk customers, actual churn 35.8%): risk driven mainly by auto_renew (+0.25); payment_method (+0.07); premium_change_pct (+0.06).
- Persona P2 (45% of at-risk customers, actual churn 30.0%): risk driven mainly by payment_method (+0.11); premium_change_pct (+0.09); late_payments_12m (+0.04).

## Recommendations

- 1. Shift manual payers to automatic payment — Offer a small incentive (e.g. premium discount/cashback) and one-click enrolment for auto-debit/recurring card payment; send pre-due reminders to remaining manual payers. Evidence: 'Cash' churns at 26.2% (1.3x avg); IV 0.10; OR 2.12; HR 1.75; SHAP rank #1. Impact: -5.21 pp churn at full adoption (≈16 churners avoided /1,000 at 30% adoption). KPI: % of policies on auto-pay; lapse rate of converted vs control.
- 2. Make renewal effortless (default auto-renewal) — Default new and renewing policies to auto-renewal with clear opt-out; 30/14/7-day renewal reminders with a one-click renew link. Evidence: '0' churns at 26.0% (1.3x avg); IV 0.09; OR 0.51; HR 0.63; SHAP rank #2. Impact: -3.06 pp churn at full adoption (≈9 churners avoided /1,000 at 30% adoption). KPI: Auto-renew adoption; renewal rate.
- 3. Smarter renewal pricing — Cap or phase in premium increases for at-risk loyal customers, explain the value behind increases, and offer coverage/deductible adjustments instead of lapse. Evidence: '12.9–29.5' churns at 31.7% (1.5x avg); IV 0.16; OR 1.57; HR 1.31; SHAP rank #3. Impact: -1.95 pp churn at full adoption (≈6 churners avoided /1,000 at 30% adoption). KPI: Churn rate among customers with increases; price elasticity.
- 4. Bundling & cross-sell to raise switching costs — Offer multi-policy discounts and relevant riders to single-product customers with good risk profiles. Evidence: '1' churns at 23.7% (1.2x avg); IV 0.06; OR 0.73; HR 0.82; SHAP rank #4. KPI: Products per customer; churn of bundled vs single.
- 5. Early-warning on payment difficulty — Treat the first late payment as a churn signal: friendly reminders, flexible instalments or payment-date change, and grace-period outreach before lapse. Evidence: '≥3' churns at 43.6% (2.1x avg); IV 0.09; OR 1.36; HR 1.23; SHAP rank #6. Impact: -1.85 pp churn at full adoption (≈6 churners avoided /1,000 at 30% adoption). KPI: Cure rate of late payers; lapse after first missed payment.
- 6. Complaint recovery programme — Trigger a proactive call within 48h of any complaint, enforce resolution SLAs, offer service-recovery gestures to high-value complainants, and fix top root causes. Evidence: '≥2' churns at 39.3% (1.9x avg); IV 0.09; OR 1.30; HR 1.20; SHAP rank #7. Impact: -1.47 pp churn at full adoption (≈4 churners avoided /1,000 at 30% adoption). KPI: Complaint resolution time; churn rate of complainants.
- 7. Improve the claims experience — Fast-track settlement, explain rejections transparently with an appeal path, and assign a claims concierge for high-value / high-risk customers after a claim event. Evidence: '0.5' churns at 34.4% (1.7x avg); IV 0.08; OR 1.14; HR 1.05; SHAP rank #18. KPI: Claim settlement days; post-claim churn rate; claim NPS.
- 8. Deploy a churn early-warning system — Score all active policies monthly with this model; route High-risk/Priority-Save customers to retention teams, lower tiers to automated digital nudges; refresh the model quarterly. Evidence: Model ROC-AUC 0.749; top-20% captures 45% of churners. Impact: optimal campaign: target top 50% → net 792.88M. KPI: Precision/recall of alerts; retained revenue vs control group.
- 9. Validate with controlled pilots (A/B tests) — For each intervention keep a random control group (e.g. 20% of targeted customers) to measure true uplift before scaling. Evidence: What-if results are associational. KPI: Uplift in retention rate (treated − control).

