# ▶ MULAI DI SINI — Runbook Final (Churn / Insurance)

Satu prosedur dari **menerima data → upload ZIP**. Ikuti urut. Dokumen pendukung:
- `PLAYBOOK_ANALISIS.md` — aturan "jika X → Y", statistik, istilah asuransi, strategi retensi, Q&A juri
- `PANDUAN_LAPORAN.md` — struktur artikel, template kalimat, tips, referensi
- `BAHAN_LATAR_BELAKANG.md` — **latar belakang, tinjauan pustaka, justifikasi metode, rumusan masalah/tujuan/manfaat (EN + ID), fakta industri Indonesia terverifikasi (OJK/AAJI/AAUI), daftar pustaka APA terverifikasi**
- `CONTOH_LAPORAN_FINAL/` — contoh artikel final lengkap (data asuransi nyata dari Kaggle) untuk ditiru struktur & gaya tulisnya
- `churn_insurance_master.ipynb` — notebook utama (Section 0–25)

---

## FASE 0 — Persiapan (sebelum soal dibuka)
- [ ] Repo sudah di laptop; `00_Setup/00_environment_check.ipynb` sudah dijalankan → semua inti ✅.
- [ ] Buat folder kerja, misal `final/` → copy `churn_insurance_master.ipynb` ke sana, buat subfolder `final/data/`.
- [ ] Latihan sekali dengan data sintetis: `python tools/make_synthetic_insurance_churn.py --out final/data`.

## FASE 1 — Baca soal & setup (≈ 15 menit)
Catat dari soal → isi di cell **USER OVERRIDE**:

| Yang dicari di soal | Isi ke | Contoh |
|---|---|---|
| Nama file data | `TRAIN_PATH`, `TEST_PATH`, `SAMPLE_SUB_PATH` | `"./data/train.csv"` |
| Kolom target & arti nilainya | `TARGET_COL`, `POSITIVE_LABEL` | `"Status"`, `"Lapsed"` |
| Kolom ID | `ID_COL` | `"policy_id"` |
| Metrik penilaian prediksi | `METRIC` | `"roc_auc"` / `"f1"` |
| Format submission (probabilitas / label) | `SUBMISSION_MODE` | `"probability"` |
| Tabel tambahan (klaim, pembayaran, keluhan) | `EXTRA_TABLES` / `EXTRA_ONE_TO_ONE` | lihat contoh di cell |
| Kolom yang jelas post-churn / tidak relevan (nama, alamat) | `DROP_COLS` | `["cancel_date"]` |
| Parameter bisnis (margin, biaya kampanye) | `PROFIT_MARGIN`, `RETENTION_COST`, `RETENTION_SUCCESS_RATE` | kalau tidak ada → pakai default & sebut "asumsi" |
| Nama perusahaan, nama tim | `COMPANY_NAME`, `TEAM_NAME` | |
| Periode premi (bulanan/tahunan) | `VALUE_PERIOD` | `"monthly"` |

Lalu set `CFG.RUN_MODE = "fast"` → **Kernel → Restart & Run All**.

## FASE 2 — Validasi hasil fast mode (≈ 15 menit)
Cek output berikut **berurutan**. Kalau ada yang salah → perbaiki config → run ulang.

| Section | Yang dicek | Kalau salah |
|---|---|---|
| 3.1 Detect target & ID | target & ID benar | set `TARGET_COL` / `ID_COL` |
| 3.2 Parse target | mapping (churn = 1), churn rate masuk akal | `POSITIVE_LABEL` |
| 3.3 Cleaning log | konversi tipe masuk akal | `FORCE_NUMERIC` / `FORCE_CATEGORICAL` |
| 3.4 Quality report | missing, nilai mustahil, duplikat | catat untuk laporan (bagian Data) |
| 5.1 Roles | tenure, premium, claims, dll. terdeteksi benar | `COLUMN_ROLES = {...}` |
| 5.3 Leakage screen | kolom post-event ter-flag & dibuang | `DROP_COLS` |
| 14 Leaderboard | semua model ≫ dummy, AUC tidak > 0.97 | cek leakage / target |
| 24 Ringkasan run | "Section error: tidak ada" | baca error → Troubleshooting (Section 25) |

## FASE 3 — Full run (≈ 30–90 menit, jalan di background)
- `CFG.RUN_MODE = "full"`, `CFG.FIG_DPI = 300` → Restart & Run All.
- Waktu terbatas? `CFG.USE_OPTUNA = False` atau `CFG.OPTUNA_TIMEOUT = 300`.
- **Sambil menunggu**: mulai tulis Introduction & Methodology dari `PANDUAN_LAPORAN.md` (tidak tergantung angka akhir).

## FASE 4 — Rangkai laporan (≈ 60–90 menit)
Setelah full run selesai, di `outputs/churn_insurance/`:

1. Buka **`REPORT_TODO.md`** → ini daftar kerja kamu.
2. Buka **`REPORT_DRAFT.docx`** (sudah A4, TNR 12, spasi 1.15, margin 4/3 cm, berisi angka & figure run ini).
3. Kerjakan semua bagian **kuning `[EDIT: ...]`**. Untuk latar belakang/tinjauan pustaka/diskusi, ambil paragraf dari `BAHAN_LATAR_BELAKANG.md` (§C) lalu sesuaikan.
4. Parafrase kalimat otomatis; ganti nama fitur teknis jadi bahasa bisnis (`fe_premium_to_income` → "premium-to-income ratio").
5. Baca `insights.md` → pilih temuan paling kuat yang belum ada di draft.
6. Cek halaman ≤ 10 (tanpa cover & appendix). Kalau MS Word ada, notebook sudah menghitung otomatis ("isi utama ≈ N hal") dan membuat `REPORT_DRAFT.pdf`. Kelebihan → pindahkan figure ke Appendix, ringkas.
7. Save As PDF: **`TeamName_Final Stage 1.pdf`**.

### Peta output → bagian laporan
| Bagian laporan | Ambil dari |
|---|---|
| Executive summary | `figures/*executive_summary*`, `insights.md` (Business, Drivers, Recommendations) |
| Data & methodology | `tables/data_quality_report.csv`, `leakage_screen.csv`, log cleaning (Section 3.3), `run_summary.json` |
| Key drivers | `driver_evidence_matrix.csv`, `figures/*driver_churn_rate_1*`, `*information_value*`, `logit_odds_ratios.csv` |
| Churn reasons (kalau ada kolom alasan) | `churn_reasons_*.csv`, `figures/*churn_reasons*` |
| When customers churn | `figures/*km_by_group*`, `*hazard_by_tenure*`, `cox_hazard_ratios.csv` |
| High-risk segments | `segment_rules.csv`, `figures/*interaction_heatmaps*`, `*segment_tree*` |
| Model | `leaderboard_all.csv`, `bootstrap_ci_final_model.csv`, `bootstrap_model_comparison.csv`, `figures/*gains_and_lift*`, `*roc_pr*` |
| Explainability | `figures/*shap_beeswarm*`, `*shap_dependence*`, `*partial_dependence*`, `driver_heterogeneity_*.csv` |
| Business impact | `risk_tiers.csv`, `risk_value_quadrants.csv`, `campaign_optimum.csv`, `campaign_sensitivity.csv`, `what_if_scenarios.csv`, `churn_personas.csv` |
| Recommendations | `recommendations.csv` (+ library di `PLAYBOOK_ANALISIS.md` §F) |
| Lampiran | figure lain + `report_tables.xlsx` |

## FASE 5 — Submit (≈ 10 menit)
- [ ] `submission.csv` lolos validator (Section 23, semua ✅) dan formatnya sesuai soal.
- [ ] Notebook di-run bersih (Restart & Run All) & disimpan (dengan output → bukti analisis).
- [ ] `CFG.ARTICLE_PDF_PATH = "...pdf"`, `CFG.MAKE_ZIP = True` → jalankan cell 24.4 → `TeamName_Final Stage 1.zip`.
- [ ] Cek isi ZIP: PDF + `.ipynb` + `supporting/`.
- [ ] Upload.

---

## Kalau ada masalah di tengah jalan
| Situasi | Langkah |
|---|---|
| Notebook error di section tertentu | lihat pesan ❌ → tabel Troubleshooting (Section 25) / `Guides/DEBUGGING_TANPA_AI.md`. Section lain tetap jalan. |
| Waktu hampir habis, full run belum selesai | pakai hasil fast mode untuk laporan (sebut 3-fold CV), submission dari fast mode lebih baik daripada tidak ada |
| Data bukan churn biner (misal jumlah klaim, nilai premi) | pakai `02_Tabular/tabular_master.ipynb` (regresi) + ambil ide analisis bisnis dari notebook ini |
| Soal minta segmentasi tanpa label | `06_Clustering_Segmentation/clustering_segmentation.ipynb` (ada RFM & profiling bisnis) |
| Ada data per bulan (time series premi/klaim) | `05_Time_Series/time_series_forecasting.ipynb` |
| Ada kolom teks (keluhan) | fitur sederhana di `custom_feature_engineering` atau `03_NLP/` |
| Hasil berbeda dari intuisi | lihat PLAYBOOK §C (confounding, U-shape, non-actionable) → justru jadikan insight |

## Prinsip nilai tinggi
1. **Jawab pertanyaan bisnis**, bukan pamer model.
2. **Setiap klaim ada angka & bukti** (effect size, CI, konsistensi antar metode).
3. **Rekomendasi spesifik & terukur** (segmen, aksi, dampak, KPI, timeline, A/B test).
4. **Metodologi rapi**: leakage dicegah, CV OOF, uji statistik + koreksi multiple testing, ketidakpastian dilaporkan.
5. **Jujur soal batasan** (asosiasi ≠ kausal, asumsi ROI).
