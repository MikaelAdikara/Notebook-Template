# Auto-generated insights

## Data

- The training data contains 160,000 customers with an overall churn rate of 11.5% (moderate class imbalance).
- Post-event variables (acct_suspd_date_year, acct_suspd_date_month, acct_suspd_date_days_since, acct_suspd_date) were excluded to prevent target leakage.

## Drivers

- fe_tenure_band: customers in '0-6m' churn at 49.2% (4.3x the overall rate of 11.5%) versus 6.9% for '2-5y' (χ² p <0.001, Cramér's V = 0.39, IV = 0.93).
- cust_orig_date_month: churned customers have a median of 8.00 vs 9.00 for retained customers (weak/non-monotonic; rank-biserial r = -0.04, negligible effect, IV = 0.10). Highest-risk bin 6–7 churns at 20.5% (1.8x the average).
- fe_age_band: customers in '25-34' churn at 13.9% (1.2x the overall rate of 11.5%) versus 8.0% for '65+' (χ² p <0.001, Cramér's V = 0.06, IV = 0.04).
- No statistically significant association with churn after FDR correction for: latitude, home_market_value, county.
- The available data contain few directly controllable (actionable) variables; drivers are mainly customer characteristics, so recommendations focus on targeting and lifecycle timing rather than on changing specific policy features.
- Key non-actionable risk indicators useful for targeting: fe_tenure_band, fe_age_band, days_tenure.

## Segments

- High-risk segment: IF fe_tenure_band = 0-6m AND length_of_residence ≤ 10.50 AND has_children = 1 AND fe_premium_to_income ≤ 0.01 THEN churn rate = 52.8% (4.6x average; 3,258 customers, 2.0% of base, capturing 9.3% of all churners).
- High-risk segment: IF fe_tenure_band = 0-6m AND length_of_residence ≤ 10.50 AND has_children = 1 AND fe_premium_to_income > 0.01 THEN churn rate = 51.0% (4.4x average; 3,403 customers, 2.1% of base, capturing 9.4% of all churners).
- High-risk segment: IF fe_tenure_band = 0-6m AND length_of_residence ≤ 10.50 AND has_children = 0 THEN churn rate = 48.6% (4.2x average; 4,701 customers, 2.9% of base, capturing 12.4% of all churners).
- Most loyal segment: IF fe_tenure_band ≠ 0-6m AND fe_tenure_band ≠ 6-12m AND fe_tenure_band ≠ 1-2y AND latitude ≤ 33.13 THEN churn rate = 6.9% (122,559 customers).

## Survival

- Estimated probability of retaining a customer beyond 90 days: 98.6% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 180 days: 95.2% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 365 days: 94.3% (Kaplan-Meier).
- Churn hazard is highest in tenure interval [90, 180) days: about 1.17% of active customers churn per 30 days in this period (vs 0.10% on average).
- Cox model: fe_age_band = <25 has a hazard ratio of 2.48 (95% CI 1.11–5.53, p 0.026), i.e. +148% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 65+ has a hazard ratio of 0.44 (95% CI 0.40–0.47, p <0.001), i.e. -56% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 25-34 has a hazard ratio of 2.02 (95% CI 1.82–2.23, p <0.001), i.e. +102% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 35-44 has a hazard ratio of 1.38 (95% CI 1.29–1.49, p <0.001), i.e. +38% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 55-64 has a hazard ratio of 0.75 (95% CI 0.70–0.81, p <0.001), i.e. -25% churn hazard (vs '45-54'), holding other factors constant.

## Interpretable model

- Holding other factors constant, fe_tenure_band = 0-6m (vs '5y+') changes the odds of churn by +1163% (OR = 12.63, 95% CI 12.12–13.15, p <0.001; average marginal effect +21.9 pp).
- Holding other factors constant, fe_tenure_band = 6-12m (vs '5y+') changes the odds of churn by +184% (OR = 2.84, 95% CI 2.65–3.04, p <0.001; average marginal effect +9.0 pp).
- Holding other factors constant, fe_tenure_band = 1-2y (vs '5y+') changes the odds of churn by +52% (OR = 1.52, 95% CI 1.37–1.68, p <0.001; average marginal effect +3.6 pp).
- Holding other factors constant, fe_age_band = 65+ (vs '45-54') changes the odds of churn by -12% (OR = 0.88, 95% CI 0.84–0.93, p <0.001; average marginal effect -1.1 pp).

## Model

- The final model (mean_top3) achieves a cross-validated roc_auc of 0.7056 (ROC-AUC 0.7056) versus 0.50 for a random baseline.
- At the selected threshold (0.23) the model identifies 44.9% of churners (recall) with a precision of 49.3%, i.e. 4.3x better targeting than random selection.
- Final model ROC-AUC = 0.706 (95% bootstrap CI 0.701–0.710).
- The final model is not significantly different from the interpretable logistic regression (Δroc_auc = +0.0026, 95% CI -0.0009 to +0.0057).

## Explainability

- Partial dependence: moving days_tenure from 119.00 to 6.29K changes average predicted churn from 30.9% to 7.9%.
- Partial dependence: moving fe_tenure_years from 0.33 to 17.22 changes average predicted churn from 14.4% to 10.0%.
- Partial dependence: moving cust_orig_date_days_since from 119.00 to 6.29K changes average predicted churn from 11.6% to 11.0%.
- Partial dependence: moving length_of_residence from 0.00 to 15.00 changes average predicted churn from 11.9% to 10.6%.
- Partial dependence: moving age_in_years from 34.00 to 84.00 changes average predicted churn from 11.2% to 9.9%.
- Partial dependence: moving cust_orig_date_year from 2.00K to 2.02K changes average predicted churn from 11.2% to 11.2%.
- For marital_status = 'Married', the top churn drivers are days_tenure (46%), fe_tenure_years (13%), length_of_residence (6%).
- For marital_status = 'Single', the top churn drivers are days_tenure (47%), fe_tenure_years (14%), cust_orig_date_days_since (7%).

## Business

- Targeting the top 20% highest-risk customers captures 52.1% of all churners (2.6x lift over random targeting); the top decile churns at 50.0% vs 6.9% in the bottom decile. KS = 0.40.
- The High-risk tier (20% of customers, p ≥ 0.08) has an actual churn rate of 30.0% and contains 52.1% of all churners.
- Expected annual premium at risk from churn is 17.50M USD (11.6% of the annual premium base); the High-risk tier alone accounts for 49.8% of it.
- 'Priority Save' customers (high risk & above-median value) are 10.1% of the base but hold 31.8% of the value at risk — the first target for personalised retention.
- Simulated retention campaign (assumed success rate 25%, cost 25.00 USD per contact): targeting the top 10% ranked by 'Model: expected loss (p × value)' maximises net profit at 600.86K (ROI 1.5x), versus -178.30K for random targeting of the same size.

## Personas

- Persona P2 (82% of at-risk customers, actual churn 7.2%): risk driven mainly by no dominant driver (moderate, diffuse risk).
- Persona P1 (18% of at-risk customers, actual churn 46.0%): risk driven mainly by days_tenure (+1.34); fe_tenure_years (+0.39); cust_orig_date_days_since (+0.19).

## Recommendations

- 1. First-year onboarding programme — Welcome call, policy walkthrough, app activation and 90-day check-in for new customers; first renewal treated as a critical moment. Evidence: '0-6m' churns at 49.2% (4.3x avg); IV 0.93; OR 12.63; SHAP rank #10. KPI: 13th-month persistency ratio; first-year churn rate.
- 2. Life-stage tailored engagement — Tailor products, pricing communication and service channels to the highest-risk age groups (e.g. digital-first onboarding and flexible payment for younger customers; loyalty recognition for long-standing older customers). Evidence: '25-34' churns at 13.9% (1.2x avg); IV 0.04; OR 0.88; HR 0.44; SHAP rank #22. KPI: Churn rate by age band; adoption of tailored offers.
- 3. Investigate and act on 'cust_orig_date_days_since' — Customers with high-risk values of 'cust_orig_date_days_since' churn more; design a targeted intervention and test it in a pilot. Evidence: '22–191' churns at 47.7% (4.1x avg); IV 0.89; SHAP rank #3. KPI: Churn rate of the 'cust_orig_date_days_since' high-risk group.
- 4. Household-based cross-sell and life-event triggers — Use household profile and life events (moving, marriage, children) as triggers for coverage reviews and multi-policy bundles. Evidence: '0–1' churns at 13.0% (1.1x avg); IV 0.02; SHAP rank #4. KPI: Products per household; churn after life events.
- 5. Deploy a churn early-warning system — Score all active policies monthly with this model; route High-risk/Priority-Save customers to retention teams, lower tiers to automated digital nudges; refresh the model quarterly. Evidence: Model ROC-AUC 0.706; top-20% captures 52% of churners. Impact: optimal campaign: target top 10% → net 600.86K. KPI: Precision/recall of alerts; retained revenue vs control group.
- 6. Validate with controlled pilots (A/B tests) — For each intervention keep a random control group (e.g. 20% of targeted customers) to measure true uplift before scaling. Evidence: What-if results are associational. KPI: Uplift in retention rate (treated − control).

