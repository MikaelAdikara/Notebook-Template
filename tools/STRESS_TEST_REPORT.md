# Stress test — 44/44 variants passed

Setiap varian = satu bentuk data asuransi berbeda, dijalankan end-to-end oleh `tools/run_case.py` (notebook utuh: cleaning → analisis → model → kausal → laporan DOCX → dashboard → submission). PASS = selesai tanpa satu pun section error.

| variant | description | status | auc | n_train | target | section_errors | report | dashboard | submission |
|---|---|---|---|---|---|---|---|---|---|
| all_categorical | only categorical predictors | PASS | 0.6022 | 2792.0 | churn | none | True | True | True |
| baseline_claims | messy synthetic + one-to-many claims table | PASS | 0.7523 | 3000.0 | churn | none | True | True | True |
| date_only_tenure | tenure only as a start date + snapshot date | PASS | 0.7409 | 3000.0 | churn | none | True | True | True |
| excel_files | train/test as .xlsx | PASS | 0.7423 | 3000.0 | churn | none | True | True | True |
| extreme_imbalance | ≈2% churn rate | PASS | 0.6689 | 4875.0 | churn | none | True | True | True |
| float_ids_numeric_target | Kaggle-style float IDs, target 0/1 integer, int IDs in sample submission | PASS | 0.7497 | 3000.0 | Churn | none | True | True | True |
| full_mode_small | FULL mode (all 9 algorithms, Optuna, multi-seed) on 1,500 rows + PDF/autofit | PASS | 0.722 | 1500.0 | churn | none | True | True | True |
| heavy_missing | 40–70% missing in many columns + missing target rows | PASS | 0.7326 | 2960.0 | churn | none | True | True | True |
| indonesian_columns | Indonesian column names, target 'berhenti' = Ya/Tidak | PASS | 0.7558 | 3000.0 | berhenti | none | True | True | True |
| inverted_is_active | target is_active (1 = still customer) | PASS | 0.7314 | 3000.0 | is_active | none | True | True | True |
| label_metric_f1 | metric F1, label submission with Yes/No | PASS | 0.7459 | 3000.0 | churn | none | True | True | True |
| labels_separate_file | features in train.csv, labels in train_labels.csv | PASS | 0.7268 | 3000.0 | churn | none | True | True | True |
| multiclass_status | target = policy status Active / Lapsed / Surrendered | PASS | 0.7194 | 3000.0 | policy_status | none | True | True | True |
| no_tenure_no_premium | no tenure, no premium, no dates (survival & value skipped) | PASS | 0.719 | 3000.0 | churn | none | True | True | True |
| no_test | only a training file (analysis + CV, no submission) | PASS | 0.7196 | 3000.0 | churn | none | True | True | False |
| panel_monthly | 3 monthly snapshots per customer (repeated customer_id, unique row_id) | PASS | 0.676 | 4500.0 | churn | none | True | True | True |
| semicolon_latin1 | semicolon CSV, latin-1 encoding, decimal comma | PASS | 0.745 | 3000.0 | churn | none | True | True | True |
| single_file_missing_target | one file only; rows with empty target are the ones to predict | PASS | 0.7411 | 3000.0 | churn | none | True | True | True |
| start_end_dates | no tenure column; policy start date + cancellation date for churners → survival time reconstructed | PASS | 0.7605 | 3000.0 | churn | none | True | True | True |
| text_and_one_to_one | free-text complaint column + one-to-one demographics table | PASS | 0.737 | 3000.0 | churn | none | True | True | True |
| tiny | 300 rows | PASS | 0.7346 | 300.0 | churn | none | True | True | True |
| wide_noise | 120 extra noise columns (numeric + categorical) | PASS | 0.7122 | 3000.0 | churn | none | True | True | True |
| x_bom_spaces_headers | [rusak] BOM UTF-8, spasi & huruf besar di nama kolom (' Churn ', 'Customer ID ') | PASS | 0.7582 | 3000.0 | Churn | none | True | True | True |
| x_bool_and_special_names | [rusak] kolom boolean True/False, 'TRUE'/'FALSE', nama kolom karakter khusus ('Premi (Rp)', 'Umur/Tahun', 'Klaim%') | PASS | 0.7352 | 3000.0 | churn | none | True | True | True |
| x_constant_target | [rusak, EXPECTED STOP] target hanya 1 kelas → harus berhenti dengan pesan jelas | PASS (stopped with clear message) | nan | nan | nan | expected stop | nan | nan | nan |
| x_currency_scaled_strings | [rusak] angka gaya Indonesia: 'Rp 5 jt', '1,2 M', '750 rb', '45%', '3,5' | PASS | 0.7341 | 3000.0 | churn | none | True | True | True |
| x_duplicate_columns | [rusak] nama kolom ganda (dua kolom 'age', dua 'region') | PASS | 0.7651 | 3000.0 | churn | none | True | True | True |
| x_duplicates_conflicting | [rusak] 10% baris duplikat di train, sebagian dengan label berlawanan; ID duplikat di test | PASS | 0.7451 | 3000.0 | churn | none | True | True | True |
| x_empty_rows_cols_constant | [rusak] baris kosong, kolom kosong total, kolom konstan, kolom 'Unnamed: 0' (index ikut tersimpan) | PASS | 0.7376 | 3000.0 | churn | none | True | True | True |
| x_excel_title_rows_multisheet | [rusak] Excel: 2 sheet (README + data), judul & baris kosong di atas header | PASS | 0.7451 | 3000.0 | churn | none | True | True | True |
| x_high_cardinality_ids | [rusak] banyak kolom berbau ID (agent_id 2000 level, branch_code numerik, kode pos) | PASS | 0.7294 | 3000.0 | churn | none | True | True | True |
| x_inf_outliers_negative | [rusak] ±inf, outlier 1e15, umur negatif/999, tenure negatif, premi 0 | PASS | 0.7423 | 3000.0 | churn | none | True | True | True |
| x_jsonl_parquet | [rusak] train .jsonl, test .parquet | PASS | 0.7464 | 3000.0 | churn | none | True | True | True |
| x_leakage_traps | [rusak] jebakan leakage: tanggal batal, alasan batal, refund, status_after, kolom = target ter-encode | PASS | 0.7616 | 3000.0 | churn | none | True | True | True |
| x_messy_target_labels | [rusak] label target tidak konsisten: 'Yes','yes ','Y','1','TRUE','No','n','0','false' | PASS | 0.7513 | 3000.0 | churn | none | True | True | True |
| x_mixed_date_formats | [rusak] tanggal format campur: '2023-01-05', '05/01/2023', 'Jan 5, 2023', '20230105'; tanpa kolom tenure | PASS | 0.7213 | 3000.0 | churn | none | True | True | True |
| x_mixed_type_numbers | [rusak] kolom angka campur teks: 'abc', '', ' 7 ', '1.5e3', 'N/A', '-' | PASS | 0.748 | 3000.0 | churn | none | True | True | True |
| x_pii_free_text | [rusak] kolom PII & teks bebas: nama, email, no HP, alamat, catatan agen | PASS | 0.7 | 3000.0 | churn | none | True | True | True |
| x_status_active_inactive | [rusak] target 'Status' = Active/Inactive/ACTIVE/inactive ditaruh di tengah tabel | PASS | 0.7377 | 3000.0 | Status | none | True | True | True |
| x_tab_txt_file | [rusak] file .txt tab-separated dengan ekstensi tidak standar + baris rusak (kolom berlebih) | PASS | 0.7343 | 3000.0 | churn | none | True | True | True |
| x_target_bool_float | [rusak] target bertipe float '1.0'/'0.0' bernama 'Exited', ID dengan leading zeros di sample | PASS | 0.7529 | 3000.0 | Exited | none | True | True | True |
| x_test_columns_mismatch | [rusak] test: urutan kolom beda, 1 kolom hilang, 1 kolom ekstra, kolom target ikut ada (kosong) | PASS | 0.7468 | 3000.0 | churn | none | True | True | True |
| x_tiny_wide_mess | [rusak] 120 baris saja + 60 kolom noise + 30% missing | PASS | 0.7242 | 120.0 | churn | none | True | True | True |
| x_unseen_categories | [rusak] kategori baru di test yang tidak ada di train + typo/kapitalisasi acak | PASS | 0.7449 | 3000.0 | churn | none | True | True | True |