# Stress test — 22/22 variants passed

Setiap varian = satu bentuk data asuransi berbeda, dijalankan end-to-end oleh `tools/run_case.py` (notebook utuh: cleaning → analisis → model → kausal → laporan DOCX → dashboard → submission). PASS = selesai tanpa satu pun section error.

| variant | description | status | auc | n_train | target | section_errors | report | dashboard | submission |
|---|---|---|---|---|---|---|---|---|---|
| all_categorical | only categorical predictors | PASS | 0.6022 | 2792 | churn | none | True | True | True |
| baseline_claims | messy synthetic + one-to-many claims table | PASS | 0.7523 | 3000 | churn | none | True | True | True |
| date_only_tenure | tenure only as a start date + snapshot date | PASS | 0.7409 | 3000 | churn | none | True | True | True |
| excel_files | train/test as .xlsx | PASS | 0.7423 | 3000 | churn | none | True | True | True |
| extreme_imbalance | ≈2% churn rate | PASS | 0.6689 | 4875 | churn | none | True | True | True |
| float_ids_numeric_target | Kaggle-style float IDs, target 0/1 integer, int IDs in sample submission | PASS | 0.7497 | 3000 | Churn | none | True | True | True |
| full_mode_small | FULL mode (all 9 algorithms, Optuna, multi-seed) on 1,500 rows + PDF/autofit | PASS | 0.7251 | 1500 | churn | none | True | True | True |
| heavy_missing | 40–70% missing in many columns + missing target rows | PASS | 0.7326 | 2960 | churn | none | True | True | True |
| indonesian_columns | Indonesian column names, target 'berhenti' = Ya/Tidak | PASS | 0.7558 | 3000 | berhenti | none | True | True | True |
| inverted_is_active | target is_active (1 = still customer) | PASS | 0.7314 | 3000 | is_active | none | True | True | True |
| label_metric_f1 | metric F1, label submission with Yes/No | PASS | 0.7459 | 3000 | churn | none | True | True | True |
| labels_separate_file | features in train.csv, labels in train_labels.csv | PASS | 0.7268 | 3000 | churn | none | True | True | True |
| multiclass_status | target = policy status Active / Lapsed / Surrendered | PASS | 0.7194 | 3000 | policy_status | none | True | True | True |
| no_tenure_no_premium | no tenure, no premium, no dates (survival & value skipped) | PASS | 0.719 | 3000 | churn | none | True | True | True |
| no_test | only a training file (analysis + CV, no submission) | PASS | 0.7196 | 3000 | churn | none | True | True | False |
| panel_monthly | 3 monthly snapshots per customer (repeated customer_id, unique row_id) | PASS | 0.676 | 4500 | churn | none | True | True | True |
| semicolon_latin1 | semicolon CSV, latin-1 encoding, decimal comma | PASS | 0.745 | 3000 | churn | none | True | True | True |
| single_file_missing_target | one file only; rows with empty target are the ones to predict | PASS | 0.7411 | 3000 | churn | none | True | True | True |
| start_end_dates | no tenure column; policy start date + cancellation date for churners → survival time reconstructed | PASS | 0.7605 | 3000 | churn | none | True | True | True |
| text_and_one_to_one | free-text complaint column + one-to-one demographics table | PASS | 0.737 | 3000 | churn | none | True | True | True |
| tiny | 300 rows | PASS | 0.7346 | 300 | churn | none | True | True | True |
| wide_noise | 120 extra noise columns (numeric + categorical) | PASS | 0.7122 | 3000 | churn | none | True | True | True |