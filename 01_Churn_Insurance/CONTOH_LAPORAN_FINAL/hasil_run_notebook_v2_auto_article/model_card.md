# Model Card — Churn Early-Warning Model

| Item | Description |
|---|---|
| Model | hill_climb (lgbm 0.50, lgbm_tuned 0.50) |
| Intended use | Rank active policyholders by 12-month churn risk to prioritise retention outreach and allocate retention budget. |
| Out-of-scope use | Not for premium pricing, underwriting, claims decisions or denial of service; not validated for other products/markets. |
| Training data | 160,000 customers, 24 input features; target 'Churn' (churn = 1); churn rate 11.7%. |
| Excluded variables | acct_suspd_date_year, acct_suspd_date_month, acct_suspd_date_days_since, acct_suspd_date (post-event leakage) |
| Validation | Stratified 5-fold CV (out-of-fold), target encoding inside folds, shuffled-label & adversarial checks, bootstrap & DeLong CIs. |
| Performance | ROC-AUC 0.702 (95% CI 0.698–0.707); PR-AUC 0.329; Brier 0.087; ECE 0.002; EMPC 4.31 USD/customer. |
| Calibration | isotonic (selected by cross-validated log-loss). |
| Decision rule | Risk tiers at the 50%/80% quantiles; campaign size chosen by expected profit (see Section 4). |
| Explainability | Global: SHAP, permutation importance, PDP, EBM shape functions (if used). Local: SHAP waterfall per customer for agents. |
| Fairness | Audited on fe_age_band, has_children, marital_status; max AUC gap 0.162. |
| Monitoring | Monthly: PSI per feature (alert > 0.25), score distribution, realised churn by tier, calibration; retrain quarterly or if AUC drops > 0.03. |
| Limitations | Observational snapshot data; causal effects assume no unmeasured confounding; ROI depends on stated cost/acceptance assumptions. |
