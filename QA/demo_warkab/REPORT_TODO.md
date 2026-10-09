# REPORT TODO — Warkab

Draft: `REPORT_DRAFT.docx` (judul: *Removing Payment Friction: Evidence-Based Churn Prevention for PT Asuransi Nusantara Sejahtera*). Isi utama ≈ 10 halaman (batas 10).

## A. Wajib

- [ ] Cover: anggota tim & universitas (sudah diisi).
- [ ] Konteks soal di Introduction (sudah dari CFG.CASE_CONTEXT).
- [ ] Jenis asuransi terdeteksi: **multi** → kalau salah set CFG.INSURANCE_LINE.
- [ ] Parameter bisnis (margin, biaya, success rate) sesuai soal; kalau soal tidak memberi → sudah ditulis sebagai asumsi + sensitivity.
- [ ] Pilih judul & framing di `NARRATIVE_OPTIONS.md` (judul alternatif, framing executive summary).
- [ ] Baca ulang seluruh teks: parafrase gaya tim, cek setiap angka sama dengan tabel.
- [ ] 0 penanda [EDIT] tersisa (highlight kuning).

## A2. Research yang dipakai (CASE_RESEARCH.xlsx)

- File: `<folder-demo>\CASE_RESEARCH.xlsx`
- Dipakai: case_facts = 2, industry_facts = 2, literature = 5, custom_paragraphs = 2, feature_labels = 17
- [ ] Semua baris industry_facts / literature sudah `verified = Y` (sumber dibuka & dicek).

## B. Verifikasi kualitas (juri)

- [ ] Mapping target benar (churn = 1); tidak ada kolom leak di model (Appendix A, leakage screen).
- [ ] Setiap driver yang dibahas konsisten di beberapa metode (Table 1 'methods agreeing').
- [ ] Klaim kausal hanya untuk efek dengan verdict 'robust' (Appendix H); lainnya ditulis 'associated with'.
- [ ] Rekomendasi: siapa (segmen + ukuran), apa, kapan, dampak, KPI, desain pilot.
- [ ] Persona diberi nama yang menarik (lihat NARRATIVE_OPTIONS.md).

## C. Format

- [ ] ≤ 10 halaman isi (cover & appendix tidak dihitung; referensi DIHITUNG).
- [ ] A4, TNR 12, spasi 1.15, margin 4/4/3/3 cm (sudah otomatis).
- [ ] Nama file: `Warkab_Final Stage 1.pdf`; ZIP `Warkab_Final Stage 1.zip` (cell 24.4).
