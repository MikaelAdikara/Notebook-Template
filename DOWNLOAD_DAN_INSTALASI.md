# Download & instalasi di komputer lain (mis. komputer panitia)

Setup ini **aman untuk komputer milik orang lain**:
- semua paket dipasang ke environment terisolasi `.venv` di folder kerja kamu;
- tidak butuh hak admin;
- tidak mengubah Python atau paket milik komputer itu;
- tidak menyimpan data atau akun.

Untuk membersihkan setelah lomba, cukup hapus folder kerja (termasuk `.venv`).

## 1. Download (±1 menit)

Pilih salah satu:
- **Zenodo (DOI)**: `https://doi.org/<DOI-ZENODO>` → *Files* → **Download**.
- **GitHub Release**: halaman *Releases* repo → versi terbaru → **Source code (zip)**.

Ekstrak ke folder kerja, misalnya `D:\lomba\`. **Ganti nama folder hasil ekstrak menjadi `Notebook-Template`**, karena ZIP dari GitHub/Zenodo biasanya bernama `Notebook-Template-1.0.0` atau sejenisnya.

```
D:\lomba\
  Notebook-Template\      ← hasil ekstrak (sudah di-rename)
  .venv\                  ← dibuat SETUP.bat (environment terisolasi)
  case\                   ← dibuat new_case.py
```

## 2. Setup (±5–10 menit, butuh internet): double-click `Notebook-Template\SETUP.bat`

SETUP akan:
1. mencari Python di komputer (`py` launcher atau `python`), butuh versi 3.9–3.12;
2. membuat `D:\lomba\.venv`;
3. memasang paket dari `requirements-churn.txt` ke environment itu, **memakai versi yang sudah teruji** (`constraints-tested.txt`). Kalau versi itu tidak tersedia untuk Python di komputer tersebut, SETUP otomatis memakai versi terbaru, yang juga sudah diuji; kalau ada paket yang gagal, dicoba satu per satu;
4. menguji import setiap paket, lalu menampilkan perintah langkah berikutnya.

Hasilnya harus **"✅ SETUP SELESAI"**. Paket bertanda "opsional" yang gagal tidak masalah, karena notebook otomatis melewati analisis yang membutuhkannya.

Tanpa double-click (atau di Linux/macOS):

```
python Notebook-Template/tools/setup_env.py
```

Di Linux/macOS juga bisa memakai `bash Notebook-Template/setup_env.sh`.

## 3. Mulai kerja

Jalankan dari folder kerja `D:\lomba\`, memakai Python dari `.venv`:

```
.venv\Scripts\python Notebook-Template\tools\new_case.py case --casebook "casebook.pdf" --team "NamaTim" --members "Nama 1;Nama 2"
```

- `case\RUN_FAST.bat` dan `case\RUN_FULL.bat` otomatis memakai `.venv`, jadi tinggal double-click.
- Untuk membuka notebook di Jupyter, double-click `Notebook-Template\START_JUPYTER.bat`.

Lanjutkan dengan `Notebook-Template\QA\ALUR_KERJA_HARI_H.md`.

## 4. Kalau ada masalah

| Masalah | Solusi |
|---|---|
| "Python tidak ditemukan" | Minta panitia Python 3.9–3.12 atau Anaconda. Kalau ada Anaconda, jalankan perintah di bagian 2 dari *Anaconda Prompt*. |
| Python 3.13+ | SETUP tetap mencoba; paket opsional yang belum mendukung versi itu dilewati otomatis. |
| Internet lambat / diblokir proxy | Pakai rencana cadangan offline (bagian 6). |
| Paket **wajib** gagal | Jalankan SETUP.bat lagi (aman diulang). Kalau tetap gagal, jalankan notebook di Jupyter bawaan komputer; notebook memasang paket yang kurang dengan `--user`, tanpa admin dan tanpa mengubah paket sistem. |
| Tidak ada MS Word | DOCX tetap dibuat; PDF memakai LibreOffice bila ada. Kalau tidak ada keduanya, *Save As PDF* manual dan cek sendiri jumlah halaman isi (≤ 10). |

## 5. Apa saja yang disentuh template di komputer itu
- `D:\lomba\` (folder kerja): `.venv`, `case\`, output analisis.
- Cache standar milik pengguna: cache pip dan matplotlib. Tidak ada perubahan sistem, registry, atau software lain.
- MS Word (kalau ada) dibuka di latar hanya untuk menghitung halaman dan membuat PDF, lalu ditutup kembali.

## 6. Rencana cadangan tanpa internet

Siapkan di laptop sendiri sebelum hari-H, lalu bawa di flashdisk:
1. ZIP template ini.
2. Paket Python offline, disesuaikan dengan versi Python dan sistem operasi komputer panitia (tanyakan panitia bila bisa). Contoh untuk Windows 64-bit, Python 3.11:

```
python -m pip download -r Notebook-Template/requirements-churn.txt -d wheels --only-binary=:all: --python-version 3.11 --platform win_amd64
```

Di komputer panitia:

```
python Notebook-Template/tools/setup_env.py --wheels D:\lomba\wheels
```

## 7. Latihan sekali sebelum hari-H

Di komputer lain (atau laptop teman), ulangi langkah 1–2, lalu jalankan dari `D:\lomba\`:

```
.venv\Scripts\python Notebook-Template\examples\mock_case_warkab\make_mock_case.py latihan
```

Double-click `latihan\RUN_FAST.bat`. Kalau selesai dengan "no section errors", template siap dipakai di komputer mana pun.
