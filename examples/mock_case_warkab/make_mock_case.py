"""
Siapkan contoh test case lengkap (fiktif) untuk tim Warkab di folder tujuan:
    python examples/mock_case_warkab/make_mock_case.py ../mock_case

Hasil: data/ (train, test, claims, sample_submission — sengaja berantakan), casebook.md, case_config.json (diisi dari casebook),
CASE_RESEARCH.xlsx (contoh temuan riset terverifikasi), RUN_FAST.bat / RUN_FULL.bat.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tools"))

for _st in (sys.stdout, sys.stderr):
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    dest = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "..", "mock_case"))
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "new_case.py"), dest, "--team", "Warkab"], check=True)
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "make_synthetic_insurance_churn.py"), "--out", os.path.join(dest, "data"),
                    "--n_train", "8000", "--n_test", "2000", "--seed", "2026"], check=True)
    truth = os.path.join(dest, "data", "_test_truth_DO_NOT_USE.csv")
    if os.path.exists(truth):
        shutil.move(truth, os.path.join(dest, "_test_truth_DO_NOT_USE.csv"))
    shutil.copyfile(os.path.join(HERE, "casebook.md"), os.path.join(dest, "casebook.md"))
    shutil.copyfile(os.path.join(HERE, "case_config.json"), os.path.join(dest, "case_config.json"))
    import research_helper
    research_helper.run(dest, os.path.join(dest, "casebook.md"))
    shutil.copyfile(os.path.join(HERE, "CASE_RESEARCH.xlsx"), os.path.join(dest, "CASE_RESEARCH.xlsx"))
    print(f"\n✅ Mock case siap di {dest}\n   → double-click RUN_FAST.bat / RUN_FULL.bat, atau:\n"
          f"   python \"{os.path.join(REPO, 'tools', 'run_case.py')}\" --config \"{os.path.join(dest, 'case_config.json')}\"")


if __name__ == "__main__":
    main()
