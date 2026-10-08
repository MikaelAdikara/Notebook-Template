# ▶ MULAI DI SINI — Runbook Final (Churn / Insurance)

Satu prosedur dari **menerima soal → upload ZIP**, tanpa perlu AI. Semua langkah sudah otomatis; tugas tim adalah mengisi konteks soal, memeriksa, lalu memilih narasi terbaik.

Dokumen pendukung:
- `CASE_SCENARIOS.md` — **semua kemungkinan bentuk case/data** → setting config & bagian laporan yang berubah
- `PLAYBOOK_ANALISIS.md` — aturan "jika X → Y", statistik, istilah asuransi, strategi retensi, Q&A juri
- `PANDUAN_LAPORAN.md` — struktur artikel, apa yang dibuat otomatis, cara mengedit
- `BAHAN_LATAR_BELAKANG.md` — fakta industri Indonesia & literatur **terverifikasi** (sudah tertanam di generator laporan)
- `churn_insurance_master.ipynb` — notebook utama (Section 0–25)
- `../tools/` — `new_case.py`, `CASE_INTAKE.html`, `run_case.py`, `make_zip.py`, `stress_test.py`

---

## FASE 0 — Persiapan (sebelum soal dibuka)
- [ ] `00_Setup/00_environment_check.ipynb` dijalankan → semua inti ✅ (atau `python -m pip install -r requirements.txt`).
- [ ] MS Word terpasang (untuk hitung halaman & PDF). Tanpa Word → LibreOffice dipakai otomatis; tanpa keduanya → DOCX tetap jadi, PDF manual.
- [ ] (Opsional) `npx vercel login` sekali — untuk deploy dashboard.
- [ ] Bukti robust: `python tools/stress_test.py --out stress_runs` → `stress_runs/STRESS_TEST_REPORT.md` (18 bentuk data berbeda).

## FASE 1 — Siapkan folder case (2 menit)
```
python Notebook-Template/tools/new_case.py case --team NamaTim
```
→ folder `case/` berisi `data/`, `case_config.json`, `CASE_INTAKE.html`, `RUN_FAST.bat`, `RUN_FULL.bat`, `NEXT_STEPS.md`.
Copy file data panitia ke `case/data/`.

## FASE 2 — Isi Case Intake (5–10 menit)
Buka `case/CASE_INTAKE.html` di browser → isi dari soal → **Download JSON** → timpa `case/case_config.json`.

| Bagian | Yang dicari di soal | Kalau tidak ada di soal |
|---|---|---|
| File & kolom | nama file, kolom target & nilai churn, ID, tabel tambahan | kosongkan → auto-detect |
| Kompetisi | metrik penilaian, format submission | `roc_auc` + probability |
| **Case brief** | konteks perusahaan (2–4 kalimat EN), definisi churn, periode data, pertanyaan yang diminta, intervensi yang mungkin | auto: RQ standar, deteksi jenis asuransi dari data |
| Bisnis | margin, biaya retensi, success rate, budget | default wajar → otomatis ditulis sebagai **asumsi + sensitivity analysis** |

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

## (Opsional) Dashboard online
```
cd case/outputs/churn_insurance/dashboard
npx vercel --prod
```
Atau drag-and-drop folder `dashboard/` ke vercel.com/new. Offline: buka `index.html`. Link bisa dicantumkan di artikel (Appendix K) / presentasi.

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

## Prinsip nilai tinggi (sudah tertanam di generator)
1. Jawab pertanyaan bisnis (RQ1–RQ4), bukan pamer model.
2. Setiap klaim ada angka + ketidakpastian (CI, effect size), dan konsisten antar metode.
3. Rekomendasi spesifik, bernilai uang, dengan desain pilot A/B & KPI.
4. Metodologi rapi: leakage dicegah, OOF CV, DeLong, ablation, uji sanity, kausal dengan uji robustness.
5. Jujur soal batasan; governance (fairness, model card).
