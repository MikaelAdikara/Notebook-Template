# Playbook Analisis Churn & Asuransi — "Jika X, maka Y"

Dokumen pegangan saat lomba (tanpa AI). Isinya: alur berpikir, aturan keputusan untuk berbagai kondisi data/hasil, cheat-sheet statistik, istilah asuransi, library strategi retensi, dan persiapan tanya-jawab juri.

**Daftar isi**
- A. Alur kerja saat lomba (timeline & decision map)
- B. Jika X → Y: kondisi data
- C. Jika X → Y: hasil analisis & model
- D. Domain asuransi: istilah & driver churn yang umum
- E. Cheat-sheet statistik (uji, effect size, cara menulis)
- F. Library strategi retensi (driver → aksi → KPI)
- G. Persiapan pertanyaan juri
- H. Snippet pandas/matplotlib cepat (tanpa AI)
- I. Cara mencari bantuan tanpa AI

---

## A. Alur kerja saat lomba

```
Baca soal (5–10 mnt)
 ├─ Apa target? (churn/lapse/status) → nilai positif = churn?
 ├─ Metrik lomba? (AUC / F1 / accuracy / logloss) → CFG.METRIC & SUBMISSION_MODE
 ├─ Ada test + sample_submission? → format probability vs label
 ├─ Ada tabel tambahan (claims, payments)? → CFG.EXTRA_TABLES
 └─ Ada parameter bisnis (biaya, margin)? → CFG.PROFIT_MARGIN, RETENTION_COST, ...
        │
Run FAST mode (10–15 mnt) → pastikan tidak error, cek:
 ├─ Target mapping & churn rate masuk akal
 ├─ Role kolom (tenure, premium, ...) benar → kalau salah, CFG.COLUMN_ROLES
 ├─ Leakage screen → buang kolom post-event
 └─ Tipe kolom (FORCE_CATEGORICAL / FORCE_NUMERIC)
        │
Baca hasil EDA/driver/survival/segment → tulis draft "Findings" (sambil...)
        │
Run FULL mode (30–90 mnt, jalan di background) → Optuna, ensemble, SHAP, business
        │
Ambil figure + insights.md → tulis Business Impact & Recommendations
        │
Submit: validator ✅ → nama file → ZIP
```

**Prioritas kalau waktu habis:** submission valid > figure inti + rekomendasi > tuning.

---

## B. Jika X → Y: kondisi data

| Kondisi | Tindakan | Di notebook |
|---|---|---|
| Target berupa teks ("Yes/No", "Churn/Stay", "Attrited Customer") | auto-map; cek output "Mapping target" | `CFG.POSITIVE_LABEL` |
| Target 3+ kelas (Active/Lapsed/Surrendered) | binarisasi: churn = Lapsed + Surrendered | `CFG.POSITIVE_LABEL = ["Lapsed","Surrendered"]` |
| Kolom target bernama `is_active`/`retained` (1 = bertahan) | dibalik otomatis — **verifikasi** churn rate | `CFG.POSITIVE_LABEL` |
| Tidak ada kolom tenure tapi ada `start_date` | buat tenure = (ref_date − start_date) di `custom_feature_engineering`, set role | `CFG.COLUMN_ROLES={"tenure": ...}` |
| Ada `end_date`/`cancel_date` | **leakage** (hanya ada untuk churner) → buang; *boleh* dipakai untuk menghitung durasi survival churner | `CFG.DROP_COLS` |
| Data multi-tabel (customer, policy, claims, payments) | 1-to-1 → merge; 1-to-many → agregasi (count/sum/mean/recency) | `EXTRA_ONE_TO_ONE`, `EXTRA_TABLES` |
| Satu customer punya banyak polis (baris = polis) | tentukan unit analisis: polis atau customer; kalau customer → agregasi; kalau polis → `GROUP_COL = customer_id` | `CFG.GROUP_COL` |
| Angka tersimpan sebagai teks ("1.250.000", "Rp 5jt") | auto-konversi; kalau gagal (misal "5jt") → bersihkan manual di `custom_feature_engineering` | `CFG.FORCE_NUMERIC` |
| Kategori typo ("Jakarta", "jakarta ", "JKT") | case/spasi otomatis; sinonim ("JKT") → map manual | `df[c].replace({...})` |
| Missing value besar (> 40%) di satu kolom | jangan langsung drop: missingness bisa informatif (indikator otomatis) | — |
| Missing karena "tidak berlaku" (settlement days kosong krn tidak pernah klaim) | itu informasi, bukan error; GBDT handle native | — |
| Nilai mustahil (umur 999, premi negatif) | → NaN otomatis untuk role terdeteksi; kolom lain cek `quality_report` | `CFG.FIX_IMPOSSIBLE_VALUES` |
| Outlier ekstrem (premi sangat besar) | tree model robust; untuk LogReg signed-log otomatis; laporan pakai median | — |
| Duplikat baris | dibuang otomatis; duplikat dengan label beda = noise | `CFG.DROP_DUPLICATES` |
| Kolom high-cardinality (agent_id, kota 300+) | freq + target encoding in-fold; CatBoost native | `CFG.HIGH_CARD_THRESHOLD` |
| Data sangat kecil (< 1.000 baris) | `N_REPEATS = 3`, model sederhana (LogReg, CatBoost depth 4), hati-hati overfit | — |
| Data besar (> 200k) | fast mode dulu, kurangi model, `SHAP_SAMPLE` kecil | recipe (F) |
| Imbalance berat (churn < 5%) | metrik PR-AUC/F1, threshold tuning, `class_weight`; jangan percaya accuracy | `CFG.IMBALANCE` |
| Test tidak ada | notebook tetap jalan (analisis + CV) | otomatis |
| Train & test beda periode | adversarial validation; pertimbangkan CV berbasis waktu | Section 12 |
| Ada kolom teks (keluhan, catatan) | panjang teks / keyword flags di `custom_feature_engineering`; atau notebook NLP untuk embedding | `03_NLP/` |
| Ada data transaksi pembayaran per bulan | fitur: jumlah telat, rata-rata hari telat, tren 3 bulan terakhir vs sebelumnya, recency | `EXTRA_TABLES` + custom FE |

---

## C. Jika X → Y: hasil analisis & model

### C1. EDA & statistik
| Hasil | Interpretasi | Tindakan |
|---|---|---|
| p < 0.05 tapi effect size negligible | signifikan secara statistik tapi tidak penting secara praktis (efek n besar) | jangan jadikan temuan utama |
| IV > 0.5 / AUC univariat > 0.95 | hampir pasti leakage | cek arti kolom; buang |
| Churn rate level tertentu ekstrem tapi n < 30 | tidak stabil (CI lebar) | sebut dengan hati-hati / gabung level |
| Hubungan U-shape (umur muda & tua churn tinggi) | non-linear | pakai band (fe_age_band), jelaskan dua segmen |
| Arah OR multivariat berlawanan dengan univariat | confounding / Simpson's paradox | bahas! contoh: premi tinggi tampak protektif karena berkorelasi dengan tenure panjang |
| VIF > 10 | multikolinear | jangan tafsirkan koefisien LogReg terpisah; pilih satu |
| KM kurva bersilangan | asumsi proportional hazards dilanggar | sebut limitation; laporkan KM & log-rank saja untuk variabel itu |
| Hazard tertinggi di awal (0–12 bln) | early-life churn | rekomendasi onboarding |
| Hazard naik di bulan 12/24/36 | churn di momen renewal | rekomendasi renewal management |
| Median survival "not reached" | > 50% customer belum churn di rentang data | laporkan retention rate di 12/24/36 bulan |

### C2. Model
| Hasil | Interpretasi | Tindakan |
|---|---|---|
| Semua model ≈ dummy (AUC ~0.5) | bug: target salah, fitur kosong, atau memang tidak ada sinyal | cek mapping & fitur; kalau benar-benar lemah, fokus ke insight |
| AUC > 0.97 | leakage | Section 5.3 & shuffled test |
| Train AUC ≫ OOF AUC (gap > 0.1) | overfit | naikkan `min_child_samples`, `reg_lambda`, turunkan `num_leaves`/`depth`; Optuna |
| LogReg ≈ GBDT | hubungan cenderung linear | **bagus untuk laporan**: model sederhana & interpretable cukup |
| GBDT ≫ LogReg | ada interaksi/non-linearitas | jelaskan via SHAP dependence & segment rules |
| CV std besar | data kecil/noisy | repeats, jangan klaim beda kecil antar model |
| Tuned < default | noise/overfit tuning | pakai yang lebih baik di CV final (otomatis) |
| Ensemble ≈ best single (< 0.001) | model mirip | pakai single (lebih sederhana) — otomatis |
| Shuffled-target AUC > 0.55 | leakage di pipeline | cek fitur yang memakai target, target encoding |
| Adversarial AUC > 0.7 | drift train vs test | buang fitur penyebab drift yang tak bermakna; sebut limitation |
| LB (leaderboard) ≪ CV | format submission/ drift / leakage | cek probability vs label, urutan ID |
| Threshold optimal jauh dari 0.5 | normal untuk imbalanced | pakai threshold OOF untuk metrik label |
| Calibration curve di bawah diagonal | over-confident | kalibrasi (otomatis bila bantu) — penting untuk ROI |

### C3. Explainability & bisnis
| Hasil | Interpretasi | Tindakan |
|---|---|---|
| Driver teratas non-actionable (umur, region) | berguna untuk targeting | rekomendasi = siapa yang ditarget, bukan apa yang diubah |
| Driver actionable kuat di semua metode | temuan robust | jadikan rekomendasi #1 |
| SHAP & permutation beda ranking | fitur berkorelasi berbagi importance | laporkan per "family" (tenure, claims, ...) |
| Profit campaign negatif di semua k | biaya > nilai yang diselamatkan | intervensi murah (digital) untuk low value; mahal hanya Priority Save |
| What-if besar tapi fitur sulit diubah | potensi besar, implementasi mahal | tandai sebagai long-term |
| Persona silhouette rendah (< 0.2) | persona tidak terpisah tegas | sajikan sebagai "kecenderungan", bukan kelompok kaku |

---

## D. Domain asuransi

### D1. Istilah penting (pakai di laporan)
| Istilah | Arti |
|---|---|
| **Lapse** | polis berhenti karena premi tidak dibayar setelah masa tenggang (*grace period*) |
| **Surrender** | pemegang polis mengakhiri polis secara aktif & mengambil nilai tunai (life insurance) |
| **Churn / attrition** | customer berhenti (lapse, surrender, tidak renew, pindah ke kompetitor) |
| **Persistency ratio** | % polis yang masih aktif setelah periode tertentu (misal *13th-month persistency* = aktif di bulan ke-13). KPI utama retensi asuransi |
| **Retention rate** | 1 − churn rate dalam satu periode |
| **Renewal** | perpanjangan polis (umum di asuransi umum/kesehatan/kendaraan, tahunan) |
| **Premium (premi)** | harga polis yang dibayar periodik |
| **Sum insured / sum assured (UP)** | nilai pertanggungan maksimum |
| **Rider** | manfaat tambahan yang menempel pada polis utama |
| **Grace period** | masa tenggang pembayaran premi sebelum polis lapse (biasanya 30–60 hari) |
| **Free-look period** | masa pelajari polis (biasanya 14 hari) di mana nasabah boleh batal dengan refund |
| **Claim / claims experience** | pengajuan manfaat; pengalaman klaim (cepat, disetujui, transparan) sangat memengaruhi loyalitas |
| **Loss ratio** | klaim dibayar ÷ premi diterima |
| **Underwriting** | proses seleksi & penentuan premi berdasarkan risiko |
| **Bancassurance** | penjualan asuransi lewat bank |
| **Agency channel** | penjualan lewat agen |
| **Acquisition cost** | biaya akuisisi (komisi agen, marketing) — dipulihkan dari premi tahun-tahun awal → lapse dini sangat merugikan |
| **CLV (Customer Lifetime Value)** | nilai sekarang dari margin masa depan customer |
| **Price elasticity / price shock** | sensitivitas customer terhadap kenaikan premi saat renewal |

### D2. Driver churn yang umum di asuransi (literatur & praktik)
1. **Harga / kenaikan premi saat renewal** (price shock) — paling sering di asuransi umum & kesehatan.
2. **Pengalaman klaim** — klaim ditolak, proses lama, kurang transparan → churn setelah klaim.
3. **Kualitas layanan / keluhan** — keluhan tidak diselesaikan.
4. **Friksi pembayaran** — metode manual (transfer/tunai) & frekuensi bulanan → lebih sering lupa/telat → lapse.
5. **Tenure pendek** — tahun pertama paling rawan (belum merasakan value, mis-selling).
6. **Channel** — online/direct cenderung lebih price-sensitive; agen memberi relasi personal.
7. **Jumlah produk** — bundling menaikkan switching cost.
8. **Affordability** — rasio premi terhadap pendapatan tinggi → rawan lapse saat ekonomi sulit.
9. **Life events** — pindah, menikah, pensiun, kehilangan pekerjaan (sering tidak ada di data → limitation).
10. **Engagement** — customer yang tidak pernah login/berinteraksi lebih mudah pergi.

### D3. Kenapa churn mahal (untuk Introduction)
- Biaya akuisisi (komisi, marketing) baru tertutup setelah beberapa tahun premi → lapse dini = rugi.
- Customer lama cenderung lebih profitable (risiko lebih diketahui, cross-sell).
- Persistency adalah indikator kesehatan bisnis yang dipantau regulator & manajemen.

---

## E. Cheat-sheet statistik

### E1. Memilih uji
| Variabel X | Target churn (biner) | Uji | Effect size |
|---|---|---|---|
| Kategori | biner | **Chi-square** (n ekspektasi < 5 → Fisher exact) | **Cramér's V** |
| Numerik (tidak normal) | biner | **Mann-Whitney U** | **rank-biserial r** (= 2·AUC − 1) |
| Numerik (≈ normal) | biner | Welch t-test | Cohen's d |
| Waktu sampai churn | event | **Log-rank test** (antar grup KM) | hazard ratio (Cox) |
| Banyak variabel sekaligus | biner | **Logistic regression** | odds ratio (+95% CI) |
| Banyak variabel + waktu | event | **Cox PH** | hazard ratio |
| Banyak uji sekaligus | — | koreksi **Benjamini-Hochberg (FDR)** | q-value |

### E2. Ambang effect size
| Ukuran | Kecil | Sedang | Besar |
|---|---|---|---|
| Cramér's V (df=1) | 0.1 | 0.3 | 0.5 |
| rank-biserial r / Cohen's d | 0.1 / 0.2 | 0.3 / 0.5 | 0.5 / 0.8 |
| Information Value | 0.02–0.1 lemah | 0.1–0.3 sedang | 0.3–0.5 kuat (>0.5 curiga) |
| Odds/Hazard ratio | 1.2–1.5 (atau 0.67–0.83) | 1.5–2.5 | > 2.5 (atau < 0.4) |
| ROC-AUC model | 0.6–0.7 lemah | 0.7–0.8 cukup baik | > 0.8 baik (> 0.95 curiga leak) |
| KS statistic | 0.2–0.3 | 0.3–0.4 | > 0.4 |

### E3. Cara menulis hasil uji (English)
- Chi-square: *"Churn differed significantly by payment method, χ²(3, N = 8,000) = 127.4, p < .001, Cramér's V = 0.13."*
- Mann-Whitney: *"Churned customers experienced larger premium increases (median 6.2% vs 3.5%; U = …, p < .001, r = 0.22)."*
- Odds ratio: *"…associated with 2.1 times higher odds of churn (OR = 2.12, 95% CI 1.81–2.49, p < .001)."*
- Hazard ratio: *"Auto-renewal reduced the instantaneous churn risk by 36% (HR = 0.64, 95% CI 0.58–0.71)."*
- Log-rank: *"Survival curves differed significantly across payment methods (log-rank χ² = 105.0, p < .001)."*
- **Selalu:** "associated with", bukan "causes".

### E4. Kesalahan umum yang dihindari
- Menyimpulkan kausalitas dari korelasi.
- Melaporkan accuracy untuk data imbalanced.
- Mengevaluasi model di data training.
- Target encoding / scaling di-fit di seluruh data sebelum split (leakage).
- Memakai fitur post-churn.
- Banyak uji tanpa koreksi multiple testing.

---

## F. Library strategi retensi (driver → aksi → KPI)

| Driver | Aksi spesifik | Segmen target | KPI |
|---|---|---|---|
| Metode bayar manual | Insentif auto-debit (diskon kecil/cashback), enrolment 1 klik, reminder H-7/H-1 | manual payers, tier High/Medium | % auto-pay, lapse rate converted vs control |
| Tidak auto-renew | Default auto-renew + opt-out, reminder 30/14/7 hari, renew 1 klik | renewal dalam 60 hari | renewal rate |
| Kenaikan premi | Cap/phase-in kenaikan untuk loyal & at-risk, jelaskan value, tawarkan penyesuaian coverage/deductible | kenaikan > X% & tier High | churn customer dengan kenaikan; elastisitas |
| Keluhan | Callback ≤ 48 jam, SLA resolusi, service recovery voucher, root-cause fixing | customer dengan keluhan 12 bln | waktu resolusi, churn complainants |
| Klaim ditolak / lama | Fast-track, penjelasan transparan + jalur banding, claims concierge untuk high-value | pasca-klaim | settlement days, NPS klaim, churn pasca-klaim |
| Telat bayar | Telat pertama = trigger: pengingat ramah, cicilan, ganti tanggal bayar, outreach di grace period | late payers | cure rate, lapse setelah missed payment |
| Tenure pendek | Onboarding: welcome call, penjelasan polis, aktivasi app, check-in 90 hari, persiapan renewal pertama | tenure < 12 bln | 13th-month persistency |
| Produk tunggal | Bundling/rider dengan multi-policy discount | single-product, risiko baik | produk per customer |
| Engagement rendah | Fitur app/wellness, konten personal, reaktivasi saat aktivitas turun | dormant users | MAU, churn re-engaged |
| Channel online | Follow-up manusia, edukasi produk | online-acquired | persistency per channel |
| Channel agen | Insentif agen berbasis persistency, bukan hanya penjualan baru | agen dengan lapse tinggi | persistency per agen |
| Bayar bulanan | Diskon bayar tahunan/kuartalan | monthly payers | % annual payers |
| Affordability (premi/pendapatan tinggi) | Opsi downgrade coverage, cicilan, produk lebih terjangkau | rasio premi/pendapatan tinggi | lapse di segmen ini |
| (Semua) | **Early-warning system**: skor bulanan, routing ke tim retensi, A/B test | semua aktif | uplift retensi vs control |

**Prinsip:** intervensi mahal (call personal, diskon) → *Priority Save* (risk & value tinggi). Intervensi murah/otomatis (email, push, reminder) → *Low-cost Save*. *Nurture & Upsell* → loyalty & cross-sell, bukan diskon.

---

## G. Persiapan pertanyaan juri

| Pertanyaan | Jawaban inti |
|---|---|
| Kenapa ROC-AUC, bukan accuracy? | Data imbalanced; accuracy bisa tinggi dengan menebak "tidak churn" semua. AUC mengukur kemampuan ranking — sesuai kebutuhan bisnis memprioritaskan customer. |
| Bagaimana mencegah overfitting? | Stratified K-fold OOF, early stopping per fold, regularisasi, cek gap train-valid & learning curve, tuning di fold terpisah. |
| Bagaimana mencegah leakage? | Buang variabel post-event; target encoding di dalam fold; shuffled-target test (AUC ≈ 0.5); adversarial validation. |
| Apakah driver itu kausal? | Tidak bisa dipastikan dari data observasional; kami konsistensi-kan bukti dari beberapa metode dan merekomendasikan A/B test sebelum rollout. |
| Kenapa pakai survival analysis? | Churn adalah proses waktu; KM/Cox menangani customer yang belum churn (censored) dan menjawab *kapan* intervensi paling efektif. |
| Kenapa ensemble/GBDT, apa tidak black-box? | Kami pasangkan dengan logistic regression (odds ratio) dan SHAP untuk menjelaskan setiap prediksi; hasil konsisten. |
| Bagaimana memilih threshold? | Dioptimasi di OOF untuk metrik terkait, atau secara bisnis: target jika p × success × value > cost. |
| Asumsi ROI dari mana? | Asumsi eksplisit (success rate, biaya, margin) + sensitivity analysis menunjukkan kesimpulan tetap berlaku di rentang wajar. |
| Bagaimana implementasi? | Model di-score bulanan, customer dirutekan per tier/kuadran, dashboard KPI, retrain per kuartal, A/B test per kampanye. |
| Bagaimana dengan fairness (gender/umur)? | Variabel demografis dipakai untuk analisis; untuk keputusan perlakuan, fokus pada variabel perilaku/actionable dan pantau dampak antar kelompok. |
| Apa keterbatasan studi? | Snapshot (bukan panel), asosiasi bukan kausal, variabel penting mungkin tidak tersedia (life events, kompetitor), asumsi biaya. |

---

## H. Snippet cepat (tanpa AI)

```python
# Lihat data
df.shape; df.info(); df.describe(include="all").T; df.isna().mean().sort_values(ascending=False)
df["col"].value_counts(dropna=False, normalize=True)

# Churn rate per kategori
df.groupby("payment_method")["churn"].agg(["mean", "size"]).sort_values("mean", ascending=False)

# Churn rate per bin numerik
df.groupby(pd.qcut(df["tenure"], 5, duplicates="drop"))["churn"].mean()

# Pivot 2 arah
df.pivot_table(index="channel", columns="payment_method", values="churn", aggfunc="mean")

# Merge & agregasi tabel anak
agg = claims.groupby("customer_id").agg(n_claims=("claim_id", "count"), total_amount=("amount", "sum"),
                                        last_claim=("claim_date", "max")).reset_index()
df = df.merge(agg, on="customer_id", how="left")
df["n_claims"] = df["n_claims"].fillna(0)

# Tanggal
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce", dayfirst=True)
df["tenure_days"] = (pd.Timestamp("2025-06-30") - df["start_date"]).dt.days

# Mapping / ganti nilai
df["gender"] = df["gender"].str.strip().str.title().replace({"M": "Male", "F": "Female"})

# Chi-square & Mann-Whitney
from scipy import stats
ct = pd.crosstab(df["payment_method"], df["churn"]); chi2, p, dof, _ = stats.chi2_contingency(ct)
u, p = stats.mannwhitneyu(df.loc[df.churn == 1, "premium"], df.loc[df.churn == 0, "premium"])

# Bar chart churn rate
ax = df.groupby("payment_method")["churn"].mean().sort_values().plot.barh()
ax.set_xlabel("Churn rate"); plt.tight_layout(); plt.savefig("fig.png", dpi=300)
```

---

## I. Cara mencari bantuan tanpa AI
- Di Jupyter: `help(pd.merge)`, `pd.merge?` lalu Enter, atau **Shift+Tab** di dalam kurung fungsi untuk melihat parameter.
- `dir(objek)` untuk melihat method yang tersedia.
- Dokumentasi resmi (boleh dibuka): pandas.pydata.org/docs, scikit-learn.org/stable, lightgbm.readthedocs.io, xgboost.readthedocs.io, catboost.ai/docs, statsmodels.org, shap.readthedocs.io, optuna.readthedocs.io.
- Error message: baca **baris terakhir** traceback dulu (jenis error + pesan), lalu baris kode milik kita yang paling bawah. Cari pesan error di Stack Overflow.
- Troubleshooting table di akhir setiap notebook (Section 25 untuk notebook churn).
- Debug cepat: `print(X.shape, X.dtypes.value_counts())`, `X.isna().sum().sum()`, `np.isinf(X.select_dtypes("number")).sum().sum()`.

---

## J. Jenis data / case asuransi lain → notebook & konfigurasi

| Case / target di soal | Contoh kolom target | Notebook | Konfigurasi kunci | Analisis bisnis utama |
|---|---|---|---|---|
| Churn / lapse / non-renewal / surrender / attrition | `Churn`, `Exited`, `Status`, `is_active`, `lapse_flag` | `01_Churn_Insurance` | `TARGET_COL`, `POSITIVE_LABEL` (kalau multi-status) | driver, survival, retensi, ROI, causal |
| Status polis multi-kelas (Active / Lapsed / Surrendered / Paid-up) | `policy_status` | `01_Churn_Insurance` (biner otomatis: aktif vs lainnya) **dan** `02_Tabular` (multiclass) | `POSITIVE_LABEL=["Lapsed","Surrendered"]` | bandingkan driver lapse vs surrender (jalankan 2× dengan POSITIVE_LABEL berbeda) |
| Klaim terjadi / tidak (claim propensity) | `is_claim`, `OUTCOME`, `ClaimNb` | `01_Churn_Insurance` (event = klaim; analisis driver & survival tetap valid) atau `02_Tabular` | target hitungan → otomatis event = >0 | risk factor, segmentasi risiko untuk underwriting/pricing — ganti narasi "retention" menjadi "risk selection" |
| Fraud klaim | `fraud_reported` (Y/N) | `02_Tabular` (binary, metric PR-AUC/F1) + driver analysis dari `01` | `METRIC="pr_auc"` atau `"f1"`, threshold tuning | red-flag rules (segment tree), biaya investigasi vs fraud dicegah |
| Cross-sell / response campaign | `Response`, `TravelInsurance`, `CARAVAN` | `01_Churn_Insurance` (event = beli) atau `02_Tabular` | — | campaign ROI (benefit = premi produk baru) — ganti narasi |
| Besar klaim / severity (regresi) | `claim_amount`, `charges` | `02_Tabular` (TASK="regression", log1p target, RMSE/MAE) | `TARGET_TRANSFORM="log1p"` | driver biaya, segmen berbiaya tinggi |
| Frekuensi klaim (count) | `ClaimNb` + `Exposure` | `02_Tabular` regresi (target = ClaimNb/Exposure) atau event >0 di `01` | | pricing factors |
| Premi / CLV (regresi) | `premium`, `clv` | `02_Tabular` regresi | | value drivers |
| Segmentasi nasabah tanpa label | — | `06_Clustering_Segmentation` (+ RFM) | `OUTCOME_COL` = churn kalau ada | persona, prioritas |
| Data deret waktu (klaim/premi/lapse per bulan) | `lapse_count` per bulan | `05_Time_Series` | horizon & frekuensi | forecast lapse/claims, kapasitas |
| Teks keluhan / catatan klaim | `complaint_text` | `03_NLP` (klasifikasi topik/sentimen) → hasilnya jadi fitur di `01` | | topik keluhan pemicu churn |

**Kombinasi yang sering menang:** `06_Clustering` (persona) + `01_Churn` (driver, survival, causal, ROI) dalam satu laporan → segmentasi + prediksi + rekomendasi per segmen.

### Data multi-tabel (umum di asuransi)
```python
CFG.TRAIN_PATH = "./data/customer.csv"                         # tabel utama (1 baris / customer) + target
CFG.EXTRA_ONE_TO_ONE = {"demo": {"path": "./data/demographic.csv", "key": "individual_id"}}
CFG.EXTRA_TABLES = {"claims":   {"path": "./data/claims.csv",   "key": "individual_id", "date_col": "claim_date"},
                    "payments": {"path": "./data/payments.csv", "key": "individual_id", "date_col": "pay_date"}}
```
Kalau target ada di tabel terpisah (misal `termination.csv` berisi tanggal berhenti): buat target dulu di cell kecil sebelum notebook,
misal `cust["Churn"] = cust["individual_id"].isin(term["individual_id"]).astype(int)` lalu simpan sebagai train.csv. **Jangan** pakai tanggal berhenti sebagai fitur (leak).
