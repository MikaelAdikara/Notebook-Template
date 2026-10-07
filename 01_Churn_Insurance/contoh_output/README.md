# Contoh output (data sintetis)

Hasil menjalankan `churn_insurance_master.ipynb` pada data latihan dari `tools/make_synthetic_insurance_churn.py`
(`RUN_MODE="fast"`, 3-fold CV, `TEAM_NAME="DataWizards"`, `COMPANY_NAME="PT Asuransi Sejahtera"`).
Tujuannya hanya untuk menunjukkan **seperti apa deliverable yang dihasilkan otomatis** — angka di sini bukan hasil lomba.

| File | Isi |
|---|---|
| `REPORT_DRAFT.docx` | draft artikel (format soal) dengan angka, figure, tabel; bagian kuning `[EDIT]` wajib diedit |
| `REPORT_DRAFT.md` | versi markdown draft yang sama |
| `REPORT_TODO.md` | daftar kerja: semua `[EDIT]`, checklist verifikasi, format, dan peta sumber data |
| `insights.md` | semua kalimat insight otomatis per section |
| `figures/`, `figure_index.md` | semua figure bernomor |
| `report_tables.xlsx` | semua tabel analisis dalam 1 file Excel |

Driver yang ditanam di data sintetis (untuk mengecek analisis): metode bayar non-auto-debit, tidak auto-renew, kenaikan premi,
keluhan, klaim ditolak, telat bayar, tenure pendek, bayar bulanan, channel online, sedikit produk, engagement rendah, umur U-shape.
Bandingkan dengan `insights.md` → notebook berhasil menemukan driver-driver ini.
