# Alur kerja Hari-H

Panduan langkah demi langkah dari download sampai upload ada di satu file: **`../MULAI_DI_SINI.md`** (root folder `Notebook-Template`).

Isinya, berurutan:
- A. persiapan komputer (SETUP.bat);
- B. siapkan case (new_case, data, form intake);
- C. run cepat untuk cek;
- D. riset & sentuhan manusia;
- E. run final;
- F. finalisasi paper di Word;
- G. ZIP, cek akhir, upload.

Bukti setiap langkah benar-benar berjalan: video `walkthrough_warkab/walkthrough_Warkab.mp4`, screenshot di `walkthrough_warkab/screens/`, dan `QA_FINAL_REPORT.md`.

## Latihan sebelum hari-H (sekali, ±40 menit)

Dari folder kerja, setelah SETUP selesai:

```
.venv\Scripts\python Notebook-Template\examples\mock_case_warkab\make_mock_case.py latihan
```

Double-click `latihan\RUN_FULL.bat`, lalu jalankan:

```
.venv\Scripts\python Notebook-Template\tools\make_zip.py --case latihan
.venv\Scripts\python Notebook-Template\QA\qa_check.py --case latihan
```

Rekam ulang walkthrough (opsional):

```
.venv\Scripts\python Notebook-Template\QA\make_walkthrough.py --case latihan --out rekaman --stress Notebook-Template\tools\STRESS_TEST_REPORT.md
```
