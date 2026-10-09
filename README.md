# Notebook Template — Data Analytics Competition

Kumpulan template notebook Python (`.ipynb`) siap pakai untuk lomba data analytics/data science, dengan fokus utama **customer churn & data asuransi**. Setiap notebook:

- **End-to-end**: load → cleaning → EDA → preprocessing → modeling (CV OOF) → tuning → ensemble → evaluasi & debugging → explainability → output/submission.
- **Tahan error**: library opsional dicek otomatis (auto-install yang belum ada), setiap model/section dibungkus supaya satu kegagalan tidak menghentikan notebook, kompatibel lintas versi library.
- **Penuh panduan** (Bahasa Indonesia, istilah teknis English): tujuan tiap langkah, cara membaca output, aturan **"Jika X → Y"**, catatan **"Untuk laporan"**, tabel troubleshooting, recipes, dan checklist.
- **Report-ready**: figure bernomor otomatis (DPI bisa 300), tabel CSV/Excel, dan kalimat insight (English) yang siap diparafrase.

> Jalankan di **Jupyter / VS Code lokal** (sesuai aturan lomba: Google Colab tidak diperbolehkan).

> **Pakai di komputer lain (mis. komputer panitia)?** Baca [`DOWNLOAD_DAN_INSTALASI.md`](DOWNLOAD_DAN_INSTALASI.md): download dari Zenodo/GitHub Release → `python -m pip install -r requirements-churn.txt` → `QA/ALUR_KERJA_HARI_H.md`.
>
> Dibuat oleh **Sains Data UB**. Lisensi MIT (lihat `LICENSE`); cara sitasi di `CITATION.cff`.

---

## Struktur repo

```
00_Setup/
  00_environment_check.ipynb        ← JALANKAN PERTAMA di laptop lomba (cek & install package, GPU)
01_Churn_Insurance/                 ← ⭐ UTAMA untuk case churn / asuransi
  00_MULAI_DI_SINI.md               ← RUNBOOK hari H: data masuk → laporan → ZIP (baca ini dulu)
  churn_insurance_master.ipynb      ← analisis + prediksi + rekomendasi bisnis + AUTO DRAFT LAPORAN, end-to-end
  contoh_output/                    ← contoh hasil run pada data sintetis (draft laporan, insights, figure)
  PLAYBOOK_ANALISIS.md              ← "jika X maka Y", cheat-sheet statistik, istilah asuransi, strategi retensi, Q&A juri
  PANDUAN_LAPORAN.md                ← struktur artikel 10 halaman, mapping figure → bab, template kalimat, referensi
  BAHAN_LATAR_BELAKANG.md           ← latar belakang + tinjauan pustaka + rumusan masalah (EN/ID), fakta OJK/AAJI terverifikasi, daftar pustaka
  CONTOH_LAPORAN_FINAL/             ← contoh artikel final lengkap (docx + pdf) dari data asuransi nyata (Kaggle)
  CASE_SCENARIOS.md                 ← semua kemungkinan bentuk case/data → setting & efek ke laporan
  RESEARCH_KIT.md                   ← metode riset latar belakang/"resume": casebook → keyword → sumber → verifikasi → workbook → laporan
  dashboard_template/               ← web app dashboard (diisi otomatis oleh notebook)
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
  new_case.py                       ← buat folder kerja case (data/, case_config.json, intake form, RUN_*.bat)
  CASE_INTAKE.html                  ← form offline: semua info dari soal → case_config.json
  run_case.py                       ← jalankan notebook headless dengan config (output tersimpan di notebook)
  make_zip.py                       ← ZIP pengumpulan sesuai aturan
  stress_test.py                    ← uji 44 bentuk data (22 skenario case + 22 data rusak/dimanipulasi) → STRESS_TEST_REPORT.md
  research_helper.py                ← casebook (pdf/docx/md) → keyword, fakta, link pencarian (RESEARCH_PLAN.html) + workbook riset
  CASE_RESEARCH_TEMPLATE.xlsx       ← workbook riset kosong (case_facts, industry_facts, literature, custom_paragraphs, feature_labels)
  case_config.example.json
  make_synthetic_insurance_churn.py ← generator data latihan asuransi (messy + driver yang diketahui)
examples/
  mock_case_warkab/                 ← contoh case lengkap (casebook fiktif, config, riset terisi) → make_mock_case.py
QA/
  QA_FINAL_REPORT.md                ← hasil QA/QC final (stress test, regresi, demo end-to-end)
  walkthrough_warkab/               ← REKAMAN proses demo: video MP4 + screenshot + STEPS.md
  make_walkthrough.py               ← membuat rekaman walkthrough dari folder case mana pun
requirements.txt
```

---

## Alur hari H (churn/asuransi) — ringkas
```
python tools/new_case.py ../case --casebook soal.pdf → folder kerja + form intake + RUN_*.bat + RESEARCH_PLAN.html + CASE_RESEARCH.xlsx
copy data panitia → case/data/ ; isi case/CASE_INTAKE.html → case_config.json
riset: klik link di RESEARCH_PLAN.html → isi CASE_RESEARCH.xlsx (otomatis masuk Introduction/Discussion/pustaka)
RUN_FAST.bat (cek 5–10 mnt) → RUN_FULL.bat (30–90 mnt)
→ case/outputs/churn_insurance/<Tim>_Final Stage 1.docx/.pdf  (artikel lengkap ≤10 hal + appendix A–L)
→ NARRATIVE_OPTIONS.md (pilih narasi) · JUDGE_QA.md (latihan Q&A) · dashboard/ (npx vercel --prod)
→ edit di Word → Save As PDF → python tools/make_zip.py --case ../case --pdf "<PDF final>"
```
Detail lengkap: `01_Churn_Insurance/00_MULAI_DI_SINI.md` · semua kemungkinan case: `01_Churn_Insurance/CASE_SCENARIOS.md`.

## Yang baru (upgrade final)
- **Headless runner** `tools/run_case.py` + `tools/new_case.py` + form offline `tools/CASE_INTAKE.html` (semua pertanyaan case → `case_config.json`).
- **Artikel ditulis otomatis & lengkap**: narasi berbasis data + literatur terverifikasi, judul berbasis temuan, figure komposit, cross-reference, daftar pustaka hanya yang disitasi, **autofit ≤ 10 halaman via MS Word/LibreOffice**, appendix A–L, PDF otomatis, `NARRATIVE_OPTIONS.md`, `JUDGE_QA.md`.
- **Metodologi tambahan**: EBM (glass-box) & MLP di model zoo, **experiment log + model development journey**, **ablation study (DeLong)**, **DeLong/Holm**, **EMPC (profit-based)**, ECE, RMST, Schoenfeld PH test, Weibull AFT, KM per risk tier + C-index, **AIPW robustness (placebo, E-value, overlap, DAG)**, **DR-learner uplift + GATES**, **fairness audit + model card**, **pilot A/B power analysis**, roadmap Gantt, 5 diagram arsitektur.
- **Robustness**: CatBoost OOF fix, label file terpisah, 1-file dengan target kosong = test, rekonstruksi tenure dari tanggal, figure tidak duplikat saat cell dijalankan ulang, console Windows UTF-8, fallback LibreOffice, template dashboard ter-embed.
- **Dashboard interaktif** (`outputs/.../dashboard/`, tanpa library eksternal) — offline & siap Vercel, dengan simulator kampanye.
- **Stress test** `tools/stress_test.py`: 44 bentuk data (22 skenario case + 22 data rusak: BOM, kolom ganda, "Rp 5 jt", tanggal campur, inf, label kotor, Excel multi-sheet berjudul, jsonl, leakage, target konstan, …) → `STRESS_TEST_REPORT.md`.
- **Research kit**: `research_helper.py` + `RESEARCH_KIT.md` + `CASE_RESEARCH.xlsx` → fakta casebook, fakta industri, literatur tim, paragraf custom & label fitur masuk otomatis ke artikel (dedupe referensi, peringatan sumber belum diverifikasi).
- **Skala portofolio & budget**: `PORTFOLIO_SIZE` → nilai uang dari sampel diskalakan ke portofolio; budget dibandingkan dengan kampanye skala portofolio (binding/tidak).
- **Contoh case + rekaman QA**: `examples/mock_case_warkab/` dan `QA/walkthrough_warkab/` (video proses end-to-end tim Warkab).
- **Dashboard (Vercel)** = hasil analisis case, dibuat ulang tiap run (konteks soal, pertanyaan, tim, KPI, driver, kampanye, rekomendasi); `DASHBOARD_INCLUDE_CUSTOMERS=false` untuk deploy publik tanpa data nasabah.

## Mulai cepat (template lain)

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
| 0–1 | Setup & Config | auto-install, availability flags, `CFG` + `USER OVERRIDE`, fast/full mode, **auto-adapt ke RAM/CPU/GPU & ukuran data** |
| 2 | Load data | csv/xlsx/parquet/json, auto separator/encoding, **multi-tabel** (merge 1-1, agregasi 1-many: claims/payments) |
| 3 | Data quality & cleaning | deteksi target/ID otomatis, parsing label churn (Yes/No, Exited, Attrited, is_active terbalik), angka-dalam-string (`"12,500,000"`, `"Rp 5.000.000"`), tanggal, typo kategori, nilai mustahil, duplikat, quality report |
| 4 | Target | churn rate, imbalance, baseline |
| 5 | Roles & domain FE | deteksi role (tenure, premi, klaim, keluhan, telat bayar, channel, ...) EN+ID; fitur asuransi (premium-to-income, claims per year, reject rate, tenure band, price shock, ...); **leakage screen** |
| 6–7 | EDA & **driver analysis** | churn rate + Wilson CI, chi-square/Mann-Whitney + **effect size**, **Information Value/WoE**, univariate AUC, FDR correction, insight otomatis, **analisis alasan churn** (kolom post-event, deskriptif) |
| 8 | Korelasi | Spearman, Cramér's V, VIF |
| 9 | Segments | heatmap interaksi, **decision-tree segment rules** (IF–THEN + lift) |
| 10 | **Survival** | Kaplan-Meier, retention 6/12/24/36 bln, hazard per interval, log-rank, **Cox hazard ratios** (+ uji asumsi PH bila lifelines ada) |
| 11 | Interpretable model | Logistic regression **odds ratio + 95% CI + marginal effects**, forest plot |
| 12 | Drift | PSI, KS, unseen categories, adversarial validation |
| 13–17 | Modeling | LogReg, RF, ET, HGB, LightGBM, XGBoost, CatBoost (native categorical, in-fold target encoding), Optuna (pruning), multi-seed, feature selection, **ensemble** (mean, rank, hill-climbing, optimized weights, stacking) |
| 18 | Threshold & calibration | threshold optimal per metrik, reliability diagram, isotonic/Platt |
| 19 | Debugging | ROC/PR, confusion matrix, **bootstrap 95% CI & paired model comparison**, fold stability, **learning curve**, **shuffled-target test**, OOF vs test, error analysis, performa per segmen |
| 20 | Explainability | gain, permutation, **SHAP** (bar, beeswarm, dependence, kategori, waterfall), **PDP**, **driver heterogeneity per segmen**, **driver evidence matrix** |
| 21 | **Business analytics** | lift/gains/KS, risk tiers, **CLV & value at risk**, **risk × value matrix**, **campaign ROI simulation + sensitivity**, **what-if scenarios**, **causal effects (doubly robust AIPW)**, **churn personas (SHAP clustering)** |
| 22 | Recommendations | rekomendasi otomatis berbasis bukti (aksi, evidence, impact, KPI) |
| 23 | Submission | validator, beberapa varian submission, action list customer (tier, value, quadrant) |
| 24 | **Deliverables** | Excel semua tabel, `insights.md`, executive summary figure, **5 diagram arsitektur**, **artikel lengkap `<Tim>_Final Stage 1.docx/.pdf` (autofit ≤10 hal, appendix A–L)**, `NARRATIVE_OPTIONS.md`, `JUDGE_QA.md`, **dashboard Vercel**, ZIP |
| 25 | Troubleshooting | 20+ error → solusi, recipes, checklist |

Latihan: `python tools/make_synthetic_insurance_churn.py --out ./data` → jalankan notebook churn (set `CFG.EXTRA_TABLES` untuk `claims.csv`) → bandingkan driver yang ditemukan dengan driver yang ditanam (lihat docstring generator).

---

## Catatan environment
- Python 3.9–3.12. Library inti: numpy, pandas, scikit-learn, scipy, matplotlib, seaborn. Disarankan: lightgbm, xgboost, catboost, statsmodels, optuna, shap, lifelines (lihat `requirements.txt`).
- **Torch tidak di-install otomatis** (harus cocok dengan CUDA) → https://pytorch.org/get-started/locally/
- Kalau di laptop ada beberapa Python, pastikan `pip` menginstall ke Python yang dipakai kernel (`sys.executable` di environment check).
- Cell install hanya memasang package yang **belum ada** (tidak meng-upgrade yang sudah ada). Matikan dengan `CFG_AUTO_INSTALL = False` / `AUTO_INSTALL = False`.
