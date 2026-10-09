# RESEARCH KIT — dari casebook ke latar belakang, literatur & ringkasan yang "nempel" ke case

Tujuan: dalam **±90 menit** (paralel dengan full run notebook), tim menghasilkan fakta case, konteks industri, dan literatur yang **spesifik ke case dan ke temuan data**, lalu notebook menempelkannya ke artikel secara otomatis — tanpa perlu AI.

```
casebook.pdf ─► tools/research_helper.py ─► RESEARCH_PLAN.html (keyword + query siap-klik)
                         │                        │
                         ▼                        ▼  (kamu: cari, baca, verifikasi)
               CASE_RESEARCH.xlsx  ◄──────── isi temuan (fakta, literatur, paragraf, label)
                         │
                         ▼
     notebook cell 24.2c–24.5 ─► artikel: Introduction, Findings, Discussion, Recommendations, References
```

---

## 0. Yang dinilai juri dari bagian latar belakang & literatur

| Juri | Yang dicari | Cara memenuhinya dengan kit ini |
|---|---|---|
| Industri asuransi | paham konteks bisnis perusahaan & pasar (premi, persistensi, regulasi, biaya akuisisi) | `case_facts` + `industry_facts` (OJK/AAJI/AAUI) di Introduction |
| Praktisi data | masalah → metode → bukti → aksi; asumsi jelas | tujuan manajemen (`CASE_CONTEXT`), `CASE_QUESTIONS` jadi RQ, parameter bisnis dari soal |
| Akademik | literatur relevan, sitasi benar, temuan dikaitkan (setuju/berbeda) | sheet `literature` per tema → Discussion; referensi APA otomatis hanya yang disitasi |

Prinsip: **setiap kalimat eksternal punya sumber yang sudah dibuka & dicek**; lebih baik 8 referensi kuat yang benar-benar dipakai daripada 30 referensi tempelan.

---

## 1. Membaca casebook (15 menit) — protokol 3 kali baca

1. **Skim (3 menit):** judul, perusahaan, produk, tugas/pertanyaan, aturan, data. Tandai semua angka.
2. **Ekstraksi (8 menit):** isi tabel di bawah langsung ke `case_config.json` (atau `CASE_INTAKE.html`) dan sheet `case_facts`.
3. **Pemetaan (4 menit):** setiap tugas di soal → RQ → section laporan → output notebook (lihat `NARRATIVE_OPTIONS.md` §5).

| # | Cari di casebook | Contoh | Isi ke |
|---|---|---|---|
| 1 | Nama perusahaan, lini produk, pasar | "PT Asuransi Nusantara Sejahtera, multi-line" | `COMPANY_NAME`, `INSURANCE_LINE`, `MARKET` |
| 2 | Masalah utama + tren | "non-renewal naik 15,2% → 20,6%" | `CASE_CONTEXT` + `case_facts` |
| 3 | Tujuan manajemen | "retention programme 2026" | `MANAGEMENT_OBJECTIVE` |
| 4 | Tugas / pertanyaan | 4 tugas | `CASE_QUESTIONS` (EN, satu per baris) |
| 5 | Definisi churn & window | "not renewed or lapsed within window" | `CHURN_DEFINITION` |
| 6 | Periode & snapshot | "Jan 2022–Jun 2025, snapshot 30 Jun 2025" | `DATA_PERIOD`, `REFERENCE_DATE` |
| 7 | Metrik penilaian & format submission | ROC-AUC, probability | `METRIC`, `SUBMISSION_MODE` |
| 8 | Parameter bisnis | margin 20%, biaya Rp150.000, success 30% | `PROFIT_MARGIN`, `RETENTION_COST`, `RETENTION_SUCCESS_RATE`, `BUSINESS_PARAMS_SOURCE = "case"` |
| 9 | Budget | Rp1,5 miliar | `RETENTION_BUDGET` |
| 10 | Intervensi yang mungkin / rencana perusahaan | app baru, kerja sama auto-debit, bonus persistensi agen | `AVAILABLE_INTERVENTIONS` + `case_facts` |
| 11 | Biaya akuisisi / nilai nasabah | Rp1,1 juta per polis hilang | `case_facts` (dan pakai untuk argumen ROI) |
| 12 | Kamus data | arti kolom | sheet `feature_labels` |
| 13 | Kolom pasca-churn | `cancellation_reason` | `DROP_COLS` (notebook juga mendeteksi otomatis) |
| 14 | Tabel tambahan | claims.csv | `EXTRA_TABLES` |
| 15 | Aturan format | 10 halaman, referensi dihitung? | `REFERENCES_COUNT_IN_LIMIT` |

> `research_helper.py` sudah mengambil **kalimat berangka** dari casebook ke sheet `case_facts` (use = N). Kamu tinggal memilih (use = Y), merapikan ke bahasa artikel, dan memilih section.

---

## 2. Strategi keyword (bisa dipakai tanpa tool)

Bangun query dari **4 blok konsep** lalu gabungkan dengan AND; sinonim dalam blok digabung OR.

| Blok | EN | ID |
|---|---|---|
| Populasi | policyholder, insured, customer, insurer | pemegang polis, tertanggung, nasabah, perusahaan asuransi |
| Outcome | lapse, surrender, non-renewal, churn, persistency, retention, cancellation | lapse, penebusan polis (surrender), tidak diperpanjang, berhenti, persistensi, retensi, pembatalan |
| Konteks | life / motor / health / general insurance, emerging market, Indonesia | asuransi jiwa / kendaraan / kesehatan / umum, Indonesia |
| Driver / metode | payment method, premium increase, claims, complaints, agent, bancassurance, survival analysis, uplift | metode bayar, kenaikan premi, klaim, keluhan, agen, bancassurance |

Contoh:
- Google Scholar: `("lapse" OR "persistency" OR "non-renewal") AND insurance AND ("payment method" OR "premium payment frequency")` + filter *Since 2015*.
- Google Scholar per penulis kunci: `author:"M Eling" lapse` · `intitle:lapse intitle:insurance`.
- Regulator: `site:ojk.go.id statistik perasuransian filetype:pdf` · `site:aaji.or.id siaran pers` · `site:aaui.or.id kinerja`.
- Jurnal Indonesia: Garuda / SINTA — `lapse polis`, `persistensi polis`, `churn nasabah asuransi`.
- Buku: Google Books `customer churn insurance analytics` (kutip bab/halaman).

**Driver → tema → query**: `RESEARCH_PLAN.html` otomatis membuat query untuk tema driver yang muncul di data (setelah fast run, jalankan ulang `research_helper.py`).

---

## 3. Triage & verifikasi sumber (2 menit per sumber)

**Hierarki bukti:** casebook > regulator (OJK, BI, LPS, BPS) > asosiasi (AAJI, AAUI) > jurnal peer-review ber-DOI > buku akademik > laporan praktisi (Bain, McKinsey, Swiss Re, RGA, J.D. Power) > berita yang mengutip rilis resmi > blog (hindari).

Triage cepat: baca judul → abstrak → tabel hasil/kesimpulan. Pakai kalau: (a) outcome-nya lapse/churn/retensi, (b) konteks asuransi/jasa keuangan, (c) temuan bisa dikaitkan ke driver di data kita.

Checklist verifikasi (kolom `verified = Y` hanya kalau semua ✅):
- [ ] Sumber dibuka langsung (bukan cuplikan mesin pencari); angka dicek di halaman/tabel aslinya.
- [ ] Jurnal: DOI dibuka di https://doi.org/… → judul, penulis, tahun, volume(issue), halaman cocok. Jurnal Indonesia: cek peringkat SINTA; hindari jurnal predator.
- [ ] Berita: tanggal, media, dan pihak yang dikutip (mis. "menurut OJK"); angka regulator lebih baik dari dokumen resminya.
- [ ] Tahun data vs tahun publikasi dibedakan ("data 2024, dirilis 2025").
- [ ] Tidak ada klaim yang melampaui isi sumber (jangan menulis "menyebabkan" kalau sumbernya korelasional).

---

## 4. Sintesis: dari bacaan ke kalimat yang "nempel"

Pakai **matriks sintesis** (di kepala atau kertas) sebelum menulis:

| Driver di data kita | Sumber | Temuan sumber | Data kita | Kalimat |
|---|---|---|---|---|
| metode bayar | Hein et al. (2020) | frekuensi bayar memengaruhi lapse (Indonesia) | Cash churn 26% vs auto-debit 17% | Consistent with Hein et al. (2020), … |
| kenaikan premi | Guelman & Guillén (2014) | elastisitas harga saat renewal | kenaikan >12% → churn 32% | … |

Pola kalimat (EN):
- **Setuju:** "Consistent with [Author (Year)], who found [finding] in [context], customers [our finding with number]."
- **Berbeda:** "Contrary to [Author (Year)], [driver] shows little association with churn here (IV = 0.01), plausibly because [reason]."
- **Konteks case:** "This matters for [Company] because [case fact with number, e.g. acquisition cost of Rp1.1 million per lost policy]."
- **Implikasi:** "Therefore, [action] should target [segment] before [timing], measured by [KPI]."

Kalimat seperti ini ditulis di kolom `finding_EN` (sheet `literature`) **dalam bentuk umum** (temuan sumber + sitasi). Notebook menaruhnya di Discussion bila temanya muncul di data. Kalimat yang memakai angka data kita → tulis di `custom_paragraphs` (section `discussion`, `findings_drivers`, dst.) **setelah** full run, supaya angkanya final.

---

## 5. APA 7 — format cepat

| Jenis | Format | Dalam teks |
|---|---|---|
| Jurnal | Penulis, A. A., & Penulis, B. B. (Tahun). Judul artikel. *Nama Jurnal, vol*(issue), hlm–hlm. https://doi.org/xx | (Eling & Kochanski, 2013) / Eling dan Kochanski (2013) |
| ≥3 penulis | sebut semua (s.d. 20) di daftar | (Hein et al., 2020) |
| Buku | Penulis, A. (Tahun). *Judul buku* (ed.). Penerbit. | (Siddiqi, 2006) |
| Laporan lembaga | Lembaga. (Tahun). *Judul laporan*. URL | (Otoritas Jasa Keuangan, 2024) |
| Regulasi | Otoritas Jasa Keuangan. (Tahun). *Peraturan OJK Nomor … tentang …*. URL | (Otoritas Jasa Keuangan, 2022) |
| Berita tanpa penulis | Judul berita. (Tahun, Bulan Tanggal). *Media*. URL | ("Judul singkat," 2025) |
| Website | Penulis/Lembaga. (Tahun, Bulan Tanggal). *Judul halaman*. Situs. URL | (Lembaga, Tahun) |

Isi kolom `in_text_citation` persis seperti di teks (mis. `(Hein et al., 2020)`), dan `apa_reference` lengkap → notebook menambahkannya ke daftar pustaka **hanya kalau disitasi** di teks.

---

## 6. Mengisi `CASE_RESEARCH.xlsx`

| Sheet | Kolom | Contoh baris yang BAIK | Hindari |
|---|---|---|---|
| `case_facts` | use, section, statement_EN | Y · introduction · "Non-renewal at ANS rose from 15.2% in 2022 to 20.6% in 2024, and renewal premiums make up 58% of premium income." | menyalin paragraf soal mentah-mentah |
| `industry_facts` | use, section, statement_EN, in_text_citation, apa_reference, url, verified | Y · introduction · "Life insurers paid Rp62.72 trillion in surrender claims in 2025, 19% less than in 2024" · ("AAJI catat nilai klaim surrender," 2026) · [APA] · Y | angka tanpa sumber/tahun |
| `literature` | use, theme, finding_EN, in_text_citation, apa_reference | Y · payment · "Forgetting to pay explained 37.8% of recent life-insurance lapses (Gottlieb & Smetters, 2021)." | ringkasan abstrak panjang |
| `custom_paragraphs` | use, section, position, text | Y · recommendations · end · "Because ANS launches its app in Q1 2026, actions 1–3 should start as in-app nudges…" | paragraf > 120 kata (makan halaman) |
| `feature_labels` | column, label | `n_complaints_12m` → "complaints in the last 12 months" | — |

Section yang valid: `executive_summary, introduction, data, methodology, findings_drivers, findings_timing, findings_segments, findings_model, findings_explain, business, causal, personas, recommendations, discussion, limitations, conclusion`.
Tema literatur: `lifecycle, payment, price, service, affordability, relationship, channel, engagement, demographic, geography, general, methods` (`methods` → Appendix B).

Setelah diisi: tutup Excel → double-click **RUN_FULL.bat** lagi (atau RUN_FAST.bat kalau waktu mepet, ±10 menit). Kalau notebook sedang terbuka di Jupyter dan sudah di-Run All di sesi itu, cukup jalankan ulang cell 24.2c–24.5 (±3 menit) → cek `REPORT_TODO.md` bagian A2 (apa saja yang masuk) → cek halaman (autofit tetap menjaga ≤ 10 halaman).

---

## 7. "Resume" / Executive Summary yang maksimal

Executive Summary otomatis berstruktur **masalah (uang) → pendekatan → 4–5 temuan berangka → model → kampanye → efek kausal → 3 rekomendasi + pilot**. Supaya benar-benar "nempel" ke case:
1. Isi `CASE_CONTEXT` dengan bahasa manajemen di soal (nama program, target, tahun).
2. Tambah 1 `case_facts` section `executive_summary` (mis. biaya akuisisi per polis atau target 2026) → muncul di awal.
3. Tambah `custom_paragraphs` section `executive_summary` position `end`: 1–2 kalimat "so what" untuk direksi (mis. dampak terhadap target persistensi 2026).
4. Pilih framing dari `NARRATIVE_OPTIONS.md` §2 bila perlu menggeser penekanan (lifecycle / uang / driver / aksi).

Template kalimat "so what" (EN):
- "If the programme reduces churn among Priority Save customers by only [x] pp, it protects about [Rp …] of annual premium — [y]% of the 2026 retention budget."
- "The first 90 days of each policy should become the company's main retention battleground."

---

## 8. Timeline hari H (paralel dengan notebook)

| Menit | Notebook | Tim riset |
|---|---|---|
| 0–15 | `new_case.py`, isi intake, RUN_FAST | baca casebook (§1), `research_helper.py --casebook …` |
| 15–30 | cek fast run → RUN_FULL | jalankan ulang `research_helper.py` (query driver-spesifik), mulai cari (§2–3) |
| 30–90 | full run berjalan | isi `CASE_RESEARCH.xlsx` (§6), tulis 2–4 custom paragraph |
| 90–110 | double-click RUN_FULL.bat lagi (riset ikut masuk) | baca artikel, pilih narasi, parafrase |
| 110–130 | `make_zip.py` | latihan `JUDGE_QA.md` |

---

## 9. Daftar referensi siap pakai (sudah terverifikasi)
Lihat `BAHAN_LATAR_BELAKANG.md` §E — sudah tertanam di generator (dipakai otomatis bila relevan). Tambahan dari kit ini hanya untuk yang **spesifik case** (perusahaan, produk, regulasi terbaru, jurnal Indonesia yang relevan dengan driver di data).
