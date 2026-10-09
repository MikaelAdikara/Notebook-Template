# NARRATIVE OPTIONS — Warkab

Semua teks di bawah sudah terisi angka dari run ini. Pilih yang paling sesuai dengan case, tempel ke REPORT_DRAFT.docx, atau set `CFG.REPORT_TITLE` / `CFG.NARRATIVE_ANGLE` lalu run ulang Section 24.3.

## 1. Judul

- Removing Payment Friction: Evidence-Based Churn Prevention for PT Asuransi Nusantara Sejahtera
- Price Shock at Renewal: Who Leaves, When, and How to Keep Them at PT Asuransi Nusantara Sejahtera
- Service Recovery as Retention: Turning Claims and Complaints into Loyalty at PT Asuransi Nusantara Sejahtera
- Protecting the Premium Base: Predicting, Explaining and Profitably Preventing Churn at PT Asuransi Nusantara Sejahtera
- Who Leaves, When, and What Works: A Causal and Predictive Retention Strategy for PT Asuransi Nusantara Sejahtera

## 2. Framing executive summary (pilih 1 sebagai kalimat pembuka)

- **Lifecycle:** "Churn at PT Asuransi Nusantara Sejahtera is a timing problem: risk peaks in tenure interval [18, 24) months, when 0.99% of active customers leave per month."
- **Money-first:** "Churn puts IDR 10B of annual premium at risk; 46% of it sits in the 20% of customers our model flags."
- **Driver-first:** "Customers with premium change at last renewal (%) = '13.2–30.6' are 1.6 times more likely to leave than average."
- **Action-first:** "A targeted retention campaign on the top 50% of customers returns IDR 810.8M net (ROI 1.4×), far above random targeting."

## 3. Nama persona (ganti P1, P2, … di laporan)

- P2 → **"Manual Renewers"** (drivers: auto-renewal, payment method; 53% of at-risk customers, actual churn 32.5%). Intervensi: Auto-debit enrolment incentive, reminders before the grace period ends, flexible payment dates and instalments.
- P1 → **"Price-Shocked Renewers"** (drivers: premium change at last renewal (%); 47% of at-risk customers, actual churn 36.8%). Intervensi: Cap or phase in increases for loyal at-risk customers, explain value, offer deductible/coverage adjustments instead of lapse.

## 4. Paragraf diskusi per tema driver (dengan sitasi terverifikasi)

### premium change at last renewal (%) (tema: price)

- **Temuan:** riskiest group '13.2–30.6' churns at 33.5% (1.6× average; IV 0.16).
- **Diskusi:** Price sensitivity at renewal agrees with Guelman and Guillén (2014) and Brockett et al. (2008); renewal pricing must also be fair (Financial Conduct Authority, 2021).
- **Aksi:** Cap or phase in increases for loyal at-risk customers, explain value, offer deductible/coverage adjustments instead of lapse.
- **KPI:** churn among customers with increases; price elasticity

### payment method (tema: payment)

- **Temuan:** riskiest group 'Bank Transfer' churns at 25.5% (1.2× average; IV 0.10).
- **Diskusi:** Payment behaviour matters, in line with Hein et al. (2020) and with survey evidence that forgetting to pay explains a large share of lapses (Gottlieb & Smetters, 2021).
- **Aksi:** Auto-debit enrolment incentive, reminders before the grace period ends, flexible payment dates and instalments.
- **KPI:** share on auto-pay; cure rate of late payers

### complaints in the last 12 months (tema: service)

- **Temuan:** riskiest group '≥2' churns at 44.3% (2.1× average; IV 0.11).
- **Diskusi:** The claims and service experience is linked to renewal (Fallis et al., 2022); the association is observational and should be validated by a pilot.
- **Aksi:** Proactive contact within 48 hours of a complaint or rejected claim, settlement SLAs, transparent rejection explanations with appeal path.
- **KPI:** post-claim churn; complaint resolution time; claim NPS

### tenure (months) (tema: lifecycle)

- **Temuan:** riskiest group '1–6' churns at 28.6% (1.4× average; IV 0.15).
- **Diskusi:** Early-tenure churn is consistent with evidence that lapse declines with contract age (Eling & Kiesenbauer, 2014) and that first-year lapse is the highest (Fleigle et al., 2026). Because acquisition costs are front-loaded, early retention has the highest value per retained policy.
- **Aksi:** Structured onboarding (welcome call, coverage check, app activation, check-in before the hazard peak) and treating the first renewal as a critical moment.
- **KPI:** first-year persistency; churn in the peak-hazard window

### number of ANS products (tema: relationship)

- **Temuan:** riskiest group '1' churns at 23.8% (1.1× average; IV 0.05).
- **Diskusi:** Cancellation of one policy predicts cancellation of others (Brockett et al., 2008).
- **Aksi:** Multi-policy bundles and relationship-level early warnings.
- **KPI:** products per customer; churn of bundled vs single

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
