# NARRATIVE OPTIONS — DataWizards

Semua teks di bawah sudah terisi angka dari run ini. Pilih yang paling sesuai dengan case, tempel ke REPORT_DRAFT.docx, atau set `CFG.REPORT_TITLE` / `CFG.NARRATIVE_ANGLE` lalu run ulang Section 24.3.

## 1. Judul

- The First Six Months Decide: A Data-Driven Retention Strategy for a Texas auto insurer
- Protecting the Premium Base: Predicting, Explaining and Profitably Preventing Churn at a Texas auto insurer
- Who Leaves, When, and What Works: A Causal and Predictive Retention Strategy for a Texas auto insurer

## 2. Framing executive summary (pilih 1 sebagai kalimat pembuka)

- **Lifecycle:** "Churn at a Texas auto insurer is a timing problem: risk peaks in tenure interval [90, 180) days, when 1.16% of active customers leave per 30 days."
- **Money-first:** "Churn puts USD 17.8M of annual premium at risk; 51% of it sits in the 20% of customers our model flags."
- **Driver-first:** "Customers with tenure band = '0-6m' are 4.2 times more likely to leave than average."
- **Action-first:** "A targeted retention campaign on the top 10% of customers returns USD 590.8K net (ROI 1.5×), far above random targeting."

## 3. Nama persona (ganti P1, P2, … di laporan)

- P2 → **"Mixed-Risk Customers"** (drivers: no dominant driver (moderate, diffuse risk); 79% of at-risk customers, actual churn 8.5%). Intervensi: Targeted pilot on the high-risk group.
- P1 → **"New & Unanchored"** (drivers: days tenure, tenure (years), cust orig date (days since); 21% of at-risk customers, actual churn 51.9%). Intervensi: Structured onboarding (welcome call, coverage check, app activation, check-in before the hazard peak) and treating the first renewal as a critical moment.

## 4. Paragraf diskusi per tema driver (dengan sitasi terverifikasi)

### tenure band (tema: lifecycle)

- **Temuan:** riskiest group '0-6m' churns at 48.8% (4.2× average; IV 0.89).
- **Diskusi:** Early-tenure churn is consistent with evidence that lapse declines with contract age (Eling & Kiesenbauer, 2014) and that first-year lapse is the highest (Fleigle et al., 2026). Because acquisition costs are front-loaded, early retention has the highest value per retained policy.
- **Aksi:** Structured onboarding (welcome call, coverage check, app activation, check-in before the hazard peak) and treating the first renewal as a critical moment.
- **KPI:** first-year persistency; churn in the peak-hazard window

### age band (tema: demographic)

- **Temuan:** riskiest group '25-34' churns at 14.6% (1.2× average; IV 0.04).
- **Diskusi:** Demographic risk differences are targeting signals, not levers.
- **Aksi:** Life-stage tailored communication and channels.
- **KPI:** churn by age band

### length of residence (tema: other)

- **Temuan:** riskiest group '0–1' churns at 13.5% (1.2× average; IV 0.01).
- **Diskusi:** This driver is specific to the portfolio and should be explored with domain experts.
- **Aksi:** Targeted pilot on the high-risk group.
- **KPI:** churn of the high-risk group

### latitude (tema: geography)

- **Temuan:** riskiest group 'Missing' churns at 12.4% (1.1× average; IV 0.00).
- **Diskusi:** Regional differences may reflect competition and service capacity.
- **Aksi:** Regional retention focus and local root-cause review.
- **KPI:** churn by region

### premium-to-income ratio (tema: price)

- **Temuan:** riskiest group '0.0182–0.0232' churns at 12.4% (1.1× average; IV 0.00).
- **Diskusi:** Price sensitivity at renewal agrees with Guelman and Guillén (2014) and Brockett et al. (2008); renewal pricing must also be fair (Financial Conduct Authority, 2021).
- **Aksi:** Cap or phase in increases for loyal at-risk customers, explain value, offer deductible/coverage adjustments instead of lapse.
- **KPI:** churn among customers with increases; price elasticity

## 5. Kalau soal menanyakan … → ambil dari

| Pertanyaan soal | Bagian laporan / output |
|---|---|
| Faktor penyebab churn | 3.1 + Table evidence + Appendix C/D/G (`driver_evidence_matrix.csv`) |
| Kapan nasabah churn | 3.2 + Appendix E (hazard, KM, RMST, AFT) |
| Segmen paling berisiko / profil | 3.3 + personas (4.x) + `segment_rules.csv`, `churn_personas.csv` |
| Prediksi / model terbaik | 3.4 + Appendix F (`model_comparison_full.csv`, `experiment_log.csv`) + `submission.csv` |
| Strategi retensi / rekomendasi | 4–5 + `recommendations.csv`, `implementation_roadmap.csv`, `pilot_design_power.csv` |
| Dampak finansial / ROI | 4.1–4.2 + `campaign_optimum.csv`, `campaign_sensitivity.csv`, EMPC |
| Intervensi mana yang efektif | 4.3 + Appendix H (AIPW, robustness, uplift) |
| Daftar nasabah yang harus dihubungi | `tables/test_customer_action_list.csv` (tier, value, uplift) |
| Monitoring / implementasi | Appendix J (model card, MLOps loop, roadmap) + dashboard |
