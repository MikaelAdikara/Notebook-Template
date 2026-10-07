# Cheat-sheet: Metrik, Model, Validasi (semua jenis soal)

## 1. Pilih template
| Jenis data / soal | Template |
|---|---|
| Churn / retensi / lapse / attrition (biner) + butuh insight bisnis | `01_Churn_Insurance/churn_insurance_master.ipynb` |
| Tabular lain: klasifikasi biner/multikelas, regresi | `02_Tabular/tabular_master.ipynb` |
| Teks → kelas / skor | `03_NLP/nlp_classification.ipynb`, `03_NLP/nlp_regression.ipynb` |
| Gambar → kelas | `04_Computer_Vision/cv_image_classification.ipynb` (+ `CV_OTHER_TASKS_GUIDE.md` untuk deteksi/segmentasi) |
| Data berurutan waktu → prediksi masa depan | `05_Time_Series/time_series_forecasting.ipynb` |
| Tanpa target, butuh segmentasi customer | `06_Clustering_Segmentation/clustering_segmentation.ipynb` |

> Soal campuran (misal churn + teks keluhan) → pakai churn notebook, ekstrak fitur teks sederhana di `custom_feature_engineering` (panjang teks, keyword flags), atau buat embedding dengan notebook NLP lalu merge.

## 2. Metrik
### Klasifikasi
| Metrik | Kapan dipakai | Catatan |
|---|---|---|
| ROC-AUC | ranking, imbalanced ringan–sedang | tidak tergantung threshold |
| PR-AUC (average precision) | imbalanced berat, fokus kelas positif | baseline = prevalensi |
| LogLoss | butuh probabilitas akurat | sensitif terhadap over-confidence → kalibrasi |
| Brier | probabilitas | lebih mudah ditafsirkan dari logloss |
| Accuracy | kelas seimbang | menyesatkan kalau imbalanced |
| F1 / F-beta | trade-off precision-recall; F2 = recall lebih penting | **tuning threshold** wajib |
| Macro-F1 | multikelas, semua kelas sama penting | per-class bias tuning membantu |
| Balanced accuracy | imbalanced, label | rata-rata recall per kelas |
| MCC | imbalanced, label, satu angka seimbang | −1..1 |
| Cohen's kappa / QWK | label ordinal (rating) | QWK: optimasi threshold pembulatan |

### Regresi
| Metrik | Kapan | Catatan |
|---|---|---|
| RMSE | error besar sangat buruk | sensitif outlier |
| MAE | robust terhadap outlier | median-oriented |
| RMSLE | target skewed & positif (harga, jumlah) | latih di `log1p(y)` |
| MAPE / sMAPE / WAPE | error relatif (forecasting) | MAPE meledak saat y≈0 → pakai WAPE/sMAPE |
| R² | proporsi variansi terjelaskan | bisa negatif |
| MASE | forecasting antar-series | dibanding naive seasonal |

**Trik:** latih model sesuai metrik — RMSLE → target log1p; MAE → objective `l1`/`mae`; F1 → threshold tuning; QWK → regresi + threshold optimization.

## 3. Model per jenis data
| Data | Baseline cepat | Biasanya terkuat | Interpretasi |
|---|---|---|---|
| Tabular | LogReg/Ridge | **CatBoost/LightGBM/XGBoost** + ensemble | LogReg OR, SHAP |
| Tabular kecil (<2k) | LogReg, RF | CatBoost (depth kecil), ensemble sederhana | — |
| Teks pendek | TF-IDF + LogReg | Transformer fine-tune (IndoBERT/DeBERTa) | top n-gram LogReg |
| Teks + GPU lemah | TF-IDF + LinearSVC | sentence embedding + LogReg/LGBM | — |
| Gambar | frozen backbone + LogReg | fine-tune ConvNeXt/EfficientNet + TTA | Grad-CAM |
| Time series | seasonal naive | LightGBM global (lag/rolling) + ETS ensemble | feature importance |
| Clustering | KMeans (scaled) | GMM / HDBSCAN sesuai bentuk | profiling + surrogate tree |

## 4. Validasi
| Situasi | Skema CV |
|---|---|
| Klasifikasi biasa | StratifiedKFold (5) |
| Regresi | KFold / Stratified dengan target dibin |
| Ada grup (customer punya banyak baris, household, agen) | GroupKFold / StratifiedGroupKFold |
| Data waktu / test = periode setelah train | TimeSeriesSplit / backtest expanding window |
| Data kecil, skor bergoyang | Repeated K-fold (3×5) |

**Aturan emas:**
1. Semua yang "belajar dari data" (imputer, scaler, encoder, target encoding, feature selection, SMOTE) di-fit **di dalam fold train saja**.
2. Skor yang dilaporkan = **OOF**, bukan skor training.
3. Ensemble/threshold dioptimasi di OOF → sedikit optimis; pilih yang sederhana kalau beda tipis.
4. Adversarial validation untuk cek kemiripan train-test.
5. Shuffled-target test untuk cek pipeline bocor.

## 5. Diagnosis cepat
| Gejala | Kemungkinan | Aksi |
|---|---|---|
| Skor sangat tinggi tiba-tiba | leakage | cek fitur post-event, ID berurutan, duplikat train-test |
| Train ≫ valid | overfit | regularisasi, kurangi kompleksitas, early stopping |
| Train ≈ valid tapi rendah | underfit / fitur lemah | feature engineering, model lebih kuat |
| CV bagus, LB jelek | format submission / drift / CV salah | cek format, adversarial validation, skema CV |
| Skor beda jauh antar fold | data kecil / heterogen | repeated CV, group CV |
| Beda seed → beda jauh | variance tinggi | multi-seed averaging |

## 6. Hyperparameter penting (yang paling berpengaruh)
| Model | Parameter kunci | Arah kalau overfit |
|---|---|---|
| LightGBM | `num_leaves`, `min_child_samples`, `learning_rate`, `colsample_bytree`, `reg_lambda` | ↓ leaves, ↑ min_child, ↓ colsample, ↑ lambda |
| XGBoost | `max_depth`, `min_child_weight`, `eta`, `subsample`, `colsample_bytree`, `gamma` | ↓ depth, ↑ min_child_weight, ↑ gamma |
| CatBoost | `depth`, `l2_leaf_reg`, `learning_rate`, `random_strength` | ↓ depth, ↑ l2 |
| RandomForest | `min_samples_leaf`, `max_features`, `max_depth` | ↑ min_samples_leaf |
| LogReg | `C` (invers regularisasi) | ↓ C |
| Transformer | `lr` (1e-5–5e-5), epochs (2–5), `max_len`, batch | ↓ lr/epochs, ↑ dropout/weight decay |

Selalu: `learning_rate` kecil + early stopping + `n_estimators` besar.
