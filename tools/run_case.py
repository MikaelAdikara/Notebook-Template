"""
Headless runner for 01_Churn_Insurance/churn_insurance_master.ipynb.

Executes the notebook top-to-bottom (like "Restart & Run All") with a JSON config, keeps all cell
outputs inside the executed notebook (evidence of analysis for the ZIP), and prints a run summary.

Usage (from anywhere):
    python tools/run_case.py --config case_config.json
    python tools/run_case.py --config case_config.json --set RUN_MODE=fast --set USE_OPTUNA=false
    python tools/run_case.py --workdir final --set TRAIN_PATH=data/train.csv --set TEAM_NAME=Warkab

Config file = JSON object whose keys are CFG attribute names (see the CFG cell), e.g.
    {"RUN_MODE": "full", "TRAIN_PATH": "data/train.csv", "TEST_PATH": "data/test.csv",
     "TARGET_COL": "churn", "TEAM_NAME": "Warkab", "COMPANY_NAME": "PT Asuransi X"}
Lines starting with // are treated as comments.

Exit code: 0 = finished without section errors, 2 = finished with section errors, 1 = crashed.
"""
import argparse
import json
import os
import shutil
import sys
import time

for _st in (sys.stdout, sys.stderr):  # console Windows (cp1252) tidak bisa mencetak emoji → paksa UTF-8
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NB = os.path.join(os.path.dirname(HERE), "01_Churn_Insurance", "churn_insurance_master.ipynb")


def read_config(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        text = "\n".join(l for l in f.read().splitlines() if not l.strip().startswith("//"))
    return json.loads(text) if text.strip() else {}


def parse_value(v):
    low = v.strip().lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("none", "null"):
        return None
    try:
        return json.loads(v)
    except Exception:
        return v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="JSON config (CFG overrides)")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="extra CFG override (repeatable)")
    ap.add_argument("--notebook", default=DEFAULT_NB, help="master notebook to execute")
    ap.add_argument("--workdir", default=None, help="working folder (relative paths in config resolve here); default = config folder or cwd")
    ap.add_argument("--out-notebook", default=None, help="where to save the executed notebook (default <workdir>/<TEAM_NAME>_churn_analysis.ipynb)")
    ap.add_argument("--timeout", type=int, default=-1, help="per-cell timeout in seconds (-1 = none)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    cfg = read_config(args.config)
    for kv in args.set:
        if "=" not in kv:
            ap.error(f"--set expects KEY=VALUE, got {kv!r}")
        k, v = kv.split("=", 1)
        cfg[k.strip()] = parse_value(v)

    workdir = os.path.abspath(args.workdir or (os.path.dirname(os.path.abspath(args.config)) if args.config else os.getcwd()))
    os.makedirs(workdir, exist_ok=True)
    cfg_path = os.path.join(workdir, ".run_case_config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, default=str)

    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        print("nbclient/nbformat tidak ada → python -m pip install nbclient nbformat ipykernel")
        return 1

    team = str(cfg.get("TEAM_NAME", "TeamName")).replace(" ", "_")
    out_nb = os.path.abspath(args.out_notebook or os.path.join(workdir, f"{team}_churn_analysis.ipynb"))
    if os.path.abspath(args.notebook) != out_nb:
        shutil.copyfile(args.notebook, out_nb)
    cfg.setdefault("NOTEBOOK_PATH", out_nb)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, default=str)

    nb = nbformat.read(out_nb, as_version=4)
    env_backup = dict(os.environ)
    os.environ["CHURN_CONFIG"] = cfg_path
    os.environ["MPLBACKEND"] = "Agg"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["CHURN_REPO_DIR"] = os.path.dirname(HERE)   # → dashboard_template & dokumen repo
    # kernel must use THIS interpreter (avoid other Pythons on PATH)
    os.environ["PATH"] = os.path.dirname(sys.executable) + os.pathsep + os.environ.get("PATH", "")
    client = NotebookClient(nb, timeout=None if args.timeout < 0 else args.timeout, kernel_name="python3",
                            allow_errors=False, resources={"metadata": {"path": workdir}})
    t0 = time.time()
    status = 0
    print(f"▶ Executing {os.path.basename(out_nb)} in {workdir}")
    print(f"  config: {json.dumps(cfg, default=str)[:400]}")
    try:
        client.execute()
    except Exception as e:  # critical section failed → notebook stopped
        status = 1
        print(f"\n❌ Notebook stopped: {type(e).__name__}: {str(e)[-1500:]}")
    finally:
        nbformat.write(nb, out_nb)
        os.environ.clear()
        os.environ.update(env_backup)
    print(f"\n⏱  {time.time() - t0:,.0f}s | executed notebook saved → {out_nb}")

    out_dir = cfg.get("OUTPUT_DIR", "./outputs/churn_insurance")
    out_dir = out_dir if os.path.isabs(out_dir) else os.path.join(workdir, out_dir)
    summ = os.path.join(out_dir, "run_summary.json")
    if os.path.exists(summ):
        with open(summ, encoding="utf-8") as f:
            s = json.load(f)
        print(f"✅ final model: {s.get('final_model')} | OOF AUC {s.get('final_oof_auc', float('nan')):.4f} | "
              f"n_train {s.get('n_train')} | churn rate {s.get('churn_rate', float('nan')):.3f}")
        errs = s.get("section_errors") or {}
        if errs:
            print(f"⚠️  {len(errs)} section error(s):")
            for k, v in errs.items():
                print(f"   - {k}: {v[:300]}")
            status = status or 2
        else:
            print("✅ no section errors")
        for fn in ["REPORT_DRAFT.docx", "REPORT_DRAFT.pdf", "dashboard/index.html", "submission.csv"]:
            p = os.path.join(out_dir, fn)
            print(f"   {'✔' if os.path.exists(p) else '✘'} {fn}")
    elif status == 0:
        status = 1
        print("❌ run_summary.json tidak ditemukan")
    return status


if __name__ == "__main__":
    sys.exit(main())
