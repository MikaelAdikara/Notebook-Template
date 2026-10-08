# Contoh v2 — artikel yang ditulis OTOMATIS oleh notebook (tanpa edit manusia)

Data: Kaggle auto-insurance churn (sampel 200.000 → train 160.000 / test 40.000), `RUN_MODE="full"`, config persis di `case_config_yang_dipakai.json`, dijalankan dengan `tools/run_case.py` (±40 menit).

| File | Isi |
|---|---|
| `AUTO_DataWizards_Final Stage 1.pdf/.docx` | artikel lengkap: cover, executive summary, 6 bab, referensi (hanya yang disitasi), appendix A–L; isi utama tepat 10 halaman (autofit) |
| `NARRATIVE_OPTIONS.md` | alternatif judul, framing, nama persona, paragraf diskusi |
| `JUDGE_QA.md` | persiapan pertanyaan juri dengan angka run ini |
| `REPORT_TODO.md` | checklist finalisasi |
| `dashboard/` | dashboard interaktif — buka `index.html` (offline) atau deploy `npx vercel --prod` |
| `model_card.md`, `insights.md`, `run_summary.json` | governance, semua kalimat insight, ringkasan run |

Bandingkan dengan `../DataWizards_Final Stage 1.pdf` (versi yang dulu diedit manual dari draft lama): judul otomatis versi baru ("The First Six Months Decide") sama dengan judul hasil edit manusia.

Catatan: data Kaggle ini tidak punya variabel yang bisa dikendalikan perusahaan (metode bayar, auto-renew, keluhan, dll.), jadi bagian kausal/uplift otomatis tidak muncul. Pada data yang punya variabel itu (lihat stress test & contoh sintetis), bagian 4.3 "What works?" terisi.
