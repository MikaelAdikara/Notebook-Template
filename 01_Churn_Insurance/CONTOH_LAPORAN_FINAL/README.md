# Contoh Laporan Final — dari data asuransi NYATA (Kaggle)

**File utama:** `DataWizards_Final Stage 1.pdf` / `.docx` — artikel lengkap, **10 halaman isi** (+ cover + appendix), format sesuai soal (A4, Times New Roman 12, spasi 1.15, margin 4/4/3/3 cm).

## Asal data & cara dibuat
- Data: *Auto Insurance Churn Analysis Dataset* (Kaggle, `merishnasuwal/auto-insurance-churn-analysis-dataset`), asuransi kendaraan di Texas, 1,68 juta customer. Disimulasikan seperti soal lomba: sampel 200.000 → `train.csv` 160.000 + `test.csv` 40.000 + `sample_submission.csv`.
- Diproses dengan `churn_insurance_master.ipynb` (`RUN_MODE="full"`), konfigurasi persis di `hasil_run_notebook/USER_OVERRIDE_yang_dipakai.py` — hanya path, nama tim, mata uang & asumsi bisnis. **Target, ID, tipe kolom, leakage, role kolom semuanya terdeteksi otomatis.**
- Total waktu run di laptop (12 core, RAM 16 GB): ±28 menit.
- `hasil_run_notebook/` berisi output mentah notebook: `REPORT_DRAFT.docx/.pdf` (draft otomatis), `REPORT_TODO.md`, `insights.md`, `report_tables.xlsx`, `run_summary.json`.

**Bandingkan `hasil_run_notebook/REPORT_DRAFT.docx` (otomatis) dengan `DataWizards_Final Stage 1.docx` (final).** Itulah pekerjaan yang harus kalian lakukan saat lomba: draft otomatis → artikel final dengan narasi, interpretasi, dan rekomendasi yang tajam.

## Hal-hal yang ditangkap otomatis oleh notebook di data ini (dan akan muncul juga di data lomba)
| Masalah di data | Ditangani otomatis |
|---|---|
| `acct_suspd_date` hanya terisi untuk customer yang churn (**leakage**) | terdeteksi (pola missing = target) → dibuang beserta fitur turunannya; fitur "jumlah missing per baris" dihitung ulang tanpa kolom leak |
| `home_market_value` berupa teks rentang "50000 - 74999" | dikonversi ke nilai tengah numerik |
| `individual_id`, `address_id` angka ID | dikeluarkan dari fitur |
| `state` konstan (semua TX) | dibuang |
| `cust_orig_date`, `date_of_birth` | di-parse; tanggal lahir tidak dibuat fitur ganda karena sudah ada `age` |
| `days_tenure` dalam hari | role tenure + satuan hari terdeteksi; hazard dilaporkan per 30 hari |
| `curr_ann_amt` | terdeteksi sebagai premi tahunan → value at risk & CLV |
| 160 ribu baris | mode data besar: RF/ET dimatikan, Optuna di subsample 100k, Cox di subsample 50k |
| ID test float (`2213…0.0`) vs sample_submission integer | disamakan otomatis, validator ✅ |

## Kenapa artikel ini kuat (pakai sebagai checklist kualitas)
1. **Judul = temuan utama** ("The First Six Months Decide") — bukan "Analisis Churn Asuransi".
2. **Executive summary berisi angka kunci, jawaban, dan rekomendasi** — juri bisa paham isi dalam 1 menit.
3. **Research questions (RQ1–RQ4) dijawab satu per satu** di Findings & Conclusion — struktur mudah dinilai.
4. **Metodologi berlapis tapi ringkas** + diagram alur (Figure 1) + validasi (OOF CV, bootstrap CI, shuffled-label test, adversarial validation) + **pencegahan leakage dijelaskan**.
5. **Setiap klaim ada angka & ukuran ketidakpastian** (CI, odds ratio, hazard ratio, IV, effect size). Dibedakan "signifikan" vs "penting" (IV < 0.02 disebut negligible walau p kecil).
6. **Konsistensi bukti antar metode** (statistik univariat → logistic regression → survival → SHAP) → driver yang robust.
7. **Insight "kapan"** (hazard puncak hari 90–180) → langsung menjadi aksi (onboarding sebelum hari 90).
8. **Bisnis: value at risk, risk×value, campaign ROI + sensitivity analysis** — rekomendasi dinilai dengan uang, dan robust terhadap asumsi.
9. **Tabel rekomendasi**: aksi spesifik, evidence, target segmen, KPI + urutan implementasi.
10. **Jujur soal keterbatasan** (data snapshot, tidak ada data harga/klaim/layanan, asosiasi ≠ kausal) + saran pilot A/B (Ascarza, 2018).
11. **Literatur dipakai secukupnya untuk memperkuat argumen**, semua referensi terverifikasi (DOI).

## Cara mengadaptasi ke case lomba
1. Jalankan notebook pada data lomba → buka `REPORT_TODO.md` & `REPORT_DRAFT.docx`.
2. Pakai **struktur & gaya** artikel contoh ini, tapi **ganti isi dengan temuan data kalian** (jangan copy kalimatnya — temuan tiap data berbeda!).
3. Latar belakang Indonesia (OJK/AAJI) & tinjauan pustaka: `../BAHAN_LATAR_BELAKANG.md`.
4. Kalau data lomba punya variabel actionable (metode bayar, auto-renew, keluhan, klaim, kenaikan premi), notebook juga menghasilkan **efek kausal (AIPW)** dan **what-if** — masukkan ke Section 4 (contoh tampilannya ada di `../contoh_output/` dari data sintetis).
5. Cek 10 halaman (notebook menghitung otomatis kalau ada MS Word), Save As PDF dengan nama `NamaTim_Final Stage 1.pdf`.

> Catatan: angka di artikel ini adalah hasil run nyata notebook pada data Kaggle tersebut. Artikel ini **contoh**; jangan dikumpulkan sebagai jawaban lomba.
