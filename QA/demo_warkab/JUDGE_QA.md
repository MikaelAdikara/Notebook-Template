# JUDGE Q&A PREP — Warkab

Jawaban sudah berisi angka run ini. Latih jawab ≤ 30 detik per pertanyaan.

## Juri industri asuransi

**Q: Berapa uang yang dipertaruhkan dan berapa yang bisa diselamatkan?**  
A: Expected annual premium at risk IDR 9.9B (20.8% of base). Optimal campaign: top 56% by expected loss → net IDR 807.7M (ROI 1.2×), profitable in 9/9 sensitivity scenarios.

**Q: Kenapa nasabah keluar — dan apakah itu bisa dikendalikan perusahaan?**  
A: Top drivers: premium change at last renewal (%), payment method, auto-renewal and complaints in the last 12 months. Actionable: premium change at last renewal (%), payment method and auto-renewal. Non-actionable drivers dipakai untuk targeting, bukan intervensi.

**Q: Apakah model ini boleh dipakai untuk pricing/underwriting?**  
A: Tidak. Model card membatasi penggunaan untuk retention outreach; fairness audit menunjukkan kalibrasi per kelompok; pricing harus mengikuti prinsip fairness (contoh larangan price-walking FCA 2021).

**Q: Bagaimana dengan regulasi & perlindungan konsumen di Indonesia?**  
A: Rekomendasi bersifat layanan (pengingat, kemudahan bayar, follow-up keluhan) — sejalan dengan arah OJK yang menekankan transparansi dan perlindungan pemegang polis (SEOJK 5/2022; POJK 8/2024). Data nasabah dipakai sesuai tujuan; tidak ada keputusan otomatis yang merugikan nasabah.

## Juri praktisi / data science

**Q: AUC 0.760 — bukankah rendah?**  
A: Churn adalah perilaku manusia dengan noise tinggi; yang penting bagi bisnis adalah konsentrasi: top 20% berisi 46% churner (2.3× random) dan kampanye menguntungkan. Learning curve masih naik, jadi data tambahan akan membantu.

**Q: Bagaimana mencegah leakage dan overfitting?**  
A: Leakage screen otomatis (nama, missingness, single-feature AUC, model-level), semua metrik out-of-fold, target encoding di dalam fold, shuffled-label AUC ≈ 0.52, adversarial validation, DeLong & bootstrap CI.

**Q: Kenapa tidak deep learning?**  
A: Neural network (MLP) sudah dicoba: AUC 0.737 vs gradient boosting 0.758, sejalan dengan Grinsztajn et al. (2022) bahwa model berbasis pohon unggul di data tabular. Logistic regression mencapai AUC 0.757, sehingga ada opsi transparan.

**Q: Berapa eksperimen yang dicoba? Bukti trial-and-error?**  
A: 32 eksperimen tercatat (experiment_log.csv): model zoo, Optuna, multi-seed, feature selection, ablation, 6 metode ensemble; figure 'model development journey' di Appendix F.

**Q: Bagaimana deploy & monitoring?**  
A: Skor bulanan → tier × value × uplift → CRM dengan control group → ukur uplift → monitor PSI (>0.25), AUC drop (>0.03), kalibrasi → retrain kuartalan (Appendix J, MLOps loop).

## Juri akademik / statistik

**Q: Apakah efeknya kausal?**  
A: Driver = asosiasi (dibedakan jelas). Untuk tuas yang bisa dikendalikan kami pakai AIPW cross-fitted (doubly robust) + uji placebo + E-value + overlap; hanya efek berlabel 'robust' yang dipakai sebagai dasar rekomendasi, dan semuanya diusulkan diuji via RCT pilot.

**Q: Asumsi proportional hazards?**  
A: Diuji dengan Schoenfeld test; bila dilanggar, HR dibaca sebagai efek rata-rata waktu dan dilengkapi Weibull AFT + RMST.

**Q: Multiple testing?**  
A: Benjamini–Hochberg untuk driver univariat; Holm untuk perbandingan model & ablation; effect size & IV dilaporkan, bukan p-value saja.

**Q: Kenapa asumsi biaya/success rate itu?**  
A: Dari soal. kesimpulan diuji pada 9 kombinasi (success ±50%, cost ×0.5–×2) dan EMPC mengintegrasikan ketidakpastian tingkat penerimaan (Beta distribution).
