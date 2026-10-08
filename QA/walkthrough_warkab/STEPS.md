# Walkthrough — Warkab

| Step | Judul | Keterangan | Screenshot |
|---|---|---|---|
| 1 | Soal / casebook | Titik awal: soal dari panitia disimpan sebagai casebook.* di folder case. | screens/01_casebook.png |
| 2 | Folder kerja dibuat otomatis | new_case.py: data/, case_config.json, CASE_INTAKE.html, CASE_RESEARCH.xlsx, RESEARCH_PLAN, RUN_FAST.bat, RUN_FULL.bat. | screens/02_folder.png |
| 3 | Case Intake (offline form) | Semua informasi dari soal diisi di form → Download JSON → case_config.json (target, metrik, konteks, pertanyaan, parameter bisnis). | screens/03_intake.png |
| 4 | case_config.json (hasil intake) | Konfigurasi case Warkab: konteks, definisi churn, pertanyaan soal, intervensi, budget, parameter bisnis dari soal. | screens/04_config.png |
| 5 | Research Plan otomatis | research_helper.py membaca casebook: istilah kunci, kalimat berangka (kandidat fakta) dan query siap-klik (Scholar, Crossref, Garuda, OJK/AAJI/AAUI). | screens/05_research_plan.png |
| 6 | Research Plan — query per driver | Query literatur disesuaikan tema driver hasil fast run (lifecycle, payment, price, service, …). | screens/05_research_plan.png |
| 7 | Hasil riset tim: case_facts | Baris use = Y otomatis ditempel ke section laporan yang dipilih; referensinya masuk daftar pustaka (hanya bila disitasi). | screens/06_0_case_facts.png |
| 8 | Hasil riset tim: industry_facts | Baris use = Y otomatis ditempel ke section laporan yang dipilih; referensinya masuk daftar pustaka (hanya bila disitasi). | screens/06_1_industry_facts.png |
| 9 | Hasil riset tim: literature | Baris use = Y otomatis ditempel ke section laporan yang dipilih; referensinya masuk daftar pustaka (hanya bila disitasi). | screens/06_2_literature.png |
| 10 | Hasil riset tim: custom_paragraphs | Baris use = Y otomatis ditempel ke section laporan yang dipilih; referensinya masuk daftar pustaka (hanya bila disitasi). | screens/06_3_custom_paragraphs.png |
| 11 | RUN_FULL.bat — console | Notebook dijalankan headless; semua output tersimpan di notebook ter-eksekusi. 'no section errors' = seluruh analisis sukses. | screens/07_run_full_console.log.png |
| 12 | Ringkasan run | Target & mapping benar, kolom leakage dibuang otomatis, semua model + ensemble, tanpa section error. | screens/08_summary.png |
| 13 | Artikel — cover | Judul berbasis temuan, nama tim & anggota otomatis. | screens/09_article_p01.png |
| 14 | Artikel — Executive Summary & Introduction | Ringkasan berangka + konteks case + fakta casebook & industri dari CASE_RESEARCH. | screens/09_article_p02.png |
| 15 | Artikel — Findings (drivers) | Figure komposit + evidence matrix (4 metode). | screens/09_article_p04.png |
| 16 | Artikel — Prediction & model comparison | AUC dengan CI DeLong, EMPC, experiment log, ablation. | screens/09_article_p06.png |
| 17 | Artikel — Business impact & recommendations | Kampanye dalam budget, kausal, rekomendasi + pilot A/B; paragraf custom tim. | screens/09_article_p08.png |
| 18 | Artikel — Discussion & references | Literatur tim (CASE_RESEARCH) dikaitkan ke driver; daftar pustaka APA hanya yang disitasi. | screens/09_article_p10.png |
| 19 | Appendix (tidak dihitung halaman) | Appendix A–L: data, metodologi & arsitektur, driver, survival, model development, kausal, bisnis, governance. | screens/10_appendix_p12.png |
| 20 | Appendix (tidak dihitung halaman) | Appendix A–L: data, metodologi & arsitektur, driver, survival, model development, kausal, bisnis, governance. | screens/10_appendix_p18.png |
| 21 | Appendix (tidak dihitung halaman) | Appendix A–L: data, metodologi & arsitektur, driver, survival, model development, kausal, bisnis, governance. | screens/10_appendix_p26.png |
| 22 | Dashboard — Overview | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_0_dash_overview.png |
| 23 | Dashboard — Drivers | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_1_dash_drivers.png |
| 24 | Dashboard — Timing | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_2_dash_timing.png |
| 25 | Dashboard — Model | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_3_dash_model.png |
| 26 | Dashboard — Campaign simulator & causal | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_4_dash_campaign.png |
| 27 | Dashboard — Actions & customer list | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_5_dash_actions.png |
| 28 | Dashboard — Methodology | Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run. | screens/11_6_dash_method.png |
| 29 | NARRATIVE_OPTIONS.md | Pilihan judul/framing/nama persona, persiapan pertanyaan juri, dan checklist finalisasi — semua berisi angka run ini. | screens/12_NARRATIVE_OPTIONS.md.png |
| 30 | JUDGE_QA.md | Pilihan judul/framing/nama persona, persiapan pertanyaan juri, dan checklist finalisasi — semua berisi angka run ini. | screens/12_JUDGE_QA.md.png |
| 31 | REPORT_TODO.md | Pilihan judul/framing/nama persona, persiapan pertanyaan juri, dan checklist finalisasi — semua berisi angka run ini. | screens/12_REPORT_TODO.md.png |
| 32 | QA otomatis artikel (QA/qa_check.py) | Cek tanpa AI: ≤10 halaman, tim & anggota di cover, konteks/fakta/riset soal benar-benar masuk artikel, caption, dashboard, ZIP. | screens/12z_qa_check.png |
| 33 | Stress test — semua bentuk data | Setiap varian (data rusak/dimanipulasi) dijalankan end-to-end; PASS = tanpa satu pun section error. | screens/13_stress_00.png |
| 34 | Stress test — semua bentuk data | Setiap varian (data rusak/dimanipulasi) dijalankan end-to-end; PASS = tanpa satu pun section error. | screens/13_stress_11.png |
| 35 | Stress test — semua bentuk data | Setiap varian (data rusak/dimanipulasi) dijalankan end-to-end; PASS = tanpa satu pun section error. | screens/13_stress_22.png |
| 36 | Stress test — semua bentuk data | Setiap varian (data rusak/dimanipulasi) dijalankan end-to-end; PASS = tanpa satu pun section error. | screens/13_stress_33.png |
| 37 | ZIP pengumpulan | make_zip.py: <Tim>_Final Stage 1.pdf + notebook ter-eksekusi + supporting/ (figures, tables, Excel, dashboard, submission). | screens/14_zip.png |
