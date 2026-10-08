"""
Siapkan folder kerja untuk case baru (hari H) dalam 1 perintah.

    python tools/new_case.py ../case            # buat folder ../case
    python tools/new_case.py ../case --team Warkab

Isi folder yang dibuat:
    data/                     ← taruh file dari panitia di sini
    case_config.json          ← isi dari soal (atau pakai CASE_INTAKE.html → Download JSON → timpa file ini)
    CASE_INTAKE.html          ← form pengisian config (buka di browser, offline)
    RUN_FAST.bat / RUN_FULL.bat (Windows) dan run_fast.sh / run_full.sh (Mac/Linux)
    NEXT_STEPS.md
"""
import argparse
import json
import os
import shutil
import sys

for _st in (sys.stdout, sys.stderr):  # console Windows (cp1252) tidak bisa mencetak emoji → paksa UTF-8
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--team", default="TeamName")
    a = ap.parse_args()
    d = os.path.abspath(a.folder)
    os.makedirs(os.path.join(d, "data"), exist_ok=True)
    with open(os.path.join(HERE, "case_config.example.json"), encoding="utf-8") as f:
        txt = "\n".join(l for l in f.read().splitlines() if not l.strip().startswith("//"))
    cfg = json.loads(txt)
    cfg["TEAM_NAME"] = a.team
    cfg_path = os.path.join(d, "case_config.json")
    if os.path.exists(cfg_path):
        print("case_config.json sudah ada → tidak ditimpa")
    else:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    shutil.copyfile(os.path.join(HERE, "CASE_INTAKE.html"), os.path.join(d, "CASE_INTAKE.html"))
    runner = os.path.join(HERE, "run_case.py")
    py = sys.executable
    for mode in ["fast", "full"]:
        with open(os.path.join(d, f"RUN_{mode.upper()}.bat"), "w", encoding="utf-8") as f:
            f.write(f'@echo off\r\nchcp 65001 >nul\r\nset PYTHONIOENCODING=utf-8\r\ncd /d "%~dp0"\r\n"{py}" "{runner}" --config case_config.json'
                    + (" --set RUN_MODE=fast" if mode == "fast" else "") + "\r\npause\r\n")
        with open(os.path.join(d, f"run_{mode}.sh"), "w", encoding="utf-8", newline="\n") as f:
            f.write(f'#!/bin/bash\ncd "$(dirname "$0")"\npython "{runner}" --config case_config.json' + (" --set RUN_MODE=fast" if mode == "fast" else "") + "\n")
    steps = f"""# Next steps — {a.team}

1. Copy semua file data dari panitia ke `data/`.
2. Buka `CASE_INTAKE.html` → isi dari soal → **Download JSON** → simpan sebagai `case_config.json` di folder ini (timpa).
   (Atau edit `case_config.json` langsung.)
3. Double-click **RUN_FAST.bat** (±5–10 menit) → cek `outputs/churn_insurance/run_summary.json` & `REPORT_TODO.md`:
   target/ID benar? churn rate masuk akal? tidak ada section error?
4. Double-click **RUN_FULL.bat** (±30–90 menit; jalan di background).
5. Hasil di `outputs/churn_insurance/`:
   - `{a.team}_Final Stage 1.docx/.pdf` — artikel (≤10 halaman isi, appendix lengkap)
   - `NARRATIVE_OPTIONS.md` — alternatif judul/framing/nama persona/paragraf diskusi
   - `JUDGE_QA.md` — persiapan pertanyaan juri
   - `dashboard/` — buka `index.html`; deploy: `cd outputs/churn_insurance/dashboard` lalu `npx vercel --prod`
   - `submission.csv`, `tables/`, `figures/`, `report_tables.xlsx`, `model_card.md`
   - `{a.team}_churn_analysis.ipynb` (di folder ini) — notebook ter-eksekusi lengkap dengan output (bukti analisis)
6. Edit artikel di Word (parafrase, pilih narasi) → Save As PDF `{a.team}_Final Stage 1.pdf`.
7. ZIP pengumpulan: `python "{os.path.join(HERE, 'make_zip.py')}" --case . --pdf "{a.team}_Final Stage 1.pdf"`
   (PDF final hasil edit kamu; tanpa --pdf → pakai draft otomatis).

Panduan lengkap: {os.path.join(REPO, '01_Churn_Insurance', '00_MULAI_DI_SINI.md')}
"""
    with open(os.path.join(d, "NEXT_STEPS.md"), "w", encoding="utf-8") as f:
        f.write(steps)
    print(f"✅ Folder case siap: {d}")
    print(steps)


if __name__ == "__main__":
    main()
