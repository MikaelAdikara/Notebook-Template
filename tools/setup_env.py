"""
Setup aman untuk komputer lain (mis. komputer panitia): semua paket dipasang ke virtual environment `.venv`
di folder kerja (sebelah folder Notebook-Template). Tidak butuh hak admin, tidak mengubah Python/paket milik komputer itu,
dan bisa dibersihkan total dengan menghapus folder `.venv`.

    python Notebook-Template/tools/setup_env.py                    → buat .venv + install requirements-churn.txt + uji import
    python Notebook-Template/tools/setup_env.py --wheels D:/wheels → install offline dari folder wheel (tanpa internet)
    python Notebook-Template/tools/setup_env.py --check            → hanya uji paket di .venv yang sudah ada

Setelah selesai, pakai Python dari .venv untuk semua perintah (SETUP.bat menuliskan perintahnya), atau double-click
START_JUPYTER.bat untuk membuka Jupyter dengan environment ini.
"""
import argparse
import os
import platform
import subprocess
import sys
import time

for _st in (sys.stdout, sys.stderr):
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WORK = os.path.dirname(REPO)                      # folder kerja = induk Notebook-Template
VENV = os.path.join(WORK, ".venv")
REQ = os.path.join(REPO, "requirements-churn.txt")
CONS = os.path.join(REPO, "constraints-tested.txt")
WIN = os.name == "nt"
VPY = os.path.join(VENV, "Scripts" if WIN else "bin", "python.exe" if WIN else "python")

# modul → wajib? (wajib = tanpa ini artikel/notebook tidak bisa dibuat)
CHECK = [("numpy", True), ("pandas", True), ("sklearn", True), ("scipy", True), ("matplotlib", True), ("seaborn", True),
         ("openpyxl", True), ("docx", True), ("nbclient", True), ("nbformat", True), ("ipykernel", True),
         ("lightgbm", False), ("xgboost", False), ("catboost", False), ("statsmodels", False), ("optuna", False),
         ("shap", False), ("lifelines", False), ("interpret", False), ("imblearn", False), ("fitz", False), ("tabulate", False)]


def run(cmd, **kw):
    print("  $", " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd))
    return subprocess.call(cmd, **kw)


def check_packages(py):
    code = ("import importlib, json, sys\n"
            f"mods = {[m for m, _ in CHECK]!r}\n"
            "out = {}\n"
            "for m in mods:\n"
            "    try:\n"
            "        mod = importlib.import_module(m); out[m] = getattr(mod, '__version__', 'ok')\n"
            "    except Exception as e:\n"
            "        out[m] = 'ERROR: ' + str(e)[:80]\n"
            "print(json.dumps(out))\n")
    r = subprocess.run([py, "-c", code], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:])
        return False
    import json
    res = json.loads(r.stdout.strip().splitlines()[-1])
    ok_required = True
    for m, req in CHECK:
        v = res.get(m, "?")
        bad = str(v).startswith("ERROR")
        mark = "✘" if bad else "✔"
        note = (" ← WAJIB, ulangi setup" if req else " ← opsional, analisis terkait dilewati otomatis") if bad else ""
        print(f"   {mark} {m:<12} {v}{note}")
        if bad and req:
            ok_required = False
    return ok_required


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wheels", default=None, help="folder berisi file .whl untuk install offline")
    ap.add_argument("--check", action="store_true", help="hanya cek paket di .venv")
    ap.add_argument("--latest", action="store_true", help="abaikan constraints-tested.txt, pasang versi terbaru")
    a = ap.parse_args()
    t0 = time.time()
    v = sys.version_info
    print(f"Python dasar : {sys.version.split()[0]} ({sys.executable})")
    print(f"Sistem       : {platform.platform()}")
    print(f"Folder kerja : {WORK}")
    print(f"Environment  : {VENV}  (terisolasi; hapus folder ini untuk membersihkan)")
    if v < (3, 9):
        print("❌ Python terlalu lama (butuh 3.9–3.12). Minta panitia Python yang lebih baru atau pakai Anaconda.")
        return 1
    if v >= (3, 13):
        print("⚠️ Python 3.13+: beberapa paket (mis. catboost) mungkin belum punya versi siap pakai; setup tetap dicoba, "
              "paket opsional yang gagal akan dilewati otomatis oleh notebook.")

    if not a.check:
        if not os.path.exists(VPY):
            print("\n[1/3] Membuat virtual environment ...")
            if run([sys.executable, "-m", "venv", VENV]) != 0 or not os.path.exists(VPY):
                print("❌ Gagal membuat venv. Di Linux pasang paket python3-venv; di Windows pastikan Python dari python.org/Anaconda.")
                return 1
        else:
            print("\n[1/3] Virtual environment sudah ada → dipakai ulang")
        print("\n[2/3] Memasang paket (±5–10 menit dengan internet) ...")
        if a.wheels:
            cmd = [VPY, "-m", "pip", "install", "--no-index", "--find-links", a.wheels, "-r", REQ]
            rc = run(cmd)
        else:
            run([VPY, "-m", "pip", "install", "-q", "--upgrade", "pip"])
            rc = 1
            if os.path.exists(CONS) and not a.latest:
                print("   → memakai versi yang sudah teruji (constraints-tested.txt) ...")
                rc = run([VPY, "-m", "pip", "install", "-r", REQ, "-c", CONS])
                if rc != 0:
                    print("   → versi teruji tidak tersedia untuk Python/OS ini → memakai versi terbaru")
            if rc != 0:
                rc = run([VPY, "-m", "pip", "install", "-r", REQ])
        if rc != 0:
            print("⚠️ Sebagian paket gagal dipasang; dicoba satu per satu supaya paket lain tetap terpasang ...")
            for line in open(REQ, encoding="utf-8"):
                pkg = line.split("#")[0].strip()
                if pkg:
                    extra = ["--no-index", "--find-links", a.wheels] if a.wheels else []
                    run([VPY, "-m", "pip", "install", "-q", *extra, pkg])
    print("\n[3/3] Uji import paket di environment ...")
    if not os.path.exists(VPY):
        print("❌ .venv belum ada → jalankan tanpa --check")
        return 1
    ok = check_packages(VPY)
    print(f"\n⏱  {time.time() - t0:,.0f}s")
    rel = os.path.relpath(VPY, WORK)
    if ok:
        print("✅ SETUP SELESAI. Semua paket wajib terpasang di environment terisolasi.\n")
        print("Langkah berikut (jalankan dari folder kerja):")
        print(f'   {rel} Notebook-Template/tools/new_case.py case --casebook "soal.pdf" --members "Nama 1;Nama 2"')
        print("   → lalu ikuti Notebook-Template/QA/ALUR_KERJA_HARI_H.md (RUN_FAST.bat / RUN_FULL.bat otomatis memakai environment ini)")
        print("   → membuka notebook di Jupyter: double-click START_JUPYTER.bat")
        return 0
    print("❌ Ada paket WAJIB yang gagal. Cek koneksi internet / proxy, lalu jalankan SETUP.bat lagi "
          "(atau pakai --wheels untuk install offline).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
