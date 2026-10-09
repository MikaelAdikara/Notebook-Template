# Download & instalasi di komputer lain (mis. komputer panitia)

Template ini tidak terikat ke satu laptop: semua path relatif, file `.bat` dibuat ulang di komputer tempat kamu menjalankan `new_case.py`, dan tidak ada data atau akun yang disimpan di dalamnya.

## 1. Download (±1 menit)

Pilih salah satu:

- **Zenodo (DOI)**: buka `https://doi.org/<DOI-ZENODO>` → bagian *Files* → **Download**.
- **GitHub Release**: halaman *Releases* repo → versi terbaru → **Source code (zip)**.

Ekstrak ZIP ke folder kerja, misalnya `D:\lomba\`. **Ganti nama folder hasil ekstrak menjadi `Notebook-Template`** (ZIP dari GitHub/Zenodo biasanya bernama `Notebook-Template-1.0.0` atau sejenisnya), supaya semua perintah di panduan cocok.

```
D:\lomba\
  Notebook-Template\      ← hasil ekstrak (sudah di-rename)
  case\                   ← nanti dibuat oleh new_case.py
```

Buka terminal (Command Prompt / PowerShell / Anaconda Prompt) di `D:\lomba\`.

## 2. Cek Python (±1 menit)

```
python --version
```

Butuh Python **3.9–3.12**. Kalau ada beberapa Python (mis. Anaconda + Python biasa), pakai satu yang sama untuk install **dan** menjalankan notebook. Selalu `python -m pip ...`, jangan `pip ...` polos.

## 3. Install paket (±5–10 menit, butuh internet)

```
python -m pip install -r Notebook-Template/requirements-churn.txt
```

`requirements-churn.txt` hanya berisi paket untuk template churn (lebih ringan dan lebih jarang gagal daripada `requirements.txt` yang ikut memasang paket NLP/computer vision).

Lalu cek: buka `Notebook-Template/00_Setup/00_environment_check.ipynb` → Restart & Run All → semua paket inti ✅. Notebook churn juga memasang otomatis paket yang belum ada saat dijalankan.

Kalau `pip install` gagal untuk satu paket:

| Paket gagal | Dampak | Tindakan |
|---|---|---|
| `catboost`, `xgboost` atau `lightgbm` | model itu dilewati otomatis, model lain tetap jalan | lanjut saja |
| `shap` | penjelasan SHAP dilewati; permutation importance tetap ada | lanjut saja |
| `lifelines` | sebagian analisis survival dilewati | lanjut saja |
| `interpret-core` | model EBM dilewati | lanjut saja |
| `python-docx` | artikel DOCX tidak dibuat | **wajib**, ulangi install |
| `nbclient`, `ipykernel` | `RUN_FAST/RUN_FULL.bat` tidak jalan | jalankan notebook manual di Jupyter (Restart & Run All) |

## 4. Mulai kerja

Ikuti `Notebook-Template/QA/ALUR_KERJA_HARI_H.md`. Langkah pertama:

```
python Notebook-Template/tools/new_case.py case --casebook "casebook.pdf" --team "NamaTim" --members "Nama 1;Nama 2"
```

`RUN_FAST.bat` / `RUN_FULL.bat` dibuat di folder `case/` dengan path Python komputer itu, jadi langsung bisa di-double-click.

## 5. Kalau komputer tidak punya MS Word

Artikel DOCX tetap dibuat. Hitung halaman & PDF memakai LibreOffice bila terpasang; kalau tidak ada keduanya, buka DOCX di aplikasi apa pun yang tersedia lalu *Save As PDF* manual dan cek sendiri jumlah halaman isi (≤ 10).

## 6. Rencana cadangan tanpa internet

Siapkan di laptop sendiri sebelum hari-H, lalu bawa di flashdisk:

1. ZIP template ini.
2. Paket Python offline. Sesuaikan versi Python & sistem operasi komputer panitia (tanyakan panitia bila bisa; contoh untuk Windows 64-bit, Python 3.11):

```
python -m pip download -r Notebook-Template/requirements-churn.txt -d wheels --only-binary=:all: --python-version 3.11 --platform win_amd64
```

Di komputer panitia:

```
python -m pip install --no-index --find-links wheels -r Notebook-Template/requirements-churn.txt
```

## 7. Latihan sekali sebelum hari-H

Di komputer lain (atau laptop teman), ulangi langkah 1–3 lalu:

```
python Notebook-Template/examples/mock_case_warkab/make_mock_case.py latihan
```

Double-click `latihan/RUN_FAST.bat`. Kalau selesai dengan "no section errors", template siap dipakai di komputer mana pun.
