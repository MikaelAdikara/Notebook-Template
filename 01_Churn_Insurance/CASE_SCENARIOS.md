# CASE SCENARIOS — semua kemungkinan bentuk case & data → apa yang dilakukan

Pakai tabel ini setelah membaca soal. Kolom **Otomatis?** = notebook sudah menangani tanpa setting; **Set** = key di `case_config.json` (atau USER OVERRIDE); **Laporan** = bagian artikel yang berubah.
Bentuk data A1–A12 dan B1–B12 sudah diuji end-to-end dengan `tools/stress_test.py` — **22 varian, semua PASS tanpa section error** (lihat `../tools/STRESS_TEST_REPORT.md`). B13 (`TREATMENT_COLS`) memakai jalur kode AIPW yang sama dengan fitur actionable yang sudah teruji.

## A. Bentuk data & target

| # | Skenario | Otomatis? | Set | Laporan |
|---|---|---|---|---|
| A1 | train + test + sample_submission (standar) | ✅ | path saja | — |
| A2 | Target nama aneh (`Status`, `is_lapsed`, `berhenti`) | ✅ deteksi nama/kolom yang tidak ada di test | `TARGET_COL` kalau salah | 2.1 |
| A3 | Target terbalik (`is_active`, `retained`, `renewed`) | ✅ dibalik otomatis (dicetak) | `POSITIVE_LABEL` kalau salah | 2.1 |
| A4 | Target multi-kelas (`Active/Lapsed/Surrendered/Cancelled`) | ✅ status aktif = 0, sisanya = 1 | `POSITIVE_LABEL: ["Lapsed","Surrendered"]` untuk memilih | 2.1 (definisi churn — isi `CHURN_DEFINITION`) |
| A5 | Target hitungan (jumlah klaim) / kontinu | hitungan ✅ (>0 = event); kontinu → berhenti dengan pesan | kontinu: pakai `02_Tabular` (regresi) | — |
| A6 | **Hanya 1 file**, baris target kosong = yang harus diprediksi | ✅ (≥5% kosong → jadi test) | `TEST_FROM_MISSING_TARGET` | — |
| A7 | Tanpa test sama sekali | ✅ analisis + CV, submission di-skip | `TEST_PATH: null` | — |
| A8 | Label di file terpisah (`train_labels.csv`) | — | `TRAIN_LABELS: {"path": ..., "key": ...}` | — |
| A9 | CSV `;` / encoding latin-1 / desimal koma / Excel / parquet / json | ✅ | — | — |
| A10 | Angka dalam teks (`"Rp 5.000.000"`, `"12,5%"`, `"50000 - 74999"`) | ✅ | `FORCE_NUMERIC` kalau terlewat | 2.1 (cleaning log) |
| A11 | ID float (`2213…0.0`) vs integer di sample | ✅ disamakan | — | — |
| A12 | Kolom bahasa Indonesia (`umur`, `premi`, `lama_polis`, `metode_bayar`) | ✅ role keyword EN+ID | `COLUMN_ROLES` kalau role salah | — |

## B. Struktur data

| # | Skenario | Otomatis? | Set | Laporan |
|---|---|---|---|---|
| B1 | Multi-tabel 1-ke-banyak (klaim, pembayaran, keluhan) | agregasi count/sum/mean/recency | `EXTRA_TABLES` | 2.1 |
| B2 | Tabel 1-ke-1 (demografi terpisah) | merge aman (cek duplikat key) | `EXTRA_ONE_TO_ONE` | — |
| B3 | Data panel / snapshot bulanan (customer berulang) | ✅ group key terdeteksi → StratifiedGroupKFold | `GROUP_COL`, `ID_COL` (ID baris) | 2.3 (validasi) |
| B4 | Banyak polis per customer, churn level polis | ✅ seperti B3 (group = customer) | `GROUP_COL: "customer_id"` | sebut di 2.1 |
| B5 | Tanpa kolom tenure, ada **tanggal mulai + tanggal berhenti** | ✅ durasi survival direkonstruksi (end−start; aktif tersensor di tanggal acuan) | `REFERENCE_DATE` (tanggal snapshot) | 3.2 |
| B6 | Tanpa tenure & tanpa tanggal berhenti | survival di-skip (mencegah bias, dicetak alasannya) | — | 3.2 hilang otomatis |
| B7 | Tanpa premi / nilai | analisis bisnis dalam "jumlah customer", EMPC relatif | `VALUE_COL` kalau ada nama lain | 4.x menyesuaikan |
| B8 | Kolom post-churn (alasan, tanggal batal, refund) | ✅ leakage screen (nama + missingness + AUC + model-level); alasan dipakai deskriptif | `DROP_COLS` tambahan | 2.1 + 3.1 (stated reasons) |
| B9 | Kolom teks bebas (keluhan) | dikecualikan dari model (tipe text) | fitur sederhana di `custom_feature_engineering` / `03_NLP` | — |
| B10 | Data sangat kecil (< 1.000) | ✅ | — | — |
| B11 | Data sangat besar (> 150k) | ✅ auto-adapt (RF/ET off, subsample tuning/Cox/SHAP) | `RUN_MODE` | — |
| B12 | Sangat imbalanced (< 5%) | ✅ metrik PR-AUC/EMPC ditonjolkan | `METRIC` | 3.4 |
| B13 | Data historis kampanye retensi (kolom "dapat penawaran") | AIPW otomatis pada fitur actionable | **`TREATMENT_COLS: ["received_offer"]`** → efek kausal intervensi nyata + uplift | 4.3 (bukti terkuat!) |

## C. Pertanyaan / tujuan soal

| # | Soal meminta… | Yang dipakai | Set |
|---|---|---|---|
| C1 | "Faktor apa yang memengaruhi churn" | 3.1 + evidence matrix + Appendix C/D/G | — |
| C2 | "Kapan nasabah churn / masa kritis" | 3.2 + Appendix E | — |
| C3 | "Siapa yang harus diprioritaskan" | risk tiers, risk × value, `test_customer_action_list.csv` | — |
| C4 | "Prediksi churn (leaderboard)" | `submission.csv` (validator), metrik sesuai `METRIC` | `METRIC`, `SUBMISSION_MODE` |
| C5 | "Strategi retensi + dampak finansial" | 4.2 + 5 + EMPC + sensitivity | parameter bisnis, `RETENTION_BUDGET` |
| C6 | "Program retensi dengan anggaran X" | kampanye optimal dalam budget (otomatis di 4.2) | `RETENTION_BUDGET` |
| C7 | "Intervensi mana yang efektif" | 4.3 kausal + uplift; desain pilot A/B | `TREATMENT_COLS`, `AVAILABLE_INTERVENTIONS` |
| C8 | Pertanyaan spesifik (daftar 3–5) | jadi Research Questions | `CASE_QUESTIONS` |
| C9 | Segmentasi tanpa label | `06_Clustering_Segmentation` + ide persona dari 21.8 | — |
| C10 | Prediksi nilai (CLV, premi, klaim) | `02_Tabular` (regresi) + analisis bisnis dari notebook ini | — |
| C11 | Forecast churn rate bulanan | `05_Time_Series` | — |
| C12 | Dashboard / monitoring | `outputs/.../dashboard` (Vercel) + model card + MLOps loop | — |

## D. Konteks bisnis & laporan

| # | Kondisi | Set | Efek |
|---|---|---|---|
| D1 | Asuransi jiwa (lapse/surrender, unit link) | `INSURANCE_LINE: "life"` (auto) | istilah "lapse or surrender", paragraf AAJI/SEOJK PAYDI |
| D2 | Asuransi umum (kendaraan/properti, non-renewal) | `"general"` (auto) | istilah "non-renewal", paragraf AAUI |
| D3 | Multi-line | `"multi"` (auto bila campuran) | istilah gabungan |
| D4 | Perusahaan fiktif / bukan Indonesia | `MARKET: "Global"` | konteks OJK/AAJI tidak dipakai |
| D5 | Soal memberi margin/biaya/success rate | parameter bisnis | ditulis "as given in the case" (sesuaikan kalimat) |
| D6 | Soal tidak memberi parameter | biarkan default | ditulis sebagai asumsi + sensitivity 9 skenario |
| D7 | Artikel wajib Bahasa Indonesia | generator menulis EN → terjemahkan di Word (struktur & angka tetap) | — |
| D8 | Referensi tidak dihitung dalam 10 halaman | `REFERENCES_COUNT_IN_LIMIT: false` | autofit memberi ruang lebih untuk figure |
| D9 | Ingin judul/angle tertentu | `REPORT_TITLE` atau `NARRATIVE_ANGLE` | judul & framing |

## E. Snippet pra-proses (kalau benar-benar perlu)

```python
import pandas as pd
df = pd.read_csv("data/raw.csv")
# (1) target dari tanggal: churn kalau polis berakhir/tidak diperpanjang dalam window
df["churn"] = (pd.to_datetime(df["end_date"]) <= pd.Timestamp("2024-12-31")).astype(int)
# (2) customer-level dari policy-level: churn = semua polis berhenti
cust = df.groupby("customer_id").agg(churn=("churn", "min"), n_policies=("policy_id", "nunique"), premium=("premium", "sum")).reset_index()
cust.to_csv("data/train.csv", index=False)
```
Lalu arahkan `TRAIN_PATH` ke file baru. Kolom tanggal yang dipakai membuat target → masukkan ke `DROP_COLS` (leakage).
