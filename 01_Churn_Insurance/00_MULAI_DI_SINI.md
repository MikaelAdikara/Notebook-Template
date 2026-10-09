# ▶ MULAI DI SINI — Runbook Final (Churn / Insurance)

Satu prosedur dari **menerima soal → upload ZIP**, tanpa perlu AI. Semua langkah sudah otomatis; tugas tim adalah mengisi konteks soal, memeriksa, lalu memilih narasi terbaik.

Dokumen pendukung:
- `CASE_SCENARIOS.md` — **semua kemungkinan bentuk case/data** → setting config & bagian laporan yang berubah
- `PLAYBOOK_ANALISIS.md` — aturan "jika X → Y", statistik, istilah asuransi, strategi retensi, Q&A juri
- `PANDUAN_LAPORAN.md` — struktur artikel, apa yang dibuat otomatis, cara mengedit
- `BAHAN_LATAR_BELAKANG.md` — fakta industri Indonesia & literatur **terverifikasi** (sudah tertanam di generator laporan)
- `RESEARCH_KIT.md` — **metode menyusun latar belakang/"resume" yang nempel ke case**: baca casebook 3 lapis, keyword EN/ID, hierarki sumber, cara verifikasi, matriks sintesis, pola kalimat, APA 7
- `../examples/mock_case_warkab/` — **contoh case lengkap end-to-end** (casebook fiktif + data + config + riset terisi) untuk latihan/demo
- `../QA/` — bukti QA final: laporan QA, rekaman walkthrough (video + screenshot), hasil stress test
- `churn_insurance_master.ipynb` — notebook utama (Section 0–25)
- `../tools/` — `new_case.py`, `CASE_INTAKE.html`, `run_case.py`, `make_zip.py`, `stress_test.py`

---

## FASE 0 — Persiapan (sebelum soal dibuka)
- [ ] `00_Setup/00_environment_check.ipynb` dijalankan → semua inti ✅ (atau `python -m pip install -r requirements.txt`).
- [ ] MS Word terpasang (untuk hitung halaman & PDF). Tanpa Word → LibreOffice dipakai otomatis; tanpa keduanya → DOCX tetap jadi, PDF manual.
- [ ] (Opsional) `npx vercel login` sekali — untuk deploy dashboard.
- [ ] Bukti robust: `python tools/stress_test.py --out stress_runs` → `stress_runs/STRESS_TEST_REPORT.md` (44 bentuk data: 22 skenario case + 22 data rusak/dimanipulasi).
- [ ] Latihan sekali: `python examples/mock_case_warkab/make_mock_case.py latihan` → jalankan `latihan/RUN_FAST.bat` → lihat semua output (±10 menit).

## FASE 1 — Siapkan folder case (2 menit)
```
python Notebook-Template/tools/new_case.py case --casebook "path/ke/casebook.pdf"
```
(Default tim = **Warkab**, anggota Mikael Alexander Adikara Purnama & Pandu Winata — ganti dengan `--team`/`--members` kalau perlu.)
→ folder `case/` berisi `data/`, `case_config.json`, `CASE_INTAKE.html`, `RUN_FAST.bat`, `RUN_FULL.bat`, `NEXT_STEPS.md`,
**`RESEARCH_PLAN.html`** (keyword + link pencarian siap klik + fakta yang terdeteksi dari casebook) dan **`CASE_RESEARCH.xlsx`** (workbook riset tim).
Copy file data panitia ke `case/data/` (format apa pun: csv/tsv/txt/xlsx multi-sheet/json/jsonl/parquet; data kotor tetap jalan — lihat tabel "Data rusak" di bawah).

## FASE 1b — Riset latar belakang (30–60 menit, dikerjakan sambil RUN_FULL berjalan)
Tujuan: Introduction & Discussion **nempel ke case**, bukan paragraf generik.
1. Buka `case/RESEARCH_PLAN.html` → baca blok "Fakta dari casebook" (kandidat kalimat untuk Introduction) dan klik link pencarian per tema (Google Scholar, Crossref, Semantic Scholar, Garuda, Google Books, OJK/AAJI).
2. Ikuti `RESEARCH_KIT.md`: pilih sumber (jurnal/buku/regulator > laporan industri > berita), **verifikasi DOI/URL**, catat 1 kalimat temuan.
3. Isi `case/CASE_RESEARCH.xlsx`:
   - `case_facts` → fakta casebook dalam English (angka persis seperti soal);
   - `industry_facts` → fakta pasar (OJK/AAJI/AAUI) + referensi APA;
   - `literature` → temuan jurnal per tema (lapse driver, payment, price, service, ML method) + referensi APA;
   - `custom_paragraphs` → paragraf tim di awal/akhir section tertentu (executive summary, introduction, discussion, recommendations, conclusion…);
   - `feature_labels` → nama fitur yang enak dibaca di laporan.
   Kolom `use` = **Y** agar dipakai, `verified` = **Y** setelah dicek (yang belum diverifikasi diberi peringatan di REPORT_TODO).
4. Setelah fast run: `python tools/research_helper.py --case case` → RESEARCH_PLAN diperbarui dengan keyword **per driver hasil model**.
5. Setelah workbook diisi: jalankan ulang cell **24.2c–24.5** (tanpa modeling ulang) atau RUN_FAST/RUN_FULL → riset otomatis masuk ke Introduction, Discussion, Appendix B & daftar pustaka (duplikat otomatis dibuang).

## FASE 2 — Isi Case Intake (5–10 menit)
Buka `case/CASE_INTAKE.html` di browser → isi dari soal → **Download JSON** → timpa `case/case_config.json`.

| Bagian | Yang dicari di soal | Kalau tidak ada di soal |
|---|---|---|
| File & kolom | nama file, kolom target & nilai churn, ID, tabel tambahan | kosongkan → auto-detect |
| Kompetisi | metrik penilaian, format submission | `roc_auc` + probability |
| **Case brief** | konteks perusahaan (2–4 kalimat EN), definisi churn, periode data, pertanyaan yang diminta, intervensi yang mungkin | auto: RQ standar, deteksi jenis asuransi dari data |
| Bisnis | margin, biaya retensi, success rate, budget, **jumlah nasabah/polis perusahaan (PORTFOLIO_SIZE)** | default wajar → otomatis ditulis sebagai **asumsi + sensitivity analysis** |
| Riset | fakta kunci casebook (`CASE_KEY_FACTS`), `USE_DEFAULT_MARKET_CONTEXT` | workbook CASE_RESEARCH.xlsx dipakai otomatis |

> `BUSINESS_PARAMS_SOURCE = case` kalau angka bisnis diberikan soal → laporan menulis "given in the case" (bukan "assumed").
> `PORTFOLIO_SIZE` → angka uang dari sampel data diskalakan ke seluruh portofolio, dan budget dibandingkan dengan biaya kampanye skala portofolio (bukan skala sampel).

> Case brief **mengubah narasi laporan** (Introduction, Research Questions, prioritas rekomendasi). Isi selengkap mungkin.

## FASE 3 — Fast check (5–10 menit)
Double-click `RUN_FAST.bat` (atau `python tools/run_case.py --config case/case_config.json --set RUN_MODE=fast`). Cek:

| File | Yang dicek | Kalau salah |
|---|---|---|
| `outputs/churn_insurance/run_summary.json` | `target`, `target_mapping` (churn = 1), `churn_rate`, `section_errors` kosong | `TARGET_COL`, `POSITIVE_LABEL` |
| `<Tim>_churn_analysis.ipynb` → Section 3.1–3.3, 5.1, 5.3 | ID, tipe kolom, role (tenure/premium), leakage | `ID_COL`, `FORCE_*`, `COLUMN_ROLES`, `DROP_COLS` |
| `REPORT_TODO.md` | jenis asuransi terdeteksi, penanda [EDIT] | `INSURANCE_LINE`, case brief |

## FASE 4 — Full run (30–90 menit, background)
Double-click `RUN_FULL.bat`. Waktu mepet: tambahkan di config `"USE_OPTUNA": false` atau `"OPTUNA_TIMEOUT": 300`.
**Sambil menunggu:** baca draft dari fast run (struktur sama, angka akan ter-update) dan siapkan narasi.

## FASE 5 — Finalisasi artikel (45–90 menit)
Di `case/outputs/churn_insurance/`:
1. **`<Tim>_Final Stage 1.docx`** — artikel lengkap (cover, executive summary, 6 bab, referensi, appendix A–L), format soal, **≤ 10 halaman isi (autofit)**.
2. `REPORT_TODO.md` — checklist.
3. `NARRATIVE_OPTIONS.md` — alternatif judul, framing executive summary, **nama persona**, paragraf diskusi per driver (dengan sitasi terverifikasi), peta "soal menanyakan X → bagian Y".
4. Edit di Word: parafrase gaya tim, tambahkan insight spesifik case, pilih narasi. Jangan ubah format.
5. Save As PDF: `<Tim>_Final Stage 1.pdf`.
6. `JUDGE_QA.md` — latihan jawab pertanyaan juri (angka sudah terisi).

Ubah narasi tanpa modeling ulang: edit case brief di notebook (cell USER OVERRIDE) → jalankan ulang cell **24.2c–24.5** saja.

## FASE 6 — Kumpulkan (5 menit)
```
python Notebook-Template/tools/make_zip.py --case case --pdf "case/<Tim>_Final Stage 1.pdf"
```
→ `case/<Tim>_Final Stage 1.zip` berisi PDF + notebook ter-eksekusi + `supporting/` (figures, tables, Excel, dashboard, submission, model card).
- [ ] `submission.csv` lolos validator (Section 23) & sesuai format soal.
- [ ] Nama file PDF/ZIP persis `<Tim>_Final Stage 1`.
- [ ] Cek akhir otomatis: `python Notebook-Template/QA/qa_check.py --case case` → semua cek wajib **PASS** (≤10 halaman, tim/anggota di cover, konteks & riset soal masuk artikel, tidak ada caption mentah/[EDIT], dashboard & ZIP lengkap).

## (Opsional) Dashboard online — apa yang di-deploy?
Yang di-deploy ke Vercel adalah **HASIL analisis** (`case/outputs/churn_insurance/dashboard/`), bukan alat bantu.
Dashboard ini **dibuat ulang setiap run** dari data & case brief case tersebut: nama perusahaan, konteks & pertanyaan soal, tim & anggota,
KPI (churn rate, AUC, value at risk), driver, kurva risiko per tenure, kampanye optimal & budget, rekomendasi, dan (opsional) daftar nasabah prioritas.
Ganti case → run ulang → isi dashboard ikut berubah.
```
cd case/outputs/churn_insurance/dashboard
npx vercel --prod
```
Login Vercel dilakukan sendiri (sekali, `npx vercel login`). Atau drag-and-drop folder `dashboard/` ke vercel.com/new. Offline: buka `index.html`.
**Data rahasia?** set `"DASHBOARD_INCLUDE_CUSTOMERS": false` lalu run ulang cell dashboard sebelum deploy publik.
Alat bantu (`CASE_INTAKE.html`, `RESEARCH_PLAN.html`) cukup dibuka lokal di browser — tidak perlu di-deploy.

---

## Kalau ada masalah
| Situasi | Langkah |
|---|---|
| Section error | lihat `run_summary.json` → `section_errors`; Section 25 (Troubleshooting) di notebook; section lain tetap jalan |
| Target/ID salah | set `TARGET_COL` / `POSITIVE_LABEL` / `ID_COL` di case_config.json → run ulang |
| Data tidak cocok dengan pola umum | `CASE_SCENARIOS.md` |
| Isi utama > 10 halaman | autofit sudah memadatkan; sisanya pindahkan 1 figure/tabel ke Appendix di Word |
| Waktu hampir habis | pakai hasil fast run — laporannya sudah lengkap (3-fold CV) |
| Hasil berbeda dari intuisi | PLAYBOOK §C — justru jadikan insight |
| Notebook berhenti "Target hanya punya 1 kelas" | kolom target salah / label ada di file terpisah → set `TARGET_COL`, `TRAIN_LABELS`, atau `POSITIVE_LABEL` |
| Data < 30 baris | berhenti dengan pesan jelas — cek file yang di-copy benar |
| Excel banyak sheet / judul di atas header | otomatis (sheet terbesar, header dideteksi); kalau salah set `EXCEL_SHEET` |

### Data rusak / dimanipulasi — semuanya sudah diuji (`tools/STRESS_TEST_REPORT.md`)
| Kerusakan | Yang dilakukan template otomatis |
|---|---|
| BOM, spasi/enter di nama kolom, nama kolom ganda, kolom index tersimpan (`Unnamed: 0`) | dibersihkan; kolom ganda diberi akhiran (`age.1`), index dibuang |
| Baris/kolom kosong, kolom konstan | dibuang + dicatat |
| Angka sebagai teks: `"1,250,000"`, `"Rp 5 jt"`, `"1,2 M"`, `"750 rb"`, `"12%"` | diparse ke angka (jt/juta, rb/ribu, M/miliar, T/triliun) |
| Tanggal campur format (`2024-01-05`, `05/01/2024`, `Jan 5 2024`) | diparse (dayfirst + mixed) |
| `inf`, angka negatif aneh, outlier ekstrem | inf → NaN dan dicatat; model tree tahan outlier |
| Label target kotor (`yes`, `Y `, `1.0`, `TRUE`, `Lapsed/Active/Surrendered`) | dinormalisasi; multi-status → aktif = 0, lainnya = 1 |
| Kolom test ≠ train (kurang/lebih/urutan beda) | diselaraskan; kolom hilang = NaN |
| Kategori baru di test, ID kardinalitas tinggi, teks bebas/PII | ditangani encoder; ID/PII dibuang |
| Duplikat (termasuk duplikat dengan label bertentangan) | dideteksi & dilaporkan |
| Kolom bocor (cancel_date, reason, dsb.) | leakage scan → dibuang otomatis |
| csv rusak (baris kelebihan kolom, encoding cp1252/latin-1, separator `;`/tab/`\|`) | separator & encoding dideteksi, baris rusak dilewati |
| Target konstan / file terlalu kecil | **berhenti dengan pesan jelas** (bukan error misterius) |

## Prinsip nilai tinggi (sudah tertanam di generator)
1. Jawab pertanyaan bisnis (RQ1–RQ4), bukan pamer model.
2. Setiap klaim ada angka + ketidakpastian (CI, effect size), dan konsisten antar metode.
3. Rekomendasi spesifik, bernilai uang, dengan desain pilot A/B & KPI.
4. Metodologi rapi: leakage dicegah, OOF CV, DeLong, ablation, uji sanity, kausal dengan uji robustness.
5. Jujur soal batasan; governance (fairness, model card).
