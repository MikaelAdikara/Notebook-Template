# Panduan Menulis Artikel (Final Stage) — Churn & Insurance Analytics

Panduan ini memetakan **output notebook `churn_insurance_master.ipynb` → bagian artikel**, plus template kalimat (English) yang tinggal diisi angka. Semua angka yang dibutuhkan ada di `outputs/churn_insurance/insights.md`, `tables/`, `report_tables.xlsx`, dan `figures/`.

> **Jalur tercepat:** notebook otomatis membuat **`outputs/churn_insurance/REPORT_DRAFT.docx`** (format soal, angka & figure run kamu sudah masuk) + **`REPORT_TODO.md`** (daftar bagian `[EDIT]` yang wajib kamu lengkapi). Panduan ini menjelaskan *kenapa* strukturnya begitu & cara menulis bagian `[EDIT]` dengan baik. Prosedur lengkap: `00_MULAI_DI_SINI.md`.

---

## 0. Aturan format (dari soal) — cek sebelum submit

| Aturan | Nilai | Cara di Word |
|---|---|---|
| Maks halaman | **10 halaman** (tidak termasuk cover & lampiran) | Insert → Section Break sebelum lampiran supaya mudah dihitung |
| Kertas | A4 | Layout → Size → A4 |
| Font | Times New Roman 12 | Home → Styles → Normal → Modify |
| Spasi | 1.15 | Paragraph → Line spacing → Multiple 1.15 |
| Margin | Top & Bottom **4 cm**, Left & Right **3 cm** | Layout → Margins → Custom |
| Nama file | `TeamName_Final Stage 1` | contoh `DataWizards_Final Stage 1.pdf` |
| Format | PDF | File → Save As → PDF |
| Pengumpulan | ZIP berisi artikel + syntax (.ipynb/.rmd) + file lain, nama sama | `DataWizards_Final Stage 1.zip` |
| Tools | Hanya R (rmd) / Python (ipynb), **bukan Google Colab** | jalankan di Jupyter/VS Code lokal |

Template Word dengan format di atas sudah disiapkan: **`Article_Template_Final_Stage.docx`** (folder ini).

> Area tulis efektif: 15 cm × 21.7 cm per halaman ≈ 40–44 baris teks. Figure lebar penuh ≈ 6–8 cm tinggi. **Budget realistis: 7–9 figure/tabel** di 10 halaman. Sisanya → lampiran.

---

## 1. Struktur artikel 10 halaman (budget halaman)

| # | Bagian | Hal. | Isi | Sumber dari notebook |
|---|---|---|---|---|
| — | Cover | (tidak dihitung) | Judul, nama tim, universitas, logo | — |
| 0 | **Executive Summary / Abstract** | 0.5 | Masalah, pendekatan, 3 temuan utama (angka!), 3 rekomendasi utama, dampak ($) | `insights.md` (Business, Drivers, Recommendations) |
| 1 | **Introduction & Business Problem** | 0.75 | Konteks industri asuransi, mengapa churn/lapse mahal, tujuan analisis, pertanyaan riset | Playbook §D (domain) |
| 2 | **Data & Methodology** | 1.5 | Deskripsi data, cleaning, feature engineering, pencegahan leakage, kerangka analisis (diagram alur), validasi | Section 3–5, 13; `data_quality_report`, `leakage_screen` |
| 3 | **Findings** | 4 | 3.1 Churn overview · 3.2 Key drivers · 3.3 When customers churn (survival) · 3.4 High-risk segments · 3.5 Predictive model · 3.6 Explainability | Section 4, 7, 9, 10, 11, 14–20 |
| 4 | **Business Impact & Recommendations** | 2.5 | Risk tiers, risk×value, campaign ROI, what-if, personas, tabel rekomendasi + KPI + roadmap | Section 21–22 |
| 5 | **Conclusion & Limitations** | 0.5 | Ringkasan, keterbatasan (asosiasi ≠ kausal, data snapshot), saran lanjutan | — |
| — | References | (biasanya dihitung — cek aturan; buat ringkas) | 5–10 referensi metode | §5 di bawah |
| — | Appendix | (tidak dihitung) | figure/tabel tambahan, detail model, hyperparameter | sisa figure |

### Rekomendasi pemilihan figure/tabel (8 item inti)
1. **Fig — Churn rate by top drivers** (`figXX_driver_churn_rate_1.png`) → Findings 3.2
2. **Table — Key driver evidence matrix** (`driver_evidence_matrix.csv`, ambil 6–8 baris, kolom: driver, high-risk level & churn rate, OR, HR, SHAP rank) → 3.2
3. **Fig — Kaplan-Meier + hazard by tenure** (`km_overall`, `km_by_group` atau `hazard_by_tenure`) → 3.3
4. **Table/Fig — Segment rules** (`segment_rules.csv` top 3 + 1 loyal) atau `interaction_heatmaps` → 3.4
5. **Table — Model comparison** (leaderboard ringkas) + **Fig ROC / Gains** (`roc_pr_curves` atau `gains_and_lift`) → 3.5
6. **Fig — SHAP beeswarm** (`shap_beeswarm`) → 3.6
7. **Fig — Risk × value matrix** atau **campaign profit curve** → 4
8. **Table — Recommendations** (driver → action → evidence → KPI) → 4

Cadangan (kalau ada ruang): what-if bar chart, persona heatmap, odds-ratio forest plot, waterfall 1 customer.

---

## 2. Template kalimat per bagian (English)

> Ganti `[...]` dengan angka dari `insights.md` / tabel. Jangan copy-paste semua — pilih yang paling kuat, lalu **parafrase** dengan gaya tim.

### 0. Executive Summary
> Customer churn erodes [X]% of the annual premium base of [Company]. Using data on [N] policyholders, we combined statistical testing, survival analysis, interpretable regression and gradient-boosted machine learning to identify why and when customers leave. Churn is concentrated among customers who [driver 1], [driver 2] and [driver 3]; the risk is highest in the first [k] months of tenure. Our predictive model (ROC-AUC [0.xx]) ranks customers so that targeting the top 20% captures [yy]% of churners. We recommend (1) [rec 1], (2) [rec 2], and (3) [rec 3], which a model-based simulation suggests could avoid ≈[z] churners per 1,000 customers and yield a net retention benefit of [IDR …] at an ROI of [r]x.

### 1. Introduction
> In insurance, retaining an existing policyholder is substantially cheaper than acquiring a new one, and policy lapses directly reduce future premium income and the recovery of acquisition costs. This study addresses three questions: (i) Which customer, policy and service factors drive churn? (ii) When during the customer lifecycle is churn risk highest? (iii) Which customers should be prioritised, and with what interventions, to maximise retained value?

### 2. Data & Methodology
> The dataset contains [N] customers and [p] variables covering demographics, policy characteristics, premium and payment behaviour, claims and service interactions. The overall churn rate is [x]%. Data preparation included type correction (e.g. numeric values stored as text), harmonisation of inconsistent category labels, removal of [d] duplicate records and treatment of impossible values (e.g. age > 110). We engineered [k] domain features such as premium-to-income ratio, claim frequency per year of tenure, claim rejection rate and tenure bands. Variables recorded only after churn (e.g. [cancellation_reason]) were excluded to prevent target leakage.
>
> Our analytical framework has four layers (Figure 1): (1) univariate driver analysis using χ²/Mann-Whitney tests with effect sizes (Cramér's V, rank-biserial r), Information Value and Benjamini-Hochberg correction; (2) survival analysis (Kaplan-Meier, log-rank tests and Cox proportional hazards) to capture *when* churn occurs; (3) a multivariate logistic regression for interpretable odds ratios; and (4) predictive machine learning (logistic regression, random forest, LightGBM, XGBoost, CatBoost) evaluated with stratified [5]-fold cross-validation, tuned with Bayesian optimisation (Optuna) and combined via ensemble selection. Model behaviour was explained with SHAP values and partial dependence, and translated into business value through lift analysis, customer lifetime value (CLV), a risk–value matrix and a retention campaign ROI simulation.

**Tips:** buat **diagram alur** sederhana (kotak-panah) di Word/PowerPoint: *Data → Cleaning & FE → Driver analysis → Survival → Interpretable model → ML + Explainability → Business simulation → Recommendations*. Juri suka metodologi yang jelas & sistematis.

### 3.1 Churn overview
> [x]% of customers churned. Churn is moderately imbalanced, so we evaluate models with ROC-AUC and precision–recall rather than accuracy.

### 3.2 Key drivers
> Table [2] summarises the evidence for each driver. Payment method shows the strongest actionable association: customers paying by [Cash] churn at [26.2]% versus [13.8]% for [auto-debit] (χ² p < 0.001, Cramér's V = [0.13]); holding other factors constant, non-automatic payers have [2.1]× higher odds of churning (OR = [2.12], 95% CI [1.81–2.49]). Premium increases at renewal are the second key driver: customers facing increases above [12.9]% churn at [31.7]% ([1.5]× the average).
>
> Drivers that are consistent across univariate tests, the multivariate model and SHAP are considered robust.

### 3.3 When do customers churn?
> The Kaplan-Meier curve (Figure [3]) shows that [7.3]% of customers are lost within the first 12 months and [16.3]% within 24 months. The churn hazard is highest at [interval] months, indicating that [early-life / first renewal] is the critical period. Survival differs significantly by [payment method] (log-rank p < 0.001). In the Cox model, [auto-renewal] reduces the churn hazard by [36]% (HR = [0.64], 95% CI [0.58–0.71]).

### 3.4 High-risk segments
> A decision-tree segmentation identifies interpretable high-risk groups. For example, customers with [frequent claims], [non-automatic payment] and [at least one complaint] churn at [57.9]% ([2.8]× the average), although they represent only [2.8]% of the base. Conversely, [long-tenure customers with stable premiums] churn at only [2.2]%.

### 3.5 Predictive model
> Table [3] compares the models. The final ensemble ([logistic regression + CatBoost]) achieves an out-of-fold ROC-AUC of [0.749] (PR-AUC [0.45]), well above the random baseline (0.50). Validation checks confirmed the absence of leakage (AUC with shuffled labels = [0.51]) and similar train/test distributions (adversarial AUC = [0.48]). Targeting the top 20% highest-risk customers captures [44.5]% of all churners, a [2.2]× lift over random selection (Figure [4]).

### 3.6 Explainability
> SHAP analysis (Figure [5]) confirms that [auto-renewal], [premium change] and [payment method] contribute most to predicted churn risk. Higher premium increases consistently push risk upward, while additional products reduce it — consistent with the switching-cost hypothesis.

### 4. Business impact & recommendations
> Expected annual premium at risk is [IDR 9.8B] ([20.5]% of the premium base). Combining churn risk with customer value (Figure [6]) identifies a 'Priority Save' group — [9.6]% of customers holding [28.3]% of value at risk. A campaign simulation (assumed [30]% success rate and [IDR 150K] cost per contact) shows that targeting the top [50]% ranked by expected loss maximises net benefit at [IDR 793M] (ROI [1.3]×), compared with [IDR 208M] for random targeting; this conclusion holds across a sensitivity range of success rates and costs.
>
> Table [4] lists our recommendations with supporting evidence, target segment and KPI. [Recommendation 1]... A model-based what-if analysis suggests that moving [30]% of manual payers to auto-debit would avoid ≈[16] churners per 1,000 customers. Because these estimates are associational, we recommend validating each intervention with a controlled pilot (A/B test) before full rollout.

**Format tabel rekomendasi (sangat disarankan):**

| # | Insight (evidence) | Action | Target segment | Expected impact | KPI | Timeline |
|---|---|---|---|---|---|---|
| 1 | Manual payers churn 2.1× odds | Auto-debit migration with incentive | Manual payers, High/Medium tier | −1.6 pp churn @30% adoption | % on auto-pay; lapse of converted | Quick win (0–3 mo) |

**Roadmap** (opsional, 3 kolom): *Quick wins (0–3 bulan)* → *Medium (3–6 bulan)* → *Long term (6–12 bulan: early-warning system, loyalty program)*.

### 5. Conclusion & limitations
> We find that churn is driven primarily by [payment friction, renewal price shocks and service failures], and is concentrated early in the customer lifecycle. Limitations: (i) the analysis is based on a single snapshot, so relationships are associational rather than causal; (ii) the ROI simulation relies on assumed campaign costs and success rates; (iii) unobserved factors (e.g. competitor offers, life events) are not captured. Future work should collect [reasons for leaving / interaction logs] and evaluate interventions through randomised pilots.

---

## 3. Tips menulis yang menaikkan nilai

1. **Angka di setiap klaim.** "Churn tinggi di customer baru" ❌ → "Customers in their first 6 months churn at 28.2%, 3.4× the 8.4% of customers with 5+ years" ✅.
2. **Insight → So what → Action.** Setiap temuan diikuti implikasi bisnis.
3. **Konsistensi bukti.** Tekankan driver yang muncul di statistik, regresi, survival, **dan** SHAP → kuat.
4. **Bedakan actionable vs non-actionable.** Umur/region → untuk targeting; payment method/auto-renew/complaint → untuk intervensi.
5. **Jujur soal asumsi & keterbatasan.** Juri menghargai kesadaran "asosiasi ≠ kausal", asumsi ROI, potensi bias.
6. **Caption figure informatif**: "Figure 3. Kaplan-Meier survival curve: 7% of customers churn within 12 months; risk peaks around the first renewal." (caption = insight).
7. **Jangan dump output mentah** (tabel 30 kolom). Ringkas jadi 4–6 kolom yang penting.
8. **Gunakan istilah asuransi** dengan tepat (lapse, persistency, renewal, premium, claims experience) — lihat Playbook §D.
9. **Satu warna konsisten**: merah = risiko/churn, biru = retained (sudah default di notebook).
10. **Figure DPI 300** (`CFG.FIG_DPI = 300`) untuk versi final.

---

## 4. Checklist akhir artikel
- [ ] ≤ 10 halaman (tanpa cover & lampiran), A4, TNR 12, spasi 1.15, margin 4/4/3/3 cm
- [ ] Executive summary memuat angka kunci & rekomendasi utama
- [ ] Setiap figure/tabel bernomor, ber-caption, dirujuk di teks
- [ ] Metodologi menyebut: validasi (CV), pencegahan leakage, metrik, uji statistik + effect size
- [ ] Rekomendasi: spesifik, ada target segmen, dampak estimasi, KPI, timeline
- [ ] Keterbatasan & asumsi disebut
- [ ] Nama file `TeamName_Final Stage 1.pdf`; ZIP berisi PDF + .ipynb (+ data/outputs pendukung) dengan nama sama
- [ ] Notebook di-run ulang bersih (Restart & Run All) sebelum di-zip

---

## 5. Referensi metode (format APA, pilih yang dipakai)

- Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*, 2623–2631.
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B, 57*(1), 289–300.
- Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.
- Caruana, R., Niculescu-Mizil, A., Crew, G., & Ksikes, A. (2004). Ensemble selection from libraries of models. *Proceedings of the 21st International Conference on Machine Learning*.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794.
- Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B, 34*(2), 187–220.
- Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association, 53*(282), 457–481.
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems, 30*.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems, 30*.
- Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. *Advances in Neural Information Processing Systems, 31*.
- Siddiqi, N. (2006). *Credit risk scorecards: Developing and implementing intelligent credit scoring*. Wiley. (Weight of Evidence & Information Value)
- Verbeke, W., Dejaeger, K., Martens, D., Hur, J., & Baesens, B. (2012). New insights into churn prediction in the telecommunication sector: A profit driven data mining approach. *European Journal of Operational Research, 218*(1), 211–229. (profit-based churn evaluation)
