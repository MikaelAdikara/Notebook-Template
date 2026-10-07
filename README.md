# Notebook Template — Data Analytics Competition

Kumpulan template notebook Python (`.ipynb`) siap pakai untuk lomba data analytics/data science, dengan fokus utama **customer churn & data asuransi**. Setiap notebook:

- **End-to-end**: load → cleaning → EDA → preprocessing → modeling (CV OOF) → tuning → ensemble → evaluasi & debugging → explainability → output/submission.
- **Tahan error**: library opsional dicek otomatis (auto-install yang belum ada), setiap model/section dibungkus supaya satu kegagalan tidak menghentikan notebook, kompatibel lintas versi library.
- **Penuh panduan** (Bahasa Indonesia, istilah teknis English): tujuan tiap langkah, cara membaca output, aturan **"Jika X → Y"**, catatan **"Untuk laporan"**, tabel troubleshooting, recipes, dan checklist.
- **Report-ready**: figure bernomor otomatis (DPI bisa 300), tabel CSV/Excel, dan kalimat insight (English) yang siap diparafrase.

> Jalankan di **Jupyter / VS Code lokal** (sesuai aturan lomba: Google Colab tidak diperbolehkan).

---

## Struktur repo

```
00_Setup/
  00_environment_check.ipynb        ← JALANKAN PERTAMA di laptop lomba (cek & install package, GPU)
01_Churn_Insurance/                 ← ⭐ UTAMA untuk case churn / asuransi
  churn_insurance_master.ipynb      ← analisis + prediksi + rekomendasi bisnis, end-to-end
  PLAYBOOK_ANALISIS.md              ← "jika X maka Y", cheat-sheet statistik, istilah asuransi, strategi retensi, Q&A juri
  PANDUAN_LAPORAN.md                ← struktur artikel 10 halaman, mapping figure → bab, template kalimat, referensi
  Article_Template_Final_Stage.docx ← template Word sesuai format soal (A4, TNR 12, 1.15, margin 4/3 cm)
02_Tabular/
  tabular_master.ipynb              ← klasifikasi biner/multikelas & regresi tabular umum
03_NLP/
  nlp_classification.ipynb          ← teks → kelas (TF-IDF, embedding, transformer K-fold)
  nlp_regression.ipynb              ← teks → angka
04_Computer_Vision/
  cv_image_classification.ipynb     ← gambar → kelas (timm / torchvision / fallback CNN)
  CV_OTHER_TASKS_GUIDE.md           ← deteksi objek, segmentasi, OCR, dll.
05_Time_Series/
  time_series_forecasting.ipynb     ← forecasting single/panel (baseline, ETS/SARIMAX, LightGBM global)
06_Clustering_Segmentation/
  clustering_segmentation.ipynb     ← segmentasi customer (KMeans/GMM/HDBSCAN, RFM, profiling bisnis)
Guides/
  CHEATSHEET_METRIK_MODEL_VALIDASI.md
  DEBUGGING_TANPA_AI.md
tools/
  make_synthetic_insurance_churn.py ← generator data latihan asuransi (messy + driver yang diketahui)
requirements.txt
```

---

## Mulai cepat (hari H)

1. **Clone / copy** repo ke laptop lomba.
2. Buka `00_Setup/00_environment_check.ipynb` → **Restart & Run All** → kalau ada install, restart kernel & run lagi sampai semua inti ✅.
3. Pilih template (lihat tabel di bawah), copy ke folder kerja, taruh data di `./data/`.
4. Edit **hanya** cell `# >>> USER OVERRIDE` (path, nama target/ID, metrik). Jalankan `RUN_MODE = "fast"` dulu.
5. Baca output & panduan → perbaiki config → `RUN_MODE = "full"` → **Restart & Run All**.
6. Ambil `outputs/<notebook>/` (figures, tables, insights.md, submission.csv) untuk laporan & submit.

| Soal | Template |
|---|---|
| Churn / retensi / lapse / attrition (+ butuh insight & rekomendasi) | `01_Churn_Insurance/churn_insurance_master.ipynb` |
| Tabular lain (klasifikasi/regresi) | `02_Tabular/tabular_master.ipynb` |
| Teks | `03_NLP/...` |
| Gambar | `04_Computer_Vision/...` |
| Data deret waktu / forecasting | `05_Time_Series/...` |
| Segmentasi tanpa label | `06_Clustering_Segmentation/...` |

---

## ⭐ Churn & Insurance master notebook — ringkasan isi

| # | Section | Highlight |
|---|---|---|
| 0–1 | Setup & Config | auto-install, availability flags, `CFG` + `USER OVERRIDE`, fast/full mode |
| 2 | Load data | csv/xlsx/parquet/json, auto separator/encoding, **multi-tabel** (merge 1-1, agregasi 1-many: claims/payments) |
| 3 | Data quality & cleaning | deteksi target/ID otomatis, parsing label churn (Yes/No, Exited, Attrited, is_active terbalik), angka-dalam-string (`"12,500,000"`, `"Rp 5.000.000"`), tanggal, typo kategori, nilai mustahil, duplikat, quality report |
| 4 | Target | churn rate, imbalance, baseline |
| 5 | Roles & domain FE | deteksi role (tenure, premi, klaim, keluhan, telat bayar, channel, ...) EN+ID; fitur asuransi (premium-to-income, claims per year, reject rate, tenure band, price shock, ...); **leakage screen** |
| 6–7 | EDA & **driver analysis** | churn rate + Wilson CI, chi-square/Mann-Whitney + **effect size**, **Information Value/WoE**, univariate AUC, FDR correction, insight otomatis |
| 8 | Korelasi | Spearman, Cramér's V, VIF |
| 9 | Segments | heatmap interaksi, **decision-tree segment rules** (IF–THEN + lift) |
| 10 | **Survival** | Kaplan-Meier, retention 6/12/24/36 bln, hazard per interval, log-rank, **Cox hazard ratios** (+ uji asumsi PH bila lifelines ada) |
| 11 | Interpretable model | Logistic regression **odds ratio + 95% CI + marginal effects**, forest plot |
| 12 | Drift | PSI, KS, unseen categories, adversarial validation |
| 13–17 | Modeling | LogReg, RF, ET, HGB, LightGBM, XGBoost, CatBoost (native categorical, in-fold target encoding), Optuna (pruning), multi-seed, feature selection, **ensemble** (mean, rank, hill-climbing, optimized weights, stacking) |
| 18 | Threshold & calibration | threshold optimal per metrik, reliability diagram, isotonic/Platt |
| 19 | Debugging | ROC/PR, confusion matrix, fold stability, **learning curve**, **shuffled-target test**, OOF vs test, error analysis, performa per segmen |
| 20 | Explainability | gain, permutation, **SHAP** (bar, beeswarm, dependence, kategori, waterfall), **PDP**, **driver evidence matrix** |
| 21 | **Business analytics** | lift/gains/KS, risk tiers, **CLV & value at risk**, **risk × value matrix**, **campaign ROI simulation + sensitivity**, **what-if scenarios**, **churn personas (SHAP clustering)** |
| 22 | Recommendations | rekomendasi otomatis berbasis bukti (aksi, evidence, impact, KPI) |
| 23–24 | Submission & export | validator, beberapa varian submission, action list customer, Excel semua tabel, `insights.md`, `figure_index.md`, `run_summary.json` |
| 25 | Troubleshooting | 20+ error → solusi, recipes, checklist |

Latihan: `python tools/make_synthetic_insurance_churn.py --out ./data` → jalankan notebook churn (set `CFG.EXTRA_TABLES` untuk `claims.csv`) → bandingkan driver yang ditemukan dengan driver yang ditanam (lihat docstring generator).

---

## Catatan environment
- Python 3.9–3.12. Library inti: numpy, pandas, scikit-learn, scipy, matplotlib, seaborn. Disarankan: lightgbm, xgboost, catboost, statsmodels, optuna, shap, lifelines (lihat `requirements.txt`).
- **Torch tidak di-install otomatis** (harus cocok dengan CUDA) → https://pytorch.org/get-started/locally/
- Kalau di laptop ada beberapa Python, pastikan `pip` menginstall ke Python yang dipakai kernel (`sys.executable` di environment check).
- Cell install hanya memasang package yang **belum ada** (tidak meng-upgrade yang sudah ada). Matikan dengan `CFG_AUTO_INSTALL = False` / `AUTO_INSTALL = False`.
