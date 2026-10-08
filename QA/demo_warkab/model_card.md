# Model Card — Churn Early-Warning Model

| Item | Description |
|---|---|
| Model | hill_climb (xgb_fs 0.44, logreg 0.33, catboost_multiseed 0.11, catboost 0.11) |
| Intended use | Rank active policyholders by 12-month churn risk to prioritise retention outreach and allocate retention budget. |
| Out-of-scope use | Not for premium pricing, underwriting, claims decisions or denial of service; not validated for other products/markets. |
| Training data | 8,000 customers, 53 input features; target 'churn' (churn = Yes); churn rate 21.1%. |
| Excluded variables | cancellation_reason (post-event leakage) |
| Validation | Stratified 5-fold CV (out-of-fold), target encoding inside folds, shuffled-label & adversarial checks, bootstrap & DeLong CIs. |
| Performance | ROC-AUC 0.760 (95% CI 0.748–0.772); PR-AUC 0.475; Brier 0.140; ECE 0.012; EMPC 115.01K IDR/customer. |
| Calibration | none (selected by cross-validated log-loss). |
| Decision rule | Risk tiers at the 50%/80% quantiles; campaign size chosen by expected profit (see Section 4). |
| Explainability | Global: SHAP, permutation importance, PDP, EBM shape functions (if used). Local: SHAP waterfall per customer for agents. |
| Fairness | Audited on gender, fe_age_band, region, dependents, marital_status; max AUC gap 0.126. |
| Monitoring | Monthly: PSI per feature (alert > 0.25), score distribution, realised churn by tier, calibration; retrain quarterly or if AUC drops > 0.03. |
| Limitations | Observational snapshot data; causal effects assume no unmeasured confounding; ROI depends on stated cost/acceptance assumptions. |
