# SENTUHAN MANUSIA — Warkab

Paper otomatis sudah lengkap dan bersih. Lima sentuhan di bawah ini yang membedakan paper bagus dari paper juara: suara aktuaria, cerita iterasi, ambang operasional, insight bisnis lokal dan kepatuhan guidebook. Setiap blok berisi **draf paragraf (English) yang angkanya sudah diisi dari run ini**; kamu tinggal mengganti bagian `[ISI DARI CASE: …]` dengan informasi dari casebook.

## Cara memasukkan ke paper (supaya tidak hilang saat run ulang)
1. Edit draf di bawah sampai tidak ada `[ISI …]` tersisa (hapus kalimat yang informasinya tidak ada di case — jangan mengarang angka).
2. Buka `CASE_RESEARCH.xlsx` → sheet `custom_paragraphs` → isi `use = Y`, `section` dan `position` sesuai yang tertulis di tiap blok, tempel teks ke kolom `text`.
3. Jalankan ulang cell **24.2c–24.5** (±3 menit) → paragraf masuk paper di tempatnya; autofit tetap menjaga ≤ 10 halaman.
4. Cek: `python QA/slop_check.py "<paper>.pdf"` (skor ≥ 80) dan `python QA/qa_check.py --case .`.

Aturan menulis: kalimat aktif dengan subjek 'we' / nama perusahaan, angka spesifik, tanpa em dash, tanpa 'crucial / robust / comprehensive / leverage', jangan memulai dengan 'Moreover / Furthermore'. Satu paragraf 2–4 kalimat sudah cukup.

## 1. Suara aktuaria (section `discussion`, position `end`)
**Cari di casebook:** biaya akuisisi / komisi per polis, target persistency perusahaan, asumsi lapse di pricing, porsi premi lanjutan (renewal) terhadap total premi, produk utama (unit link / tradisional / umum).

Draf:

> For PT Asuransi Nusantara Sejahtera, a 13-month persistency of 91.5% means that about 8.5% of new policies lapse before their first anniversary, usually before the acquisition cost of [ISI DARI CASE: biaya akuisisi/komisi per polis] is recovered. By month 25 persistency falls to 82.0%, so [ISI DARI CASE: asumsi persistency di pricing, mis. 85%] in the pricing basis is [lebih tinggi/lebih rendah] than experience and should be reviewed with the actuarial team. Weighted by premium, churn is 20.8% against 21.1% by headcount, which tells the pricing team whether the policies being lost are larger or smaller than average.

## 2. Cerita iterasi model dengan akar masalah (section `findings_model`, position `end`)
**Tidak perlu info dari case** — angka di bawah diambil dari experiment log; cukup tambahkan satu kalimat tentang hal yang mengejutkanmu.

Draf:

> We started from untuned models; the best, Logistic regression, reached ROC-AUC 0.757. Extra trees fitted the training folds far better than unseen folds (train AUC 1.000 vs out-of-fold 0.724), so model selection relied on out-of-fold accuracy, never on training accuracy. An ablation study showed that removing premium_change cost 0.033 AUC, which confirmed that this information group carries real signal rather than noise. Tuning, multi-seed averaging and ensemble selection lifted the final out-of-fold ROC-AUC to 0.760. [ISI: satu kalimat pengalaman tim, mis. 'Our first submission over-weighted X until we found Y in the residuals.']

## 3. Ambang operasional & governance (section `recommendations`, position `end`)
**Cari di casebook:** kanal yang bisa menghubungi nasabah (agen, call centre, aplikasi, bank partner), SLA layanan, struktur organisasi / siapa pengambil keputusan (Head of Retention, Chief Actuary, CFO, Direksi).

Draf:

> Operationally, a customer whose churn score exceeds 0.32 enters the High-risk tier (1,600 customers in the sample, actual churn 48.2%) and is routed to [ISI DARI CASE: kanal, mis. agen pemegang polis] within [ISI: SLA, mis. 7 hari] of scoring. The 'Priority Save' group (782 customers holding 29% of the value at risk) receives a personal call; other high-risk customers receive automated reminders through [ISI DARI CASE: aplikasi/SMS/email]. The score is re-validated every quarter and retrained when out-of-fold AUC falls below 0.73, when any feature's PSI exceeds 0.10 or when calibration drifts by more than five percentage points. Decisions escalate by size: [ISI DARI CASE: mis. Head of Retention] approves campaigns within budget, [ISI: mis. Chief Actuary] signs off pricing changes, and [ISI: mis. Direksi/Board] approves changes above [ISI: batas anggaran].

## 4. Insight bisnis lokal per driver (section `discussion`, position `start`)
Untuk setiap driver, tulis **satu kalimat kenapa driver itu masuk akal untuk perusahaan ini** memakai fakta casebook. Pertanyaan pemandu per tema:

- **premium change at last renewal (%)** (tema: price; kelompok berisiko: 13.2–30.6, churn 33.5%, 1.6× rata-rata).
  Pertanyaan: Bagaimana kebijakan kenaikan premi saat renewal? Ada inflasi medis / repricing produk? Apakah pesaing lebih murah?
  Draf: > At PT Asuransi Nusantara Sejahtera, the effect of premium change at last renewal (%) reflects [ISI DARI CASE: fakta/kebijakan perusahaan yang menjelaskan pola ini], so [ISI: tindakan yang paling masuk akal].
- **payment method** (tema: payment; kelompok berisiko: Bank Transfer, churn 25.5%, 1.2× rata-rata).
  Pertanyaan: Apakah perusahaan sudah punya auto-debit / virtual account / kerja sama bank? Berapa porsi nasabah yang masih bayar manual? Ada grace period berapa hari?
  Draf: > At PT Asuransi Nusantara Sejahtera, the effect of payment method reflects [ISI DARI CASE: fakta/kebijakan perusahaan yang menjelaskan pola ini], so [ISI: tindakan yang paling masuk akal].
- **auto-renewal** (tema: payment; kelompok berisiko: No, churn 26.4%, 1.3× rata-rata).
  Pertanyaan: Apakah perusahaan sudah punya auto-debit / virtual account / kerja sama bank? Berapa porsi nasabah yang masih bayar manual? Ada grace period berapa hari?
  Draf: > At PT Asuransi Nusantara Sejahtera, the effect of auto-renewal reflects [ISI DARI CASE: fakta/kebijakan perusahaan yang menjelaskan pola ini], so [ISI: tindakan yang paling masuk akal].
- **complaints in the last 12 months** (tema: service; kelompok berisiko: ≥2, churn 44.3%, 2.1× rata-rata).
  Pertanyaan: Berapa SLA klaim dan penanganan keluhan? Ada masalah klaim yang disebut di casebook?
  Draf: > At PT Asuransi Nusantara Sejahtera, the effect of complaints in the last 12 months reflects [ISI DARI CASE: fakta/kebijakan perusahaan yang menjelaskan pola ini], so [ISI: tindakan yang paling masuk akal].

## 5. Kepatuhan guidebook (cek di hari-H, sebelum Save As PDF)
- [ ] **Bahasa**: wajib Bahasa Indonesia? → terjemahkan di Word (struktur, angka, sitasi, nomor figure/tabel tetap).
- [ ] **Lembar orisinalitas / deklarasi penggunaan AI** diminta? → sisipkan setelah cover (template di bawah).
- [ ] Batas halaman, font, spasi, margin, nama file `<Tim>_Final Stage 1` sesuai guidebook terbaru.
- [ ] Apakah daftar pustaka dihitung dalam batas halaman? (`REFERENCES_COUNT_IN_LIMIT`).
- [ ] Lampiran yang diminta (notebook, data hasil, dashboard) sudah ada di ZIP.

Template deklarasi AI (Bahasa Indonesia, sesuaikan dengan aturan lomba):

> Kami, Tim Warkab (Anggota 1, Anggota 2), menyatakan bahwa laporan ini merupakan karya orisinal dan belum pernah diikutsertakan dalam perlombaan lain. Kami menggunakan kecerdasan buatan generatif [ISI: nama model] untuk [ISI: mis. penyusunan draf narasi, pengecekan tata bahasa dan peringkasan literatur]. Seluruh analisis data, pemodelan, interpretasi hasil dan rekomendasi telah ditinjau, diverifikasi dan menjadi tanggung jawab tim.

