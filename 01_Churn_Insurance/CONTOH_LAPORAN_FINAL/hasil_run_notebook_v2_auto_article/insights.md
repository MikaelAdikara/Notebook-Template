# Auto-generated insights

## Data

- The training data contains 160,000 customers with an overall churn rate of 11.7% (moderate class imbalance).
- Post-event variables (acct_suspd_date_year, acct_suspd_date_month, acct_suspd_date_days_since, acct_suspd_date) were excluded to prevent target leakage.

## Drivers

- fe_tenure_band: customers in '0-6m' churn at 48.8% (4.2x the overall rate of 11.7%) versus 7.1% for '5y+' (χ² p <0.001, Cramér's V = 0.38, IV = 0.89).
- cust_orig_date_month: churned customers have a median of 8.00 vs 9.00 for retained customers (weak/non-monotonic; rank-biserial r = -0.04, negligible effect, IV = 0.09). Highest-risk bin 6–7 churns at 20.1% (1.7x the average).
- age_in_years: churned customers have a median of 54.00 vs 55.00 for retained customers (higher → less churn; rank-biserial r = -0.09, negligible effect, IV = 0.04). Highest-risk bin 23–37 churns at 14.3% (1.2x the average).
- No statistically significant association with churn after FDR correction for: longitude, home_market_value, latitude, county, income, good_credit, marital_status.
- The available data contain few directly controllable (actionable) variables; drivers are mainly customer characteristics, so recommendations focus on targeting and lifecycle timing rather than on changing specific policy features.
- Key non-actionable risk indicators useful for targeting: fe_tenure_band, fe_age_band, days_tenure.

## Segments

- High-risk segment: IF fe_tenure_band = 0-6m AND cust_orig_date_month > 6.50 AND age_in_years ≤ 45.50 THEN churn rate = 50.9% (4.4x average; 5,105 customers, 3.2% of base, capturing 13.9% of all churners).
- High-risk segment: IF fe_tenure_band = 0-6m AND cust_orig_date_month > 6.50 AND age_in_years > 45.50 AND curr_ann_amt ≤ 994.28 THEN churn rate = 49.4% (4.2x average; 3,404 customers, 2.1% of base, capturing 9.0% of all churners).
- High-risk segment: IF fe_tenure_band = 0-6m AND cust_orig_date_month > 6.50 AND age_in_years > 45.50 AND curr_ann_amt > 994.28 THEN churn rate = 48.6% (4.2x average; 3,367 customers, 2.1% of base, capturing 8.8% of all churners).
- Most loyal segment: IF fe_tenure_band ≠ 0-6m AND fe_tenure_band ≠ 6-12m AND fe_tenure_band ≠ 1-2y AND latitude ≤ 32.85 THEN churn rate = 6.9% (77,717 customers).

## Survival

- Estimated probability of retaining a customer beyond 90 days: 98.6% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 180 days: 95.3% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 365 days: 94.4% (Kaplan-Meier).
- Churn hazard is highest in tenure interval [90, 180) days: about 1.16% of active customers churn per 30 days in this period (vs 0.10% on average).
- Cox model: fe_age_band = <25 has a hazard ratio of 4.23 (95% CI 2.19–8.14, p <0.001), i.e. +323% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 65+ has a hazard ratio of 0.48 (95% CI 0.45–0.52, p <0.001), i.e. -52% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 25-34 has a hazard ratio of 1.94 (95% CI 1.76–2.15, p <0.001), i.e. +94% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 55-64 has a hazard ratio of 0.75 (95% CI 0.70–0.81, p <0.001), i.e. -25% churn hazard (vs '45-54'), holding other factors constant.
- Cox model: fe_age_band = 35-44 has a hazard ratio of 1.33 (95% CI 1.24–1.43, p <0.001), i.e. +33% churn hazard (vs '45-54'), holding other factors constant.
- Restricted mean survival time (RMST, horizon 730 days): customers with fe_age_band = '<25' stay on average 57.9 days less than '65+' within the first 730 days (659.9 vs 717.9).
- Proportional-hazards diagnostics (Schoenfeld residual test): 2 of 6 terms show time-varying effects (p < 0.01); hazard ratios are therefore read as time-averaged effects and complemented by an accelerated failure time model.
- Accelerated failure time model: fe_age_band = <25 (vs '45-54') multiplies expected time-to-churn by 0.07 (95% CI 0.02–0.24), i.e. customers leave 93% sooner.
- Accelerated failure time model: fe_age_band = 25-34 (vs '45-54') multiplies expected time-to-churn by 0.46 (95% CI 0.38–0.56), i.e. customers leave 54% sooner.
- Accelerated failure time model: fe_age_band = 65+ (vs '45-54') multiplies expected time-to-churn by 2.08 (95% CI 1.83–2.37), i.e. customers leave 108% later.

## Interpretable model

- Holding other factors constant, fe_tenure_band = 0-6m (vs '5y+') changes the odds of churn by +1120% (OR = 12.20, 95% CI 11.72–12.71, p <0.001; average marginal effect +22.1 pp).
- Holding other factors constant, fe_tenure_band = 6-12m (vs '5y+') changes the odds of churn by +174% (OR = 2.74, 95% CI 2.56–2.94, p <0.001; average marginal effect +8.9 pp).
- Holding other factors constant, fe_tenure_band = 1-2y (vs '5y+') changes the odds of churn by +63% (OR = 1.63, 95% CI 1.47–1.79, p <0.001; average marginal effect +4.3 pp).
- Holding other factors constant, fe_age_band = 65+ (vs '45-54') changes the odds of churn by -8% (OR = 0.92, 95% CI 0.88–0.97, p 0.001; average marginal effect -0.7 pp).

## Model

- Ablation study: removing 'tenure' lowers ROC-AUC by 0.023 (95% CI 0.019 to 0.028, DeLong p <0.001), the largest contribution of any feature group.
- Engineered insurance features add -0.0013 ROC-AUC over the raw variables (DeLong p 0.346).
- The final model (hill_climb) achieves a cross-validated roc_auc of 0.7021 (ROC-AUC 0.7021) versus 0.50 for a random baseline.
- We ran 30 logged experiments across 6 stages (model zoo, tuning, multi-seed, feature selection, ablation, ensembling); ROC-AUC improved from 0.6960 (logistic regression baseline) to 0.7021 (final hill_climb).
- At the selected threshold (0.22) the model identifies 43.9% of churners (recall) with a precision of 48.9%, i.e. 4.2x better targeting than random selection.
- Final model ROC-AUC = 0.702 (95% bootstrap CI 0.698–0.707).
- The final model is significantly better than the interpretable logistic regression (Δroc_auc = +0.0061, 95% CI +0.0022 to +0.0102).
- Across 12 candidate models, the final model's ROC-AUC is 0.702 (95% DeLong CI 0.697–0.707); it is significantly better than 6 of them after Holm correction.
- Profit-based evaluation (EMPC; Verbraken et al., 2013) differs from the AUC ranking: the most profitable model is hgb with an expected maximum profit of 4.32 USD per customer when targeting about 10.8% of the base.
- The interpretable logistic regression reaches ROC-AUC 0.696; the gap to the final model is +0.0061 (DeLong p 0.002).
- A glass-box Explainable Boosting Machine attains ROC-AUC 0.693 (Δ vs final +0.0089, DeLong p <0.001), offering a fully transparent alternative for regulated use.
- The out-of-fold risk score also orders customers by time to churn (Harrell's C-index 0.819); survival curves of the three risk tiers separate clearly (log-rank p <0.001).

## Explainability

- Partial dependence: moving days_tenure from 121.00 to 6.29K changes average predicted churn from 30.2% to 8.0%.
- Partial dependence: moving fe_tenure_years from 0.33 to 17.22 changes average predicted churn from 14.5% to 10.0%.
- Partial dependence: moving cust_orig_date_days_since from 121.00 to 6.29K changes average predicted churn from 11.6% to 10.9%.
- Partial dependence: moving length_of_residence from 0.00 to 15.00 changes average predicted churn from 11.8% to 10.7%.
- Partial dependence: moving latitude from 32.56 to 33.18 changes average predicted churn from 10.8% to 11.1%.
- Partial dependence: moving age_in_years from 34.00 to 83.00 changes average predicted churn from 11.1% to 9.9%.
- For marital_status = 'Married', the top churn drivers are days_tenure (51%), fe_tenure_years (15%), cust_orig_date_days_since (7%).
- For marital_status = 'Single', the top churn drivers are days_tenure (52%), fe_tenure_years (15%), cust_orig_date_days_since (6%).

## Business

- Targeting the top 20% highest-risk customers captures 51.1% of all churners (2.6x lift over random targeting); the top decile churns at 49.4% vs 7.0% in the bottom decile. KS = 0.39.
- The High-risk tier (20% of customers, p ≥ 0.07) has an actual churn rate of 28.0% and contains 52.6% of all churners.
- Expected annual premium at risk from churn is 17.81M USD (11.8% of the annual premium base); the High-risk tier alone accounts for 53.5% of it.
- 'Priority Save' customers (high risk & above-median value) are 11.4% of the base but hold 34.6% of the value at risk — the first target for personalised retention.
- Simulated retention campaign (assumed success rate 25%, cost 25.00 USD per contact): targeting the top 10% ranked by 'Model: expected loss (p × value)' maximises net profit at 590.81K (ROI 1.5x), versus -175.96K for random targeting of the same size.

## Personas

- Persona P2 (79% of at-risk customers, actual churn 8.5%): risk driven mainly by no dominant driver (moderate, diffuse risk).
- Persona P1 (21% of at-risk customers, actual churn 51.9%): risk driven mainly by days_tenure (+1.29); fe_tenure_years (+0.38); cust_orig_date_days_since (+0.17).

## Governance

- Fairness audit across age band, has children, marital status: predicted risk tracks actual churn within each group (largest calibration ratio deviation: fe_age_band = '<25', 1.22); the largest within-attribute AUC gap is 0.162. Differences in High-tier selection reflect genuine differences in churn rates; the score is intended for retention outreach only, not for pricing or underwriting.

## Recommendations

- 1. First-year onboarding programme — Welcome call, policy walkthrough, app activation and 90-day check-in for new customers; first renewal treated as a critical moment. Evidence: '0-6m' churns at 48.8% (4.2x avg); IV 0.89; OR 12.20; SHAP rank #10. KPI: 13th-month persistency ratio; first-year churn rate.
- 2. Life-stage tailored engagement — Tailor products, pricing communication and service channels to the highest-risk age groups (e.g. digital-first onboarding and flexible payment for younger customers; loyalty recognition for long-standing older customers). Evidence: '25-34' churns at 14.6% (1.2x avg); IV 0.04; OR 0.92; HR 0.48; SHAP rank #16. KPI: Churn rate by age band; adoption of tailored offers.
- 3. Household-based cross-sell and life-event triggers — Use household profile and life events (moving, marriage, children) as triggers for coverage reviews and multi-policy bundles. Evidence: '0–1' churns at 13.5% (1.2x avg); IV 0.01; SHAP rank #4. KPI: Products per household; churn after life events.
- 4. Deploy a churn early-warning system — Score all active policies monthly with this model; route High-risk/Priority-Save customers to retention teams, lower tiers to automated digital nudges; refresh the model quarterly. Evidence: Model ROC-AUC 0.702; top-20% captures 51% of churners. Impact: optimal campaign: target top 10% → net 590.81K. KPI: Precision/recall of alerts; retained revenue vs control group.
- 5. Validate with controlled pilots (A/B tests) — For each intervention keep a random control group (e.g. 20% of targeted customers) to measure true uplift before scaling. Evidence: What-if results are associational. KPI: Uplift in retention rate (treated − control).
- Pilot design: to detect a 3.5 pp reduction from a baseline of 28.0% in the High-risk tier ('Generic retention offer'), a randomised test needs 2,481 customers per arm (α = 0.05, power 80%), i.e. 75% of the High-tier portfolio.

