# Alur kerja Hari-H: dari soal diterima sampai paper & ZIP terkumpul (Tim Warkab)

> Tidak perlu AI. Semua perintah dijalankan dari folder yang berisi `Notebook-Template/`.
> Bukti setiap langkah benar-benar berjalan: video `walkthrough_warkab/walkthrough_Warkab.mp4`, screenshot di `walkthrough_warkab/screens/`, dan `QA_FINAL_REPORT.md`.

```
 SOAL (casebook + data)
   │
   ├─(1) new_case.py ───────────► folder case: data/, case_config.json, CASE_INTAKE.html,
   │                              RESEARCH_PLAN.html, CASE_RESEARCH.xlsx, RUN_FAST.bat, RUN_FULL.bat
   ├─(2) CASE_INTAKE.html ──────► case_config.json (target, metrik, konteks, pertanyaan, budget, portofolio)
   ├─(3) RESEARCH_PLAN.html ────► cari sumber (link siap klik) ─► isi CASE_RESEARCH.xlsx     [orang ke-2, paralel]
   ├─(4) RUN_FAST.bat ──────────► cek target/ID/leakage/narasi (±10 menit)
   ├─(5) RUN_FULL.bat ──────────► notebook ter-eksekusi + artikel DOCX/PDF ≤10 hal + appendix + dashboard + submission
   ├─(6) rerun cell 24.2c–24.5 ─► artikel ter-update dengan riset tim (tanpa modeling ulang, ±3 menit)
   ├─(7) Word: edit & Save As PDF
   ├─(8) make_zip.py ───────────► <Tim>_Final Stage 1.zip
   └─(9) qa_check.py ───────────► QA_CHECK.md: semua cek wajib PASS → upload
```

## Pembagian kerja 2 orang

| Waktu | Mikael | Pandu |
|---|---|---|
| T+0–10 mnt | Langkah 1–2: folder case, copy data, isi intake | Baca casebook 3 lapis (RESEARCH_KIT §2), tandai angka & fakta |
| T+10–20 | Langkah 4: RUN_FAST → cek `run_summary.json`, `REPORT_TODO.md` | Buka RESEARCH_PLAN.html, mulai cari sumber |
| T+20–90 | Langkah 5: RUN_FULL (background) → baca draft fast run, pilih narasi di NARRATIVE_OPTIONS.md | Isi CASE_RESEARCH.xlsx (case_facts, industry_facts, literature, custom_paragraphs), verifikasi DOI/URL |
| T+90–100 | Langkah 6: rerun cell 24.2c–24.5 | Cek kutipan & daftar pustaka |
| T+100–160 | Langkah 7: edit di Word (bagian depan) | Edit di Word (diskusi, rekomendasi), latihan JUDGE_QA.md |
| T+160–170 | Langkah 8–9: ZIP + qa_check → upload | Cek nama file & isi ZIP |

## Langkah detail

### 1. Buat folder case (2 menit)
```
python Notebook-Template/tools/new_case.py case --casebook "soal.pdf"
```
Copy semua file data panitia ke `case/data/`. Format apa pun: csv/tsv/txt, xlsx (banyak sheet, judul di atas header), json/jsonl, parquet.
Data rusak/dimanipulasi tetap jalan: BOM, kolom ganda, "Rp 5 jt", tanggal campur, inf, label kotor, baris rusak, kolom bocor
(lihat `01_Churn_Insurance/CASE_SCENARIOS.md` bagian X dan `tools/STRESS_TEST_REPORT.md`).

### 2. Case Intake (5–10 menit)
Buka `case/CASE_INTAKE.html` (offline) → isi dari soal → **Download JSON** → timpa `case/case_config.json`.

| Isi dari soal | Key |
|---|---|
| Nama kolom target & nilai churn, ID, file tambahan | `TARGET_COL`, `POSITIVE_LABEL`, `ID_COL`, `EXTRA_TABLES`, `TRAIN_LABELS` |
| Metrik & format submission | `METRIC`, `SUBMISSION_MODE` |
| Nama perusahaan, konteks (EN), definisi churn, periode | `COMPANY_NAME`, `CASE_CONTEXT`, `CHURN_DEFINITION`, `DATA_PERIOD` |
| Pertanyaan yang diminta soal → Research Questions | `CASE_QUESTIONS` |
| Intervensi yang mungkin | `AVAILABLE_INTERVENTIONS` |
| Margin, biaya, success rate, budget, jumlah nasabah | `PROFIT_MARGIN`, `RETENTION_COST`, `RETENTION_SUCCESS_RATE`, `RETENTION_BUDGET`, `PORTFOLIO_SIZE`, `BUSINESS_PARAMS_SOURCE=case` |
| Fakta angka di casebook | `CASE_KEY_FACTS` (atau sheet `case_facts`) |

### 3. Riset latar belakang ("resume") — paralel
1. `case/RESEARCH_PLAN.html`: istilah kunci & kalimat berangka dari casebook + link pencarian per tema (Google Scholar, Crossref, Semantic Scholar, Garuda, Google Books, OJK/AAJI/AAUI).
2. Metode lengkap: `01_Churn_Insurance/RESEARCH_KIT.md` (baca casebook 3 lapis, keyword EN/ID + Boolean, hierarki sumber, verifikasi, matriks sintesis, pola kalimat, APA 7).
3. Isi `case/CASE_RESEARCH.xlsx`, `use = Y`, `verified = Y` setelah sumber dibuka.
4. Setelah fast run: `python Notebook-Template/tools/research_helper.py --case case` → query literatur per driver hasil model.
Contoh workbook terisi: `examples/mock_case_warkab/CASE_RESEARCH.xlsx`.

### 4. RUN_FAST.bat (±10 menit)
Cek `outputs/churn_insurance/run_summary.json`: `target_mapping` (churn = 1), `churn_rate`, `section_errors` kosong, `leaky_cols`.
Kalau berhenti dengan pesan (target 1 kelas, data < 30 baris, target kontinu): pesan menyebut key yang harus diubah.

### 5. RUN_FULL.bat (30–90 menit, background)
Hasil di `case/outputs/churn_insurance/`:
- `<Tim>_Final Stage 1.docx/.pdf`: cover, executive summary, 6 bab, referensi ≤ 10 halaman (autofit via Word), appendix A–L tidak dibatasi;
- `NARRATIVE_OPTIONS.md` (judul/framing alternatif), `JUDGE_QA.md` (latihan pertanyaan juri), `REPORT_TODO.md` (checklist);
- `dashboard/` (web app hasil analisis, siap Vercel), `submission.csv`, Excel semua tabel, figures, model card;
- `<Tim>_churn_analysis.ipynb` ter-eksekusi (bukti analisis untuk ZIP).

### 6. Masukkan riset tim tanpa modeling ulang
Buka notebook ter-eksekusi → jalankan cell **24.2c sampai 24.5** (±3 menit). Fakta casebook dan fakta industri masuk ke Introduction. Literatur masuk ke Discussion & Appendix B, paragraf custom masuk ke section yang dipilih, dan daftar pustaka ter-update.

### 7. Finalisasi di Word
Parafrase gaya tim, pilih narasi, hapus penanda [EDIT], cek angka = tabel. Jangan ubah format. Save As PDF `<Tim>_Final Stage 1.pdf`.

### 8. ZIP
```
python Notebook-Template/tools/make_zip.py --case case --pdf "case/<Tim>_Final Stage 1.pdf"
```

### 9. Cek akhir otomatis
```
python Notebook-Template/QA/qa_check.py --case case
```
Harus "semua cek wajib PASS". Cek mencakup:
- ≤10 halaman isi;
- nama tim & anggota di cover;
- nama perusahaan & konteks soal;
- tiap pertanyaan soal;
- skala portofolio & budget;
- tiap baris riset `use = Y` benar-benar ada di artikel;
- tidak ada caption mentah / [EDIT] / "nan";
- dashboard, submission, ZIP.

### (Opsional) Dashboard online
Yang di-deploy adalah **hasil analisis** case itu sendiri (dibuat ulang setiap run, isinya mengikuti data + case brief).
```
cd case/outputs/churn_insurance/dashboard
npx vercel --prod
```
Data nasabah rahasia → `"DASHBOARD_INCLUDE_CUSTOMERS": false` lalu jalankan ulang cell dashboard sebelum deploy.

## Latihan sebelum hari-H (sekali, ±40 menit)
```
python Notebook-Template/examples/mock_case_warkab/make_mock_case.py latihan
```
Lalu double-click `latihan/RUN_FULL.bat` → `python Notebook-Template/tools/make_zip.py --case latihan` → `python Notebook-Template/QA/qa_check.py --case latihan`.
Rekam ulang walkthrough (opsional): `python Notebook-Template/QA/make_walkthrough.py --case latihan --out rekaman --stress Notebook-Template/tools/STRESS_TEST_REPORT.md`.
