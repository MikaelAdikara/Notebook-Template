# Auto-generated insights

## Data

- The training data contains 8,000 customers with an overall churn rate of 21.1% (moderate class imbalance).
- Post-event variables (cancellation_reason) were excluded to prevent target leakage.

## Drivers

- premium_change_pct: churned customers have a median of 6.60 vs 3.60 for retained customers (higher → more churn; rank-biserial r = 0.23, small effect, IV = 0.16). Highest-risk bin 13.2–30.6 churns at 33.5% (1.6x the average).
- tenure_months: churned customers have a median of 18.00 vs 25.00 for retained customers (higher → less churn; rank-biserial r = -0.20, small effect, IV = 0.15). Highest-risk bin 1–6 churns at 28.6% (1.4x the average).
- fe_claims_per_year: churned customers have a median of 0.27 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.18, small effect, IV = 0.13). Highest-risk bin 1.5–24 churns at 34.9% (1.7x the average).
- fe_claim_reject_rate: churned customers have a median of 0.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.12, small effect, IV = 0.12). Highest-risk bin 1 churns at 37.1% (1.8x the average).
- n_complaints_12m: churned customers have a median of 0.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.14, small effect, IV = 0.11). Highest-risk bin ≥2 churns at 44.3% (2.1x the average).
- avg_claim_settlement_days: churned customers have a median of 14.00 vs 13.00 for retained customers (higher → more churn; rank-biserial r = 0.12, small effect, IV = 0.10). Highest-risk bin 21–28 churns at 34.6% (1.6x the average).
- payment_method: customers in 'Bank Transfer' churn at 25.5% (1.2x the overall rate of 21.1%) versus 14.2% for 'Auto-debit' (χ² p <0.001, Cramér's V = 0.12, IV = 0.10).
- auto_renew: customers in '0' churn at 26.4% (1.3x the overall rate of 21.1%) versus 16.7% for '1' (χ² p <0.001, Cramér's V = 0.12, IV = 0.08).
- claims_status_nunique: customers in '1' churn at 34.8% (1.7x the overall rate of 21.1%) versus 17.1% for 'Missing' (χ² p <0.001, Cramér's V = 0.12, IV = 0.08).
- claims_count: churned customers have a median of 1.00 vs 0.00 for retained customers (higher → more churn; rank-biserial r = 0.14, small effect, IV = 0.08). Highest-risk bin ≥3 churns at 32.8% (1.6x the average).
- No statistically significant association with churn after FDR correction for: claims_claim_amount_max, claims_days_since_last, claims_days_since_first, claims_claim_amount_mean, claims_claim_amount_min, claims_claim_amount_std, age, policy_start_date_month, annual_premium, sum_insured, marital_status, region.
- Among churned customers, the most frequently stated reasons (cancellation_reason) were Moved (21%), Price (21%), Competitor offer (20%).
- Most robust actionable churn drivers (consistent across statistical tests, regression and SHAP): premium_change_pct, payment_method, auto_renew, n_complaints_12m, avg_claim_settlement_days.
- Key non-actionable risk indicators useful for targeting: tenure_months, digital_engagement_score, fe_claims_per_year.

## Segments

- High-risk segment: IF fe_claims_per_year > 0.41 AND premium_change_pct > 3.85 AND payment_method ≠ Auto-debit AND fe_claim_reject_rate > 0.12 THEN churn rate = 55.3% (2.6x average; 266 customers, 3.3% of base, capturing 8.7% of all churners).
- High-risk segment: IF fe_claims_per_year > 0.41 AND premium_change_pct ≤ 3.85 AND fe_claim_reject_rate > 0.58 THEN churn rate = 38.3% (1.8x average; 209 customers, 2.6% of base, capturing 4.7% of all churners).
- High-risk segment: IF fe_claims_per_year ≤ 0.41 AND premium_change_pct > 6.55 AND payment_method ≠ Auto-debit AND tenure_months ≤ 26.50 THEN churn rate = 37.3% (1.8x average; 590 customers, 7.4% of base, capturing 13.0% of all churners).
- Most loyal segment: IF fe_claims_per_year ≤ 0.41 AND premium_change_pct ≤ 6.55 AND auto_renew = 1 AND n_products > 1.50 THEN churn rate = 6.1% (885 customers).

## Survival

- Estimated probability of retaining a customer beyond 6 months: 96.8% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 12 months: 92.2% (Kaplan-Meier).
- Estimated probability of retaining a customer beyond 24 months: 82.8% (Kaplan-Meier).
- Churn hazard is highest in tenure interval [18, 24) months: about 0.99% of active customers churn per month in this period (vs 0.72% on average).
- Cox model: payment_method = Bank Transfer has a hazard ratio of 1.83 (95% CI 1.61–2.07, p <0.001), i.e. +83% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: payment_method = Cash has a hazard ratio of 1.80 (95% CI 1.52–2.13, p <0.001), i.e. +80% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: auto_renew has a hazard ratio of 0.61 (95% CI 0.56–0.68, p <0.001), i.e. -39% churn hazard (binary (0→1)), holding other factors constant.
- Cox model: payment_method = Credit Card has a hazard ratio of 1.59 (95% CI 1.39–1.82, p <0.001), i.e. +59% churn hazard (vs 'Auto-debit'), holding other factors constant.
- Cox model: premium_change_pct has a hazard ratio of 1.39 (95% CI 1.32–1.45, p <0.001), i.e. +39% churn hazard (per 1 SD (= 6.99)), holding other factors constant.
- Restricted mean survival time (RMST, horizon 24 months): customers with n_claims_rejected = '2' stay on average 2.9 months less than '0' within the first 24 months (19.4 vs 22.4).
- Proportional-hazards diagnostics (Schoenfeld residual test): 0 of 14 terms show time-varying effects (p < 0.01); the PH assumption is supported.
- Accelerated failure time model: payment_method = Bank Transfer (vs 'Auto-debit') multiplies expected time-to-churn by 0.60 (95% CI 0.54–0.67), i.e. customers leave 40% sooner.
- Accelerated failure time model: payment_method = Cash (vs 'Auto-debit') multiplies expected time-to-churn by 0.62 (95% CI 0.53–0.72), i.e. customers leave 38% sooner.
- Accelerated failure time model: auto_renew (binary (0→1)) multiplies expected time-to-churn by 1.55 (95% CI 1.42–1.69), i.e. customers leave 55% later.

## Interpretable model

- Holding other factors constant, payment_method = Bank Transfer (vs 'Auto-debit') changes the odds of churn by +133% (OR = 2.33, 95% CI 2.00–2.71, p <0.001; average marginal effect +12.1 pp).
- Holding other factors constant, payment_method = Cash (vs 'Auto-debit') changes the odds of churn by +129% (OR = 2.29, 95% CI 1.86–2.82, p <0.001; average marginal effect +11.8 pp).
- Holding other factors constant, payment_method = Credit Card (vs 'Auto-debit') changes the odds of churn by +107% (OR = 2.07, 95% CI 1.76–2.42, p <0.001; average marginal effect +10.4 pp).
- Holding other factors constant, auto_renew (binary (0→1)) changes the odds of churn by -49% (OR = 0.51, 95% CI 0.46–0.58, p <0.001; average marginal effect -9.5 pp).
- Holding other factors constant, premium_change_pct (per 1 SD (= 6.99)) changes the odds of churn by +64% (OR = 1.64, 95% CI 1.54–1.74, p <0.001; average marginal effect +7.0 pp).
- Holding other factors constant, tenure_months (per 1 SD (= 23.6)) changes the odds of churn by -37% (OR = 0.63, 95% CI 0.58–0.68, p <0.001; average marginal effect -6.6 pp).

## Model

- Ablation study: removing 'premium_change' lowers ROC-AUC by 0.033 (95% CI 0.024 to 0.042, DeLong p <0.001), the largest contribution of any feature group.
- Engineered insurance features add -0.0036 ROC-AUC over the raw variables (DeLong p 0.179).
- The final model (hill_climb) achieves a cross-validated roc_auc of 0.7599 (ROC-AUC 0.7599) versus 0.50 for a random baseline.
- We ran 32 logged experiments across 6 stages (model zoo, tuning, multi-seed, feature selection, ablation, ensembling); ROC-AUC improved from 0.7565 (logistic regression baseline) to 0.7599 (final hill_climb).
- At the selected threshold (0.25) the model identifies 61.5% of churners (recall) with a precision of 41.2%, i.e. 2.0x better targeting than random selection.
- Final model ROC-AUC = 0.760 (95% bootstrap CI 0.748–0.772).
- The final model is significantly better than the interpretable logistic regression (Δroc_auc = +0.0034, 95% CI +0.0011 to +0.0058).
- Across 15 candidate models, the final model's ROC-AUC is 0.760 (95% DeLong CI 0.747–0.773); it is significantly better than 15 of them after Holm correction.
- Profit-based evaluation (EMPC; Verbraken et al., 2013) agrees with the AUC ranking: the most profitable model is FINAL: hill_climb with an expected maximum profit of 114.99K IDR per customer when targeting about 55.7% of the base.
- The interpretable logistic regression reaches ROC-AUC 0.757; the gap to the final model is +0.0034 (DeLong p 0.008).
- A glass-box Explainable Boosting Machine attains ROC-AUC 0.748 (Δ vs final +0.0119, DeLong p <0.001), offering a fully transparent alternative for regulated use.
- The out-of-fold risk score also orders customers by time to churn (Harrell's C-index 0.794); survival curves of the three risk tiers separate clearly (log-rank p <0.001).

## Explainability

- Partial dependence: moving premium_change_pct from -7.50 to 15.72 changes average predicted churn from 11.4% to 31.9%.
- Partial dependence: moving tenure_months from 3.00 to 76.00 changes average predicted churn from 22.9% to 15.9%.
- Partial dependence: moving digital_engagement_score from 19.00 to 88.00 changes average predicted churn from 23.8% to 18.1%.
- Partial dependence: moving n_products from 1.00 to 3.00 changes average predicted churn from 22.2% to 15.6%.
- Partial dependence: moving avg_claim_settlement_days from 3.00 to 34.00 changes average predicted churn from 17.7% to 24.5%.
- Partial dependence: moving fe_tenure_years from 0.25 to 6.33 changes average predicted churn from 21.7% to 17.6%.
- For policy_type = 'Auto', the top churn drivers are premium_change_pct (11%), payment_method (11%), auto_renew (10%).
- For policy_type = 'Health', the top churn drivers are premium_change_pct (11%), auto_renew (10%), payment_method (10%).
- For policy_type = 'Life', the top churn drivers are premium_change_pct (11%), payment_method (11%), auto_renew (10%).
- For policy_type = 'Property', the top churn drivers are premium_change_pct (12%), payment_method (11%), auto_renew (10%).

## Business

- Targeting the top 20% highest-risk customers captures 45.8% of all churners (2.3x lift over random targeting); the top decile churns at 55.9% vs 3.4% in the bottom decile. KS = 0.39.
- The High-risk tier (20% of customers, p ≥ 0.32) has an actual churn rate of 48.2% and contains 45.8% of all churners.
- Expected annual premium at risk from churn is 9.97B IDR (20.8% of the annual premium base); the High-risk tier alone accounts for 43.1% of it.
- 'Priority Save' customers (high risk & above-median value) are 9.8% of the base but hold 29.3% of the value at risk — the first target for personalised retention.
- Simulated retention campaign (assumed success rate 30%, cost 150.00K IDR per contact): targeting the top 50% ranked by 'Model: expected loss (p × value)' maximises net profit at 810.79M (ROI 1.4x), versus 238.95M for random targeting of the same size.
- What-if: 'Move all 'payment_method' customers to 'Auto-debit'' affects 67% of customers and lowers their predicted churn from 23.7% to 14.5%; at 30% adoption this avoids ≈19 churners per 1,000 customers (model-based, associational).
- What-if: 'Set auto_renew = 1 for everyone' affects 45% of customers and lowers their predicted churn from 24.6% to 16.7%; at 30% adoption this avoids ≈11 churners per 1,000 customers (model-based, associational).
- What-if: 'Cap premium_change_pct at median (4.1)' affects 48% of customers and lowers their predicted churn from 25.5% to 19.3%; at 30% adoption this avoids ≈9 churners per 1,000 customers (model-based, associational).

## Causal

- Adjusting for observed confounders (doubly robust AIPW), premium_change_pct ≤ median (4.1) is associated with a -11.7 pp change in churn probability (95% CI -13.6 to -9.9; naive difference -11.1 pp).
- Adjusting for observed confounders (doubly robust AIPW), auto_renew = 1 is associated with a -10.0 pp change in churn probability (95% CI -11.8 to -8.1; naive difference -9.7 pp).
- Adjusting for observed confounders (doubly robust AIPW), payment_method = Auto-debit is associated with a -9.9 pp change in churn probability (95% CI -11.9 to -8.0; naive difference -10.4 pp).
- Adjusting for observed confounders (doubly robust AIPW), n_complaints_12m = 0 is associated with a -8.9 pp change in churn probability (95% CI -11.5 to -6.2; naive difference -11.2 pp).
- Adjusting for observed confounders (doubly robust AIPW), avg_claim_settlement_days ≤ median (13) is associated with a -6.9 pp change in churn probability (95% CI -10.3 to -3.5; naive difference -6.8 pp).
- The effect of 'premium_change_pct ≤ median (4.1)' (-11.7 pp) is robust: a placebo treatment yields -0.60 pp (p 0.538) and an unmeasured confounder would need a risk-ratio association of at least 2.51 with both treatment and churn to explain it away (E-value).
- The effect of 'payment_method = Auto-debit' (-9.9 pp) is robust: a placebo treatment yields +0.70 pp (p 0.507) and an unmeasured confounder would need a risk-ratio association of at least 2.34 with both treatment and churn to explain it away (E-value).
- The effect of 'auto_renew = 1' (-10.0 pp) is robust: a placebo treatment yields +1.18 pp (p 0.221) and an unmeasured confounder would need a risk-ratio association of at least 2.23 with both treatment and churn to explain it away (E-value).
- The effect of 'n_complaints_12m = 0' (-8.9 pp) is robust: a placebo treatment yields -2.13 pp (p 0.077) and an unmeasured confounder would need a risk-ratio association of at least 1.90 with both treatment and churn to explain it away (E-value).
- The effect of 'avg_claim_settlement_days ≤ median (13)' (-6.9 pp) is robust: a placebo treatment yields -1.70 pp (p 0.341) and an unmeasured confounder would need a risk-ratio association of at least 1.51 with both treatment and churn to explain it away (E-value).
- Effects of 'premium_change_pct ≤ median (4.1)' are broadly homogeneous: the most responsive quintile shows a 12.0 pp churn reduction vs 11.7 pp in the least responsive (difference p 0.940). Treating the top 20% by predicted uplift avoids 30.6 churners per 1,000 eligible customers vs 66.5 when targeting by churn risk (-35.8).
- Effects of 'auto_renew = 1' are broadly homogeneous: the most responsive quintile shows a 10.3 pp churn reduction vs 9.0 pp in the least responsive (difference p 0.681). Treating the top 20% by predicted uplift avoids 14.1 churners per 1,000 eligible customers vs 47.1 when targeting by churn risk (-33.0).

## Personas

- Persona P2 (53% of at-risk customers, actual churn 32.5%): risk driven mainly by auto_renew (+0.09); payment_method (+0.08).
- Persona P1 (47% of at-risk customers, actual churn 36.8%): risk driven mainly by premium_change_pct (+0.42).

## Governance

- Fairness audit across dependents, age band, gender, marital status, region: predicted risk tracks actual churn within each group (largest calibration ratio deviation: dependents = '3', 1.09); the largest within-attribute AUC gap is 0.127. Differences in High-tier selection reflect genuine differences in churn rates; the score is intended for retention outreach only, not for pricing or underwriting.

## Recommendations

- 1. Smarter renewal pricing — Cap or phase in premium increases for at-risk loyal customers, explain the value behind increases, and offer coverage/deductible adjustments instead of lapse. Evidence: premium_change_pct = 13.2–30.6: churn 33.5% (1.6× avg); IV 0.16; OR 1.64; HR 1.39; SHAP rank #1; causal (AIPW) -11.7 pp [-13.6, -9.9]. Impact: -2.98 pp churn at full adoption (≈9 churners avoided /1,000 at 30% adoption). KPI: Churn rate among customers with increases; price elasticity.
- 2. Shift manual payers to automatic payment — Offer a small incentive (e.g. premium discount/cashback) and one-click enrolment for auto-debit/recurring card payment; send pre-due reminders to remaining manual payers. Evidence: payment_method = Bank Transfer: churn 25.5% (1.2× avg); IV 0.10; OR 2.33; HR 1.83; SHAP rank #2; causal (AIPW) -9.9 pp [-11.9, -8.0]. Impact: -6.19 pp churn at full adoption (≈19 churners avoided /1,000 at 30% adoption). KPI: % of policies on auto-pay; lapse rate of converted vs control.
- 3. Make renewal effortless (default auto-renewal) — Default new and renewing policies to auto-renewal with clear opt-out; 30/14/7-day renewal reminders with a one-click renew link. Evidence: auto_renew = No: churn 26.4% (1.3× avg); IV 0.08; OR 0.51; HR 0.61; SHAP rank #3; causal (AIPW) -10.0 pp [-11.8, -8.1]. Impact: -3.56 pp churn at full adoption (≈11 churners avoided /1,000 at 30% adoption). KPI: Auto-renew adoption; renewal rate.
- 4. Complaint recovery programme — Trigger a proactive call within 48h of any complaint, enforce resolution SLAs, offer service-recovery gestures to high-value complainants, and fix top root causes. Evidence: n_complaints_12m = ≥2: churn 44.3% (2.1× avg); IV 0.11; OR 1.33; HR 1.23; SHAP rank #8; causal (AIPW) -8.9 pp [-11.5, -6.2]. Impact: -1.11 pp churn at full adoption (≈3 churners avoided /1,000 at 30% adoption). KPI: Complaint resolution time; churn rate of complainants.
- 5. Improve the claims experience — Fast-track settlement, explain rejections transparently with an appeal path, and assign a claims concierge for high-value / high-risk customers after a claim event. Evidence: avg_claim_settlement_days = 21–28: churn 34.6% (1.6× avg); IV 0.10; OR 1.19; HR 1.11; SHAP rank #9; causal (AIPW) -6.9 pp [-10.3, -3.5]. Impact: -0.76 pp churn at full adoption (≈2 churners avoided /1,000 at 30% adoption). KPI: Claim settlement days; post-claim churn rate; claim NPS.
- 6. Bundling & cross-sell to raise switching costs — Offer multi-policy discounts and relevant riders to single-product customers with good risk profiles. Evidence: n_products = 1: churn 23.8% (1.1× avg); IV 0.05; OR 0.76; SHAP rank #7. KPI: Products per customer; churn of bundled vs single.
- 7. Longer payment / contract terms — Encourage annual/quarterly payment or longer contracts with a discount; monthly payers get extra reminders. Evidence: payment_frequency = Monthly: churn 23.6% (1.1× avg); IV 0.02; SHAP rank #6. KPI: Share of annual payers; churn by payment frequency.
- 8. Deploy a churn early-warning system — Score all active policies monthly with this model; route High-risk/Priority-Save customers to retention teams, lower tiers to automated digital nudges; refresh the model quarterly. Evidence: Model ROC-AUC 0.760; top-20% captures 46% of churners. Impact: optimal campaign: target top 50% → net 810.79M. KPI: Precision/recall of alerts; retained revenue vs control group.
- 9. Validate with controlled pilots (A/B tests) — For each intervention keep a random control group (e.g. 20% of targeted customers) to measure true uplift before scaling. Evidence: What-if results are associational. KPI: Uplift in retention rate (treated − control).
- Pilot design: to detect a 11.7 pp reduction from a baseline of 48.2% in the High-risk tier ('Shift to: premium_change_pct ≤ median (4.1)'), a randomised test needs 277 customers per arm (α = 0.05, power 80%), i.e. 137% of the High-tier portfolio.

