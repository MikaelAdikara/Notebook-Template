# Next steps — Warkab

1. Copy semua file data dari panitia ke `data/`.
2. Buka `CASE_INTAKE.html` → isi dari soal → **Download JSON** → simpan sebagai `case_config.json` di folder ini (timpa).
   (Atau edit `case_config.json` langsung.)
3. Simpan PDF/DOCX soal sebagai `casebook.pdf` di folder ini → `python "C:\Users\mikae\OneDrive\Documents\Lomba\DAC ITS\Final\Notebook-Template\tools\research_helper.py" --case .`
   → buka **RESEARCH_PLAN.html** (keyword + query siap-klik) & isi **CASE_RESEARCH.xlsx** (panduan: RESEARCH_KIT.md).
4. Double-click **RUN_FAST.bat** (±5–10 menit) → cek `outputs/churn_insurance/run_summary.json` & `REPORT_TODO.md`:
   target/ID benar? churn rate masuk akal? tidak ada section error?
5. Double-click **RUN_FULL.bat** (±30–90 menit; jalan di background).
6. Hasil di `outputs/churn_insurance/`:
   - `Warkab_Final Stage 1.docx/.pdf` — artikel (≤10 halaman isi, appendix lengkap)
   - `NARRATIVE_OPTIONS.md` — alternatif judul/framing/nama persona/paragraf diskusi
   - `JUDGE_QA.md` — persiapan pertanyaan juri
   - `dashboard/` — buka `index.html`; deploy: `cd outputs/churn_insurance/dashboard` lalu `npx vercel --prod`
   - `submission.csv`, `tables/`, `figures/`, `report_tables.xlsx`, `model_card.md`
   - `Warkab_churn_analysis.ipynb` (di folder ini) — notebook ter-eksekusi lengkap dengan output (bukti analisis)
7. Setelah CASE_RESEARCH.xlsx terisi: jalankan ulang cell 24.2c–24.5 di notebook (±3 menit) → artikel memuat riset tim.
8. Edit artikel di Word (parafrase, pilih narasi) → Save As PDF `Warkab_Final Stage 1.pdf`.
9. ZIP pengumpulan: `python "C:\Users\mikae\OneDrive\Documents\Lomba\DAC ITS\Final\Notebook-Template\tools\make_zip.py" --case . --pdf "Warkab_Final Stage 1.pdf"`
   (PDF final hasil edit kamu; tanpa --pdf → pakai draft otomatis).
10. Cek akhir otomatis: `python "C:\Users\mikae\OneDrive\Documents\Lomba\DAC ITS\Final\Notebook-Template\QA\qa_check.py" --case .` → semua cek wajib PASS (hasil di `QA_CHECK.md`).

Panduan lengkap: C:\Users\mikae\OneDrive\Documents\Lomba\DAC ITS\Final\Notebook-Template\01_Churn_Insurance\00_MULAI_DI_SINI.md
