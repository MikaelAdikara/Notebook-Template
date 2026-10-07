# REPORT TODO — DataWizards

Kerjakan semua item ini di `REPORT_DRAFT.docx` (bagian kuning = wajib diedit).

## A. Bagian [EDIT] di draft

- [ ] **Executive Summary** — tambahkan 1 kalimat konteks spesifik dari soal (produk, pasar, tujuan manajemen) dan rapikan ringkasan ini maks. ½ halaman.
- [ ] **1. Introduction and Business Problem** — konteks PT Asuransi Sejahtera dari soal — lini produk, situasi churn saat ini, kenapa manajemen peduli.
- [ ] **2.1 Data** — demographics, policy characteristics, premium & payment behaviour, claims and service interactions
- [ ] **2.3 Analytical framework** — sisipkan diagram alur (Figure 1) — Data → Cleaning & Feature Engineering → Driver analysis → Survival → Interpretable model → ML & explainability → Business simulation → Recommendations. Bisa dibuat di PowerPoint/Word SmartArt.
- [ ] **3.1 Churn overview** — moderate/severe
- [ ] **3.2 Key churn drivers** — jelaskan 2–3 driver utama dengan bahasa bisnis — kenapa masuk akal di industri asuransi (lihat PLAYBOOK §D2).
- [ ] **3.3 When do customers churn?** — interpretasi — kapan momen kritis (onboarding? renewal pertama?) dan implikasinya untuk timing intervensi.
- [ ] **3.6 Explaining churn risk** — hubungkan SHAP dengan temuan statistik — driver mana yang konsisten di semua metode (robust).
- [ ] **4.2 Retention campaign simulation** — sebutkan asumsi bisnis — margin 20%, cost per contact 150.00K IDR, success rate 30% — dan sumbernya (soal / asumsi wajar); rujuk tabel sensitivity di Appendix.
- [ ] **4.4 Churn personas** — beri nama tiap persona (misal 'Price-shocked renewers', 'Service-frustrated claimants') + 1 intervensi khusus per persona.
- [ ] **4.5 Recommendations** — tambahkan roadmap — Quick wins (0–3 bulan), Medium (3–6 bulan), Long term (6–12 bulan) — dan rencana pengukuran (A/B test dengan control group).
- [ ] **5. Conclusion and Limitations** — 1–2 kalimat jawaban langsung untuk 3 pertanyaan riset.
- [ ] **5. Conclusion and Limitations** — interaction logs / stated reasons for leaving

## B. Verifikasi angka & narasi

- [ ] Semua angka di draft sama dengan `insights.md` / `tables/` (run terakhir, `RUN_MODE='full'`).
- [ ] Mapping target benar (churn = 1) dan tidak ada fitur leak di model (Section 5.3).
- [ ] Parameter bisnis (margin 20%, cost 150.00K, success 30%) sesuai soal / dinyatakan sebagai asumsi.
- [ ] Kalimat otomatis diparafrase dengan gaya tim (jangan copy mentah).
- [ ] Nama fitur di teks sudah otomatis dibuat lebih ramah (pretty labels) — cek & perbaiki; untuk label custom isi `CFG.FEATURE_LABELS` lalu run ulang cell 24.3. Figure masih memakai nama kolom asli → sebutkan di caption bila perlu.
- [ ] Driver yang dibahas = yang konsisten di evidence matrix (bukan satu metode saja).
- [ ] Rekomendasi spesifik: siapa (segmen + ukuran), apa, kapan, dampak, KPI.
- [ ] Persona diberi nama & intervensi khusus.
- [ ] Keterbatasan & asumsi disebut.

## C. Format (aturan soal)

- [ ] ≤ 10 halaman (tanpa cover & appendix) — kalau lebih: pindahkan figure ke Appendix, ringkas 3.x.
- [ ] A4, Times New Roman 12, spasi 1.15, margin atas/bawah 4 cm, kiri/kanan 3 cm (sudah di draft — jangan diubah).
- [ ] Figure/tabel bernomor urut & dirujuk di teks; caption menyatakan insight.
- [ ] Figure versi `FIG_DPI = 300`.
- [ ] Save As PDF: `DataWizards_Final Stage 1.pdf`.
- [ ] ZIP: `DataWizards_Final Stage 1.zip` berisi PDF + notebook (.ipynb) + file pendukung (cell 24.4).

## D. Sumber setiap bagian laporan

| Bagian | File output |
|---|---|
| Data & cleaning | tables/data_quality_report.csv, tables/leakage_screen.csv |
| Drivers | tables/driver_table.csv, tables/driver_evidence_matrix.csv, figures/*driver_churn_rate* |
| Survival | tables/hazard_by_tenure_interval.csv, tables/cox_hazard_ratios.csv, figures/*km_* |
| Segments | tables/segment_rules.csv, figures/*interaction_heatmaps*, *segment_tree* |
| Interpretable model | tables/logit_odds_ratios.csv, figures/*logit_odds_ratios* |
| Model | tables/leaderboard_all.csv, tables/bootstrap_ci_final_model.csv, figures/*roc_pr*, *gains_and_lift* |
| Explainability | tables/shap_importance.csv, figures/*shap_* , *partial_dependence* |
| Business | tables/risk_tiers.csv, risk_value_quadrants.csv, campaign_optimum.csv, campaign_sensitivity.csv, what_if_scenarios.csv, churn_personas.csv |
| Recommendations | tables/recommendations.csv |
| Semua kalimat insight | insights.md |