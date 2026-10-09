# QA CHECK — Warkab

Case: `<folder-demo>\demo_warkab`

**43 PASS · 0 FAIL · 2 WARN**

| Status | Cek | Detail |
|---|---|---|
| PASS | Run selesai (run_summary.json) | <folder-demo>\demo_warkab\outputs/churn_insurance\run_summary.json |
| PASS | Tanpa section error | 0 error |
| PASS | Target churn = 1 ter-mapping | {'No': 0, 'Yes': 1} |
| PASS | Skor model tercatat | hill_climb / OOF AUC 0.7599 |
| PASS | Artikel DOCX | <folder-demo>\demo_warkab\outputs/churn_insurance\Warkab_Final Stage 1.docx |
| PASS | Artikel PDF | <folder-demo>\demo_warkab\outputs/churn_insurance\Warkab_Final Stage 1.pdf |
| PASS | Isi utama ≤ 10 halaman (cover & appendix tidak dihitung) | 10 halaman isi, total PDF 83 |
| PASS | Nama tim 'Warkab' di cover |  |
| PASS | Anggota 'Mikael Alexander Adikara Purnama' di cover |  |
| PASS | Anggota 'Pandu Winata' di cover |  |
| PASS | Nama perusahaan dari soal dipakai | PT Asuransi Nusantara Sejahtera |
| PASS | Konteks soal (CASE_CONTEXT) masuk Introduction |  |
| PASS | Pertanyaan soal dijawab: 'What are the main drivers of churn, and how large …' |  |
| PASS | Pertanyaan soal dijawab: 'When during the customer lifecycle is churn risk h…' |  |
| PASS | Pertanyaan soal dijawab: 'How accurately can churn be predicted for the cust…' |  |
| PASS | Pertanyaan soal dijawab: 'Which retention programme within the Rp1.5 billion…' |  |
| PASS | Skala portofolio dipakai | 1,200,000 |
| PASS | Budget soal dibahas |  |
| PASS | Parameter bisnis ditulis 'given in the case' |  |
| PASS | Riset [case_facts] masuk artikel: 'ANS manages around 1.2 million active policie…' |  |
| PASS | Riset [case_facts] masuk artikel: 'Management estimates that every lost policyho…' |  |
| PASS | Riset [industry_facts] masuk artikel: 'Renewal premiums accounted for Rp77.07 trilli…' |  |
| PASS | Riset [industry_facts] masuk artikel: 'Surrender claims paid by Indonesian life insu…' |  |
| PASS | Semua sumber [industry_facts] verified = Y | 0 belum diverifikasi |
| WARN | Riset [literature] masuk artikel: 'Using more than one million contracts, Eling …' | tidak ditemukan (mungkin dipangkas autofit / tema tidak cocok driver) |
| PASS | Riset [literature] masuk artikel: 'In a survey of recent lapsers, forgetting to …' |  |
| WARN | Riset [literature] masuk artikel: 'In the U.S. property and casualty market, aro…' | tidak ditemukan (mungkin dipangkas autofit / tema tidak cocok driver) |
| PASS | Riset [literature] masuk artikel: 'In an Indonesian insurer's portfolio, product…' |  |
| PASS | Riset [literature] masuk artikel: 'Uplift models can yield more profitable reten…' |  |
| PASS | Semua sumber [literature] verified = Y | 0 belum diverifikasi |
| PASS | Riset [custom_paragraphs] masuk artikel: 'For ANS, whose renewal premiums are 58% of pr…' |  |
| PASS | Riset [custom_paragraphs] masuk artikel: 'Two company initiatives make these actions ch…' |  |
| PASS | Tidak ada caption mentah (nama file) |  |
| PASS | Tidak ada penanda [EDIT] tersisa | cari [EDIT] di Word (highlight kuning) |
| PASS | Tidak ada 'nan'/'None' di teks isi |  |
| PASS | Daftar pustaka ada |  |
| PASS | Gaya tulisan tidak terasa AI (slop_check ≥ 80) | skor 98/100, 1 temuan → python QA/slop_check.py "Warkab_Final Stage 1.pdf" |
| PASS | Output submission.csv |  |
| PASS | Output dashboard/index.html |  |
| PASS | Output NARRATIVE_OPTIONS.md |  |
| PASS | Output JUDGE_QA.md |  |
| PASS | Output REPORT_TODO.md |  |
| PASS | Dashboard berisi data case ini |  |
| PASS | ZIP pengumpulan dibuat | <folder-demo>\demo_warkab\Warkab_Final Stage 1.zip |
| PASS | ZIP berisi PDF + notebook ter-eksekusi | 157 file |
