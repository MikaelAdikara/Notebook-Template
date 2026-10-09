# QA / QC FINAL — Template Churn Asuransi (Tim Warkab)

Tanggal: 9 Oktober 2026. Mesin uji: Windows 11, Python 3.11, MS Word (hitung halaman & PDF), Microsoft Edge (screenshot), ffmpeg (video).
Anggota tim: Mikael Alexander Adikara Purnama & Pandu Winata.

## Ringkasan

| # | Pengujian | Hasil | Bukti |
|---|---|---|---|
| 1 | **Stress test 44 bentuk data**: 22 skenario case + 22 data rusak/dimanipulasi, semuanya pada notebook final | ****44/44 PASS**** (target 1 kelas berhenti dengan pesan jelas = perilaku yang benar) | `tools/STRESS_TEST_REPORT.md`, bagian 2 |
| 2 | Bukti per jenis kerusakan: data rusak ditafsirkan **benar**, bukan sekadar tidak error | 22/22 sesuai harapan | bagian 3 (baris log asli notebook) |
| 3 | **Demo end-to-end tim Warkab** (casebook fiktif → intake → riset → `RUN_FULL.bat` → artikel → dashboard → ZIP) | 0 section error, OOF AUC 0,760, **AUC test tersembunyi 0,782**, 49,4 menit | `demo_warkab/`, video |
| 4 | QA otomatis artikel demo (`QA/qa_check.py`) | **43 PASS · 0 FAIL · 2 WARN** | `demo_warkab/QA_CHECK.md` |
| 5 | Regresi (tidak ada downgrade): notebook final vs sebelum upgrade, data & seed sama | AUC fast run identik 0,7575; 154 cell (90 code) tetap; semua fitur lama tetap | bagian 5 |
| 6 | Run cepat pada notebook + runner final | 0 section error, AUC 0,7575, test AUC 0,780, console bersih | bagian 5 |
| 7 | Rekaman proses | Video MP4 (37 langkah, ±2,8 menit) + screenshot per langkah + `STEPS.md` | `walkthrough_warkab/` |

## 1. Apa yang dibuktikan

1. **Data apa pun masuk**:
   - format csv/tsv/txt, Excel banyak sheet dengan judul di atas header, json/jsonl, parquet;
   - encoding dan separator apa pun;
   - kolom dan label berantakan;
   - angka gaya Indonesia ("Rp 5 jt", "1,2 M");
   - tanggal format campur;
   - inf/outlier, duplikat, kolom bocor, PII;
   - data sangat kecil atau sangat lebar.

   Semuanya berjalan sampai artikel, dashboard, dan submission tanpa section error.
2. **Data yang memang tidak bisa dianalisis berhenti dengan pesan jelas**, misalnya target hanya 1 kelas, < 30 baris, atau target kontinu. Pesannya menyebut key yang harus diubah, bukan error misterius.
3. **Paper menempel ke case**: nama perusahaan, konteks, pertanyaan soal, skala portofolio, budget, fakta casebook, riset tim, dan paragraf custom benar-benar muncul di artikel. Ini diverifikasi otomatis oleh `qa_check.py`, bukan diklaim saja.
4. **Format lomba terpenuhi**: isi utama ≤ 10 halaman (cover & appendix tidak dihitung, referensi dihitung), A4, TNR 12, 1.15, nama file `<Tim>_Final Stage 1`.

## 2. Stress test (notebook final)

Ringkasan ada di `tools/STRESS_TEST_REPORT.md`. Setiap varian = satu folder kerja baru. Notebook dijalankan utuh oleh `tools/run_case.py`: cleaning → EDA → driver → survival → model → kausal → artikel DOCX → dashboard → submission.

Daftar varian `x_*` (data rusak) beserta penanganannya: `01_Churn_Insurance/CASE_SCENARIOS.md` bagian X.

| variant | description | status | auc | n_train | section_errors |
|---|---|---|---|---|---|
| all_categorical | only categorical predictors | PASS | 0.6022 | 2792.0 | none |
| baseline_claims | messy synthetic + one-to-many claims table | PASS | 0.7523 | 3000.0 | none |
| date_only_tenure | tenure only as a start date + snapshot date | PASS | 0.7409 | 3000.0 | none |
| excel_files | train/test as .xlsx | PASS | 0.7423 | 3000.0 | none |
| extreme_imbalance | ≈2% churn rate | PASS | 0.6689 | 4875.0 | none |
| float_ids_numeric_target | Kaggle-style float IDs, target 0/1 integer, int IDs in sample submission | PASS | 0.7497 | 3000.0 | none |
| full_mode_small | FULL mode (all 9 algorithms, Optuna, multi-seed) on 1,500 rows + PDF/autofit | PASS | 0.7158 | 1500.0 | none |
| heavy_missing | 40–70% missing in many columns + missing target rows | PASS | 0.7326 | 2960.0 | none |
| indonesian_columns | Indonesian column names, target 'berhenti' = Ya/Tidak | PASS | 0.7558 | 3000.0 | none |
| inverted_is_active | target is_active (1 = still customer) | PASS | 0.7314 | 3000.0 | none |
| label_metric_f1 | metric F1, label submission with Yes/No | PASS | 0.7459 | 3000.0 | none |
| labels_separate_file | features in train.csv, labels in train_labels.csv | PASS | 0.7268 | 3000.0 | none |
| multiclass_status | target = policy status Active / Lapsed / Surrendered | PASS | 0.7194 | 3000.0 | none |
| no_tenure_no_premium | no tenure, no premium, no dates (survival & value skipped) | PASS | 0.719 | 3000.0 | none |
| no_test | only a training file (analysis + CV, no submission) | PASS | 0.7196 | 3000.0 | none |
| panel_monthly | 3 monthly snapshots per customer (repeated customer_id, unique row_id) | PASS | 0.676 | 4500.0 | none |
| semicolon_latin1 | semicolon CSV, latin-1 encoding, decimal comma | PASS | 0.745 | 3000.0 | none |
| single_file_missing_target | one file only; rows with empty target are the ones to predict | PASS | 0.7411 | 3000.0 | none |
| start_end_dates | no tenure column; policy start date + cancellation date for churners → survival time reconstructed | PASS | 0.7605 | 3000.0 | none |
| text_and_one_to_one | free-text complaint column + one-to-one demographics table | PASS | 0.737 | 3000.0 | none |
| tiny | 300 rows | PASS | 0.7346 | 300.0 | none |
| wide_noise | 120 extra noise columns (numeric + categorical) | PASS | 0.7122 | 3000.0 | none |
| x_bom_spaces_headers | [rusak] BOM UTF-8, spasi & huruf besar di nama kolom (' Churn ', 'Customer ID ') | PASS | 0.7582 | 3000.0 | none |
| x_bool_and_special_names | [rusak] kolom boolean True/False, 'TRUE'/'FALSE', nama kolom karakter khusus ('Premi (Rp)', 'Umur/Tahun', 'Klaim%') | PASS | 0.7352 | 3000.0 | none |
| x_constant_target | [rusak, EXPECTED STOP] target hanya 1 kelas → harus berhenti dengan pesan jelas | PASS (stopped with clear message) | nan | nan | expected stop |
| x_currency_scaled_strings | [rusak] angka gaya Indonesia: 'Rp 5 jt', '1,2 M', '750 rb', '45%', '3,5' | PASS | 0.7341 | 3000.0 | none |
| x_duplicate_columns | [rusak] nama kolom ganda (dua kolom 'age', dua 'region') | PASS | 0.7651 | 3000.0 | none |
| x_duplicates_conflicting | [rusak] 10% baris duplikat di train, sebagian dengan label berlawanan; ID duplikat di test | PASS | 0.7451 | 3000.0 | none |
| x_empty_rows_cols_constant | [rusak] baris kosong, kolom kosong total, kolom konstan, kolom 'Unnamed: 0' (index ikut tersimpan) | PASS | 0.7376 | 3000.0 | none |
| x_excel_title_rows_multisheet | [rusak] Excel: 2 sheet (README + data), judul & baris kosong di atas header | PASS | 0.7451 | 3000.0 | none |
| x_high_cardinality_ids | [rusak] banyak kolom berbau ID (agent_id 2000 level, branch_code numerik, kode pos) | PASS | 0.7294 | 3000.0 | none |
| x_inf_outliers_negative | [rusak] ±inf, outlier 1e15, umur negatif/999, tenure negatif, premi 0 | PASS | 0.7423 | 3000.0 | none |
| x_jsonl_parquet | [rusak] train .jsonl, test .parquet | PASS | 0.7464 | 3000.0 | none |
| x_leakage_traps | [rusak] jebakan leakage: tanggal batal, alasan batal, refund, status_after, kolom = target ter-encode | PASS | 0.7616 | 3000.0 | none |
| x_messy_target_labels | [rusak] label target tidak konsisten: 'Yes','yes ','Y','1','TRUE','No','n','0','false' | PASS | 0.7513 | 3000.0 | none |
| x_mixed_date_formats | [rusak] tanggal format campur: '2023-01-05', '05/01/2023', 'Jan 5, 2023', '20230105'; tanpa kolom tenure | PASS | 0.7213 | 3000.0 | none |
| x_mixed_type_numbers | [rusak] kolom angka campur teks: 'abc', '', ' 7 ', '1.5e3', 'N/A', '-' | PASS | 0.748 | 3000.0 | none |
| x_pii_free_text | [rusak] kolom PII & teks bebas: nama, email, no HP, alamat, catatan agen | PASS | 0.7 | 3000.0 | none |
| x_status_active_inactive | [rusak] target 'Status' = Active/Inactive/ACTIVE/inactive ditaruh di tengah tabel | PASS | 0.7377 | 3000.0 | none |
| x_tab_txt_file | [rusak] file .txt tab-separated dengan ekstensi tidak standar + baris rusak (kolom berlebih) | PASS | 0.7343 | 3000.0 | none |
| x_target_bool_float | [rusak] target bertipe float '1.0'/'0.0' bernama 'Exited', ID dengan leading zeros di sample | PASS | 0.7529 | 3000.0 | none |
| x_test_columns_mismatch | [rusak] test: urutan kolom beda, 1 kolom hilang, 1 kolom ekstra, kolom target ikut ada (kosong) | PASS | 0.7468 | 3000.0 | none |
| x_tiny_wide_mess | [rusak] 120 baris saja + 60 kolom noise + 30% missing | PASS | 0.7242 | 120.0 | none |
| x_unseen_categories | [rusak] kategori baru di test yang tidak ada di train + typo/kapitalisasi acak | PASS | 0.7449 | 3000.0 | none |

## 3. Bukti per jenis kerusakan (baris log asli dari notebook ter-eksekusi)

| Varian | Bukti dari notebook ter-eksekusi |
|---|---|
| `x_bom_spaces_headers` | ℹ️ [train.csv] nama kolom dirapikan: ' Customer Id '→'Customer Id', ' Age '→'Age', ' Gender '→'Gender', ' Marital Status '→'Marital Status', ' Dependents '→'Dependents', ' Region '→'Region'<br>ℹ️ [test.csv] nama kolom dirapikan: ' Customer Id '→'Customer Id', ' Age '→'Age', ' Gender '→'Gender', ' Marital Status '→'Marital Status', ' Dependents '→'Dependents', ' Region '→'Region' |
| `x_duplicate_columns` |  |
| `x_test_columns_mismatch` | ⚠️ Kolom beda antara train & test → hanya train: {'digital_engagement_score'} / hanya test: {'extra_only_in_test'} |
| `x_mixed_type_numbers` | • age: string → numeric (99.3% berhasil)<br>• annual_income: string → numeric (100.0% berhasil)<br>• tenure_months: string → numeric (99.3% berhasil) |
| `x_messy_target_labels` | Mapping target : {'No': 0, 'no': 0, 'TRUE': 1, 'n': 0, 'false': 0, 'Y': 1, 'yes ': 1, '1': 1, 'Yes': 1, '0': 0} |
| `x_inf_outliers_negative` | • 16 nilai ±inf diganti NaN<br>• train.age (age): 7 nilai mustahil (di luar [0, 110]) → NaN<br>• test.age (age): 2 nilai mustahil (di luar [0, 110]) → NaN |
| `x_mixed_date_formats` | • policy_start_date: parsed sebagai tanggal (100.0%) |
| `x_empty_rows_cols_constant` | ℹ️ [train.csv] 0 baris kosong & 1 kolom kosong total dibuang<br>ℹ️ [train.csv] kolom index tersimpan ['Unnamed: 0'] (0,1,2,…) dibuang<br>ℹ️ [test.csv] 0 baris kosong & 1 kolom kosong total dibuang |
| `x_duplicates_conflicting` | Duplikat baris (fitur identik, abaikan ID): 300 / grup duplikat dengan label berbeda: 90<br>→ 300 duplikat dibuang. Train sekarang (3000, 28) |
| `x_unseen_categories` | • gender: 2 variasi ejaan/case disatukan (4 → 2 level)<br>• region: 10 variasi ejaan/case disatukan (21 → 11 level)<br>• payment_method: 4 variasi ejaan/case disatukan (8 → 4 level) |
| `x_pii_free_text` | • customer_name: data pribadi (PII: nama kolom identitas pribadi & nilai hampir unik) → tidak dipakai sebagai fitur & tidak diekspor ke dashboard<br>• email: data pribadi (PII: email) → tidak dipakai sebagai fitur & tidak diekspor ke dashboard<br>• phone: data pribadi (PII: nomor telepon) → tidak dipakai sebagai fitur & tidak diekspor ke dashboard |
| `x_bool_and_special_names` | • auto_renew: boolean-like → 1/0<br>- cancellation_reason: nama kolom mengandung kata kunci post-event; pola missing hampir identik dengan target (AUC 1.000); single-feature AUC 1.000 |
| `x_excel_title_rows_multisheet` | ℹ️ [train.xlsx] 2 sheet: ['README', 'Data'] → dipakai sheet terbesar 'Data' (set CFG.EXCEL_SHEET kalau salah)<br>ℹ️ [train.xlsx] header ditemukan di baris 4 file (ada judul/keterangan di atas tabel) → dipakai sebagai nama kolom<br>ℹ️ [test.xlsx] 2 sheet: ['README', 'Data'] → dipakai sheet terbesar 'Data' (set CFG.EXCEL_SHEET kalau salah) |
| `x_currency_scaled_strings` | • annual_income: string → numeric (100.0% berhasil)<br>• annual_premium: string → numeric (100.0% berhasil)<br>• premium_change_pct: string → numeric (100.0% berhasil) |
| `x_tab_txt_file` | ⚠️ [train.txt] ada baris dengan jumlah kolom tidak konsisten → baris rusak dilewati |
| `x_jsonl_parquet` | TRAIN_PATH                 = data/train.jsonl<br>TEST_PATH                  = data/test.parquet<br>Train shape : (3000, 29) |
| `x_target_bool_float` | Mapping target : |
| `x_status_active_inactive` | Mapping target : {'Active': 0, 'inactive': 1, 'ACTIVE': 0, 'INACTIVE': 1, 'Inactive': 1, 'active ': 0}<br>Metode         : target multi-kelas (6 status) → status aktif ['Active', 'ACTIVE', 'active '] = 0, lainnya (lapse/surrender/cancel/…) = 1 |
| `x_high_cardinality_ids` | • row_number: kolom ID numerik (nama ID & 3,000 nilai unik) → tidak dipakai sebagai fitur<br>High-card cat  : 1 ['agent_id']<br>Fitur model: 44 asli → tree=54, catboost=55, linear=54 (+one-hot) / high-card TE: ['agent_id'] |
| `x_leakage_traps` | - flag_x: single-feature AUC 1.000<br>- refund_amount: nama kolom mengandung kata kunci post-event; single-feature AUC 1.000<br>- termination_date_month: nama kolom mengandung kata kunci post-event; pola missing hampir identik dengan target (AUC 1.000); single-feature AUC 1.000 |
| `x_tiny_wide_mess` | ⚠️ Kolom dengan missing > 40%: ['avg_claim_settlement_days', 'cancellation_reason'] → missingness-nya sendiri bisa jadi sinyal (indikator dibuat otomatis).<br>18 fitur domain dibuat: ['fe_tenure_years', 'fe_tenure_band', 'fe_is_new_customer', 'fe_age_band', 'fe_premium_to_income', 'fe_sum_insured_to_premium', 'fe_has_claim', 'fe_claims_per_year', 'fe_claim_reject_rate', 'fe_ha<br>- cancellation_reason: nama kolom mengandung kata kunci post-event; pola missing hampir identik dengan target (AUC 1.000); single-feature AUC 1.000 |
| `x_constant_target` | ValueError: Target 'churn' hanya punya 1 kelas (semua = {'No': 0}) → model churn tidak bisa dilatih. Cek: (1) TARGET_COL benar? (2) file label terpisah sudah di-set di CFG.TRAIN_LABELS? (3) POSITIVE_LABEL benar? (Target  |

Catatan:
- `x_duplicate_columns`: pandas memberi akhiran `age.1` saat membaca. Kedua kolom dipakai dengan nama berbeda, terlihat di insight "age, age.1".
- `x_target_bool_float`: mapping `{'0.0': 0, '1.0': 1}`.
- `x_jsonl_parquet`: train dibaca dari `.jsonl` dan test dari `.parquet`.

## 4. Demo end-to-end tim Warkab

Case fiktif **PT Asuransi Nusantara Sejahtera** (`examples/mock_case_warkab/casebook.md`):
- 1,2 juta polis;
- churn naik dari 15,2% ke 20,6%;
- budget retensi Rp1,5 miliar;
- parameter bisnis diberikan soal.

Data sintetis: 8.000 train + 2.000 test + tabel klaim, sengaja berantakan.

| Langkah | Perintah | Hasil |
|---|---|---|
| Siapkan case | `python examples/mock_case_warkab/make_mock_case.py <folder>` | folder kerja + RESEARCH_PLAN + workbook riset |
| Run penuh | double-click `RUN_FULL.bat` | 49,4 menit (sambil 3 stress test paralel), 0 section error |
| Model | — | hill-climbing ensemble (XGBoost-FS, LogReg, CatBoost), OOF ROC-AUC 0,760 (95% CI 0,748–0,772); **AUC pada test tersembunyi 0,782** |
| Leakage | — | `cancellation_reason` terdeteksi & dibuang otomatis |
| Artikel | `Warkab_Final Stage 1.pdf` | 84 halaman total: cover + **10 halaman isi** + appendix A–L |
| ZIP | `python tools/make_zip.py --case <folder>` | `Warkab_Final Stage 1.zip` (PDF + notebook ter-eksekusi + supporting) |
| QA | `python QA/qa_check.py --case <folder>` | 43 PASS · 0 FAIL · 2 WARN (termasuk gaya tulisan 98/100) |

Isi artikel yang dicek mengikuti case:
- **Executive summary**:
  - value at risk sampel Rp9,9 miliar, sekitar Rp1.490 miliar pada skala portofolio 1,2 juta nasabah;
  - paragraf custom tim di akhir.
- **Introduction**:
  - konteks soal;
  - 2 fakta casebook (1,2 juta polis, premi bruto Rp4,8 T, biaya akuisisi Rp1,1 juta);
  - 2 fakta industri AAJI dengan sitasi.
- **Bab 4**: budget Rp1,5 M adalah *binding constraint*. Budget membiayai sekitar 10.000 kontak (0,8% portofolio) dengan net sekitar Rp12,2 miliar (ROI 8,1×). Kesimpulannya: budget dikonsentrasikan pada nasabah dengan expected loss tertinggi.
- **Rekomendasi**: paragraf custom tentang aplikasi Q1 2026 & kemitraan auto-debit (dari casebook).
- **Discussion**:
  - menjawab ke-4 pertanyaan soal;
  - angka RQ4 konsisten dengan Bab 4 (sampel, portofolio, dalam budget);
  - literatur tim (Eling & Kiesenbauer 2014; Gottlieb & Smetters 2021; Fallis et al. 2022) dikaitkan dengan driver.
- **Appendix B**: dukungan metode dari literatur tim (Devriendt et al., 2021).
- **Dashboard**: judul, perusahaan, tim & anggota, konteks & pertanyaan soal, KPI, driver, timing, model, kampanye, aksi, metodologi. Semuanya dari run ini.

Dua WARN: 2 dari 5 literatur tim tidak dipakai karena Discussion memilih 3 literatur yang paling cocok dengan driver teratas. Literatur itu tetap bisa dipakai lewat sheet `custom_paragraphs`.

## 5a. Kualitas tulisan & kedalaman appendix (putaran akhir)

Generator narasi diaudit dengan aturan tiga skill: **ai-paraphrase** (Wikipedia: Signs of AI writing), **anti-ai-slop-writing** dan **stop-slop**. Aturannya disesuaikan untuk ragam akademik: tanpa kontraksi, dan pasif masih boleh di bagian metode. Perbaikannya dilakukan di sumber, jadi paper hari-H otomatis ikut bersih:

- Em dash di kalimat diubah: yang berpasangan jadi kurung, yang tunggal jadi koma. Rentang angka seperti 13,2–30,6 tidak disentuh.
- "The conclusion is robust" dan "Most importantly" diganti pernyataan langsung. "Doubly robust" tetap dipakai karena istilah statistik baku.
- Label mentah dalam kalimat diganti frasa wajar, misalnya:
  - "customers whose premium change at last renewal is between 13.2% and 30.6%";
  - "between 18 and 24 months of tenure";
  - "keeping the premium change at the last renewal at or below its median (4.1%)";
  - "auto-renewal = No" (bukan '0').
- Kesalahan tata bahasa diperbaiki:
  - "answer three questions" padahal ada 4 RQ, kini "four research questions";
  - "1 related table(s)" kini "One related table (claims) was…";
  - "a 11.7 pp" kini "an 11.7 pp";
  - huruf kapital di tengah daftar rekomendasi.
- Urutan kalimat tujuan → RQ diperbaiki, dan jawaban RQ di Discussion ditulis satu kalimat per RQ.
- Bug heading "4.4 Churn personas" tanpa isi (terjadi saat autofit memangkas paragrafnya) sudah diperbaiki.

Hasil `QA/slop_check.py` (skor 0–100, aman ≥ 80):

| Paper | Sebelum | Sesudah |
|---|---|---|
| Demo Warkab (isi utama) | 68 (15 em dash, "robust", "Most importantly") | **98** (0 em dash, 0 kosakata khas AI) |
| 43 paper dari stress test (semua bentuk data) | — | **min 93, median 98** |

Kedalaman appendix (paper demo: 78 → 83 halaman):

- **Observasi kunci berbasis data** di awal appendix A, C, E, F, G, H, I, J. Contohnya:
  - 35 dari 52 variabel tetap signifikan setelah koreksi Benjamini–Hochberg;
  - uji Schoenfeld tidak menolak asumsi proportional hazards;
  - perjalanan model dari AUC baseline ke final;
  - PSI drift terbesar;
  - rentang AUC per segmen;
  - porsi atribusi SHAP 5 fitur teratas;
  - 3 dari 3 efek kausal lolos semua uji, dengan E-value terkecil;
  - spread risiko 18× antar desil;
  - selisih AUC terbesar antar grup (audit fairness).
- **Appendix K (baru): metodologi & rumus**:
  - IV/WoE, interval Wilson, Benjamini–Hochberg;
  - Kaplan–Meier, Cox, RMST;
  - DeLong, Brier, ECE;
  - EMPC, CLV;
  - AIPW, E-value;
  - PSI dan ukuran sampel pilot;
  - semuanya dengan sitasi.
- **6 tabel tambahan**: ringkasan numerik, baseline default, bootstrap berpasangan, permutation importance untuk seleksi fitur, performa per segmen, profil error.
- Urutan akhir: A–J analisis, K rumus, L reproducibility, M figure tambahan (bila ada).

Skor gaya tulisan per varian stress test:

| Varian | Skor | Temuan | Kata isi utama |
|---|---|---|---|
| all_categorical | 96 | 2 | 2,092 |
| baseline_claims | 96 | 2 | 1,956 |
| date_only_tenure | 96 | 2 | 2,270 |
| excel_files | 98 | 1 | 1,954 |
| extreme_imbalance | 98 | 1 | 1,970 |
| float_ids_numeric_target | 98 | 1 | 1,953 |
| full_mode_small | 98 | 1 | 1,976 |
| heavy_missing | 98 | 1 | 1,956 |
| indonesian_columns | 98 | 1 | 1,954 |
| inverted_is_active | 98 | 1 | 1,949 |
| label_metric_f1 | 96 | 2 | 1,967 |
| labels_separate_file | 98 | 1 | 1,943 |
| multiclass_status | 98 | 1 | 1,940 |
| no_tenure_no_premium | 96 | 2 | 2,240 |
| no_test | 98 | 1 | 1,949 |
| panel_monthly | 98 | 1 | 1,938 |
| semicolon_latin1 | 98 | 1 | 1,956 |
| single_file_missing_target | 98 | 1 | 1,960 |
| start_end_dates | 98 | 1 | 1,978 |
| text_and_one_to_one | 98 | 1 | 1,969 |
| tiny | 98 | 1 | 1,919 |
| wide_noise | 98 | 1 | 1,952 |
| x_bom_spaces_headers | 98 | 1 | 1,932 |
| x_bool_and_special_names | 98 | 1 | 1,933 |
| x_currency_scaled_strings | 98 | 1 | 1,949 |
| x_duplicate_columns | 98 | 1 | 1,951 |
| x_duplicates_conflicting | 98 | 1 | 1,952 |
| x_empty_rows_cols_constant | 98 | 1 | 1,969 |
| x_excel_title_rows_multisheet | 98 | 1 | 1,959 |
| x_high_cardinality_ids | 98 | 1 | 1,961 |
| x_inf_outliers_negative | 96 | 2 | 1,948 |
| x_jsonl_parquet | 98 | 1 | 1,943 |
| x_leakage_traps | 98 | 1 | 1,965 |
| x_messy_target_labels | 98 | 1 | 1,944 |
| x_mixed_date_formats | 97 | 2 | 2,296 |
| x_mixed_type_numbers | 98 | 1 | 1,964 |
| x_pii_free_text | 98 | 1 | 1,950 |
| x_status_active_inactive | 98 | 1 | 1,947 |
| x_tab_txt_file | 98 | 1 | 1,938 |
| x_target_bool_float | 98 | 1 | 1,945 |
| x_test_columns_mismatch | 98 | 1 | 1,951 |
| x_tiny_wide_mess | 93 | 4 | 2,231 |
| x_unseen_categories | 98 | 1 | 1,942 |

## 5b. Putaran terakhir: equation, sentuhan manusia, kebersihan ZIP

- **Equation bernomor**:
  - Isi utama 4.2 memuat (1) CLV yang benar-benar dipakai notebook, CLVᵢ = m·Pᵢ·(1 − ρᵢᴴ)/(1 − ρᵢ) dengan ρᵢ = (1 − pᵢ)/(1 + d), dan (2) profit kampanye Π(k).
  - Bagian 4.3 memuat estimator AIPW (bisa dipangkas autofit bila halaman penuh).
  - Appendix K kini berisi ±16 equation bernomor: IV/WoE, Wilson, Benjamini–Hochberg, Kaplan–Meier, Cox, RMST, Brier, ECE, EMPC, CLV, AIPW, E-value, PSI, ukuran sampel pilot.
- **Insurance KPI**: rasio persistensi 13/25 bulan (3.2 dan Appendix E) dan churn berbobot premi (4.1).
- **`SENTUHAN_MANUSIA.md`** dibuat otomatis setiap run. Isinya draf paragraf berangka untuk:
  - suara aktuaria;
  - cerita iterasi model;
  - ambang operasional & governance;
  - insight lokal per driver (dengan pertanyaan pemandu);
  - checklist guidebook dan template deklarasi AI.

  Bagian `[ISI DARI CASE]` diisi tim, lalu ditempel ke `custom_paragraphs` supaya ikut setiap rerun.
- **Kebocoran catatan internal ke ZIP diperbaiki**. Sebelumnya `JUDGE_QA.md`, `NARRATIVE_OPTIONS.md` dan `REPORT_TODO.md` ikut ZIP pengumpulan. Sekarang `make_zip.py` dan cell ZIP notebook mengecualikan semua catatan internal; terverifikasi 0 file internal di ZIP demo.
- **Verifikasi akhir**:
  - stress test 44/44 lolos;
  - 43 paper dari stress test punya skor gaya minimal 96 (median 98);
  - demo full: 0 error, 49 menit, OOF AUC 0,760, AUC test tersembunyi 0,782, 10 halaman isi (84 total), qa_check 43 PASS · 0 FAIL, slop 98/100.

## 5. Regresi & perbaikan pada QA final

Tidak ada downgrade:
- jumlah cell notebook sama (154, 90 code);
- semua section lama tetap ada;
- AUC fast run pada data & seed yang sama identik (0,7575) sebelum dan sesudah seluruh patch QA ini.

Celah yang **ditemukan oleh QA dan sudah diperbaiki** (lalu diuji ulang):

| Temuan | Perbaikan | Diuji ulang dengan |
|---|---|---|
| Target hanya 1 kelas → error di tahap akhir yang membingungkan | Guard di "Parse target": berhenti dengan pesan + key yang harus dicek | `x_constant_target` |
| Data sangat kecil → error di "Driver heterogeneity" | Ambang segmen adaptif; dilewati dengan alasan jika segmen < 2 | `x_tiny_wide_mess` |
| Kolom nama/email/no HP/alamat ikut jadi fitur | Deteksi PII (nama kolom + pola nilai) → dikecualikan dari model; tanpa false positive pada varian lain (stress test final) | `x_pii_free_text` + semua varian |
| Index pandas tersimpan (`Unnamed: 0`) terpilih sebagai ID | Kolom index 0,1,2,… dibuang saat membaca | `x_empty_rows_cols_constant` |
| Caption appendix berupa nama file (`validation_design`, `causal_dag`) | Caption deskriptif otomatis | demo full (Figure B.2, H.2) |
| RQ4 di Discussion hanya angka sampel | RQ4 menyebut skala portofolio + hasil dalam budget | demo full |
| Console penuh traceback `KeyError joblib_memmapping_folder` (bug pembersih joblib di Windows, tidak berbahaya) | stderr kernel dialihkan ke `kernel_stderr.log` | run cepat final (console bersih) |

## 6. Cara mengulang semua bukti ini (tanpa AI)

```
python tools/stress_test.py --out stress_runs --jobs 3
python examples/mock_case_warkab/make_mock_case.py latihan
python tools/run_case.py --config latihan/case_config.json
python tools/make_zip.py --case latihan
python QA/qa_check.py --case latihan
python QA/slop_check.py "latihan/outputs/churn_insurance/Warkab_Final Stage 1.pdf"
python QA/make_walkthrough.py --case latihan --out rekaman --stress tools/STRESS_TEST_REPORT.md
```

- Langkah 1: ±1,5–3 jam (3 paralel). Hasilnya `stress_runs/STRESS_TEST_REPORT.md`.
- Langkah 3 bisa diganti double-click `latihan/RUN_FULL.bat`.
- Langkah 6 menghasilkan video, screenshot, dan STEPS.md.

## 7. Batasan yang jujur

- Data dari panitia yang benar-benar di luar churn biner (misalnya regresi nilai klaim, teks/gambar) diarahkan ke template lain (`02_Tabular`, `03_NLP`, `04_Computer_Vision`) dengan pesan jelas.
- Riset latar belakang tetap membutuhkan tim:
  - template menyediakan keyword, link, metode, workbook, dan injeksi otomatis;
  - kebenaran sumber harus dibuka & diverifikasi sendiri (kolom `verified`).
- PDF memerlukan MS Word atau LibreOffice. Tanpa keduanya, DOCX tetap jadi dan PDF dibuat manual.
- Deploy dashboard ke Vercel memerlukan login Vercel milik tim sendiri.
