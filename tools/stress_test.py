"""
Stress test: run churn_insurance_master.ipynb on many deliberately different insurance-churn datasets and check
that every run finishes WITHOUT section errors and produces the report, dashboard and submission.

    python tools/stress_test.py --out stress_runs              # all variants (parallel 2)
    python tools/stress_test.py --out stress_runs --only tiny,panel --jobs 1

Variants cover: separators/encodings/Excel, no test file, multi-class & inverted targets, Indonesian column names,
no tenure/premium, date-only tenure, tiny / wide / panel data, float IDs, all-categorical, heavy missingness,
extreme imbalance, label-metric submissions, text columns, one-to-one + one-to-many extra tables, full mode on small data.
Result table → <out>/STRESS_TEST_REPORT.md
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_synthetic_insurance_churn import add_mess, make_claims, make_customers  # noqa: E402

for _st in (sys.stdout, sys.stderr):  # console Windows (cp1252) tidak bisa mencetak emoji → paksa UTF-8
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_CFG = {"RUN_MODE": "fast", "TEAM_NAME": "Stress", "REPORT_AUTOFIT": False, "MAKE_PDF": False, "FIG_DPI": 70,
            "TRAIN_PATH": "data/train.csv", "TEST_PATH": "data/test.csv", "SAMPLE_SUB_PATH": "data/sample_submission.csv",
            # ringan: fokus menguji robustness ingest & seluruh section (CatBoost/EBM/MLP diuji di varian 'baseline_claims' & 'full_mode_small')
            "MODELS": ["logreg", "hgb", "lgbm"], "N_BOOTSTRAP": 100, "ABLATION_MAX_GROUPS": 3, "CAUSAL_MAX_TREATMENTS": 2}


def base(n=3000, n_test=800, seed=0):
    rng = np.random.default_rng(seed)
    full, churn = make_customers(n + n_test, rng)
    claims = make_claims(full, rng)
    full = add_mess(full, rng)
    full["churn"] = np.where(churn == 1, "Yes", "No")
    return full.iloc[:n].copy(), full.iloc[n:].copy(), claims


def write(d, train, test=None, sub_col="churn", sub_val=0.5, id_col="customer_id", fmt="csv", sep=","):
    os.makedirs(os.path.join(d, "data"), exist_ok=True)
    if fmt == "xlsx":
        train.to_excel(os.path.join(d, "data", "train.xlsx"), index=False)
    else:
        train.to_csv(os.path.join(d, "data", "train.csv"), index=False, sep=sep)
    if test is not None:
        te = test.drop(columns=[c for c in [sub_col] if c in test.columns])
        if fmt == "xlsx":
            te.to_excel(os.path.join(d, "data", "test.xlsx"), index=False)
        else:
            te.to_csv(os.path.join(d, "data", "test.csv"), index=False, sep=sep)
        if id_col:
            pd.DataFrame({id_col: te[id_col], sub_col: sub_val}).to_csv(os.path.join(d, "data", "sample_submission.csv"), index=False)


def variants():
    V = {}

    def v(name, desc):
        def deco(fn):
            V[name] = (desc, fn)
            return fn
        return deco

    @v("baseline_claims", "messy synthetic + one-to-many claims table")
    def _(d):
        tr, te, cl = base()
        write(d, tr, te)
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        cl.to_csv(os.path.join(d, "data", "claims.csv"), index=False)
        return {"EXTRA_TABLES": {"claims": {"path": "data/claims.csv", "key": "customer_id", "date_col": "claim_date"}},
                "MODELS": ["logreg", "hgb", "lgbm", "catboost"]}

    @v("semicolon_latin1", "semicolon CSV, latin-1 encoding, decimal comma")
    def _(d):
        tr, te, _ = base(seed=1)
        for df in (tr, te):
            df["annual_premium"] = df["annual_premium"].map(lambda x: f"{x:.2f}".replace(".", ","))
            df["region"] = df["region"].str.replace("Jawa", "Jáwa")
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        tr.to_csv(os.path.join(d, "data", "train.csv"), index=False, sep=";", encoding="latin-1")
        te.drop(columns=["churn"]).to_csv(os.path.join(d, "data", "test.csv"), index=False, sep=";", encoding="latin-1")
        pd.DataFrame({"customer_id": te["customer_id"], "churn": 0.5}).to_csv(os.path.join(d, "data", "sample_submission.csv"), index=False)
        return {}

    @v("excel_files", "train/test as .xlsx")
    def _(d):
        tr, te, _ = base(seed=2)
        write(d, tr, te, fmt="xlsx")
        return {"TRAIN_PATH": "data/train.xlsx", "TEST_PATH": "data/test.xlsx"}

    @v("no_test", "only a training file (analysis + CV, no submission)")
    def _(d):
        tr, _, _ = base(seed=3)
        write(d, tr, None)
        return {"TEST_PATH": None, "SAMPLE_SUB_PATH": None}

    @v("multiclass_status", "target = policy status Active / Lapsed / Surrendered")
    def _(d):
        tr, te, _ = base(seed=4)
        rng = np.random.default_rng(4)
        for df in (tr, te):
            st = np.where(df["churn"] == "Yes", rng.choice(["Lapsed", "Surrendered"], len(df)), "Active")
            df["policy_status"] = st
            df.drop(columns=["churn"], inplace=True)
        write(d, tr, te, sub_col="policy_status")
        return {}

    @v("inverted_is_active", "target is_active (1 = still customer)")
    def _(d):
        tr, te, _ = base(seed=5)
        for df in (tr, te):
            df["is_active"] = (df["churn"] == "No").astype(int)
            df.drop(columns=["churn"], inplace=True)
        write(d, tr, te, sub_col="is_active")
        return {}

    @v("indonesian_columns", "Indonesian column names, target 'berhenti' = Ya/Tidak")
    def _(d):
        tr, te, _ = base(seed=6)
        ren = {"customer_id": "id_nasabah", "age": "umur", "gender": "jenis_kelamin", "region": "provinsi", "annual_income": "pendapatan",
               "policy_type": "jenis_polis", "sales_channel": "saluran", "payment_method": "metode_bayar", "payment_frequency": "frekuensi_bayar",
               "policy_start_date": "tgl_mulai_polis", "tenure_months": "lama_polis_bulan", "annual_premium": "premi_tahunan",
               "premium_change_pct": "kenaikan_premi_pct", "n_claims_3y": "jumlah_klaim", "n_complaints_12m": "jumlah_keluhan",
               "late_payments_12m": "telat_bayar", "auto_renew": "perpanjang_otomatis", "cancellation_reason": "alasan_berhenti"}
        for df in (tr, te):
            df.rename(columns=ren, inplace=True)
            df["berhenti"] = df["churn"].map({"Yes": "Ya", "No": "Tidak"})
            df.drop(columns=["churn"], inplace=True)
        write(d, tr, te, sub_col="berhenti", id_col="id_nasabah")
        return {"CURRENCY": "IDR"}

    @v("no_tenure_no_premium", "no tenure, no premium, no dates (survival & value skipped)")
    def _(d):
        tr, te, _ = base(seed=7)
        drop = ["tenure_months", "annual_premium", "policy_start_date", "premium_change_pct", "sum_insured"]
        write(d, tr.drop(columns=drop), te.drop(columns=drop))
        return {}

    @v("date_only_tenure", "tenure only as a start date + snapshot date")
    def _(d):
        tr, te, _ = base(seed=8)
        write(d, tr.drop(columns=["tenure_months"]), te.drop(columns=["tenure_months"]))
        return {}

    @v("start_end_dates", "no tenure column; policy start date + cancellation date for churners → survival time reconstructed")
    def _(d):
        tr, te, _ = base(seed=19)
        rng = np.random.default_rng(19)
        for df in (tr, te):
            start = pd.to_datetime(df["policy_start_date"])
            snap = pd.Timestamp("2025-06-30")
            gap = (snap - start).dt.days.clip(lower=1)
            end = start + pd.to_timedelta((rng.uniform(0.2, 1.0, len(df)) * gap).astype(int), unit="D")
            df["cancel_date"] = np.where(df["churn"] == "Yes", end.dt.strftime("%Y-%m-%d"), None)
            df.drop(columns=["tenure_months"], inplace=True)
        write(d, tr, te)
        return {"REFERENCE_DATE": "2025-06-30"}

    @v("single_file_missing_target", "one file only; rows with empty target are the ones to predict")
    def _(d):
        tr, te, _ = base(seed=20)
        te = te.copy()
        te["churn"] = np.nan
        allrows = pd.concat([tr, te], ignore_index=True).sample(frac=1, random_state=0)
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        allrows.to_csv(os.path.join(d, "data", "train.csv"), index=False)
        return {"TEST_PATH": None, "SAMPLE_SUB_PATH": None}

    @v("labels_separate_file", "features in train.csv, labels in train_labels.csv")
    def _(d):
        tr, te, _ = base(seed=21)
        write(d, tr.drop(columns=["churn"]), te)
        tr[["customer_id", "churn"]].to_csv(os.path.join(d, "data", "train_labels.csv"), index=False)
        return {"TRAIN_LABELS": {"path": "data/train_labels.csv", "key": "customer_id"}, "TARGET_COL": "churn"}

    @v("tiny", "300 rows")
    def _(d):
        tr, te, _ = base(n=300, n_test=100, seed=9)
        write(d, tr, te)
        return {}

    @v("wide_noise", "120 extra noise columns (numeric + categorical)")
    def _(d):
        tr, te, _ = base(seed=10)
        rng = np.random.default_rng(10)
        for df in (tr, te):
            for j in range(80):
                df[f"x_num_{j}"] = rng.normal(size=len(df))
            for j in range(40):
                df[f"x_cat_{j}"] = rng.choice(list("ABCDEFG"), len(df))
        write(d, tr, te)
        return {}

    @v("panel_monthly", "3 monthly snapshots per customer (repeated customer_id, unique row_id)")
    def _(d):
        tr, te, _ = base(n=1500, n_test=400, seed=11)
        rows = []
        for m in range(3):
            x = tr.copy()
            x["snapshot_month"] = m + 1
            x["tenure_months"] = x["tenure_months"] + m
            rows.append(x)
        trp = pd.concat(rows, ignore_index=True)
        trp.insert(0, "row_id", np.arange(len(trp)))
        te = te.copy()
        te.insert(0, "row_id", np.arange(len(trp), len(trp) + len(te)))
        write(d, trp, te, id_col="row_id")
        return {"ID_COL": "row_id"}

    @v("float_ids_numeric_target", "Kaggle-style float IDs, target 0/1 integer, int IDs in sample submission")
    def _(d):
        tr, te, _ = base(seed=12)
        for i, df in enumerate((tr, te)):
            df["policy_no"] = (221300000000 + np.arange(len(df)) + i * 100000).astype(float)
            df["Churn"] = (df["churn"] == "Yes").astype(int)
            df.drop(columns=["churn", "customer_id"], inplace=True)
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        tr.to_csv(os.path.join(d, "data", "train.csv"), index=False)
        te.drop(columns=["Churn"]).to_csv(os.path.join(d, "data", "test.csv"), index=False)
        pd.DataFrame({"policy_no": te["policy_no"].astype("int64"), "Churn": 0.5}).to_csv(os.path.join(d, "data", "sample_submission.csv"), index=False)
        return {}

    @v("all_categorical", "only categorical predictors")
    def _(d):
        tr, te, _ = base(seed=13)
        keep = ["customer_id", "gender", "marital_status", "region", "policy_type", "coverage_level", "sales_channel", "payment_method",
                "payment_frequency", "auto_renew", "churn"]
        write(d, tr[keep], te[keep])
        return {}

    @v("heavy_missing", "40–70% missing in many columns + missing target rows")
    def _(d):
        tr, te, _ = base(seed=14)
        rng = np.random.default_rng(14)
        for df in (tr, te):
            for c in ["age", "annual_premium", "n_claims_3y", "payment_method", "sales_channel", "digital_engagement_score"]:
                df.loc[rng.random(len(df)) < rng.uniform(0.4, 0.7), c] = np.nan
        tr.loc[rng.choice(len(tr), 40, replace=False), "churn"] = np.nan
        write(d, tr, te)
        return {}

    @v("extreme_imbalance", "≈2% churn rate")
    def _(d):
        tr, te, _ = base(n=6000, seed=15)
        pos = tr[tr["churn"] == "Yes"]
        tr = pd.concat([tr[tr["churn"] == "No"], pos.sample(min(len(pos), 120), random_state=0)]).sample(frac=1, random_state=0)
        write(d, tr, te)
        return {}

    @v("label_metric_f1", "metric F1, label submission with Yes/No")
    def _(d):
        tr, te, _ = base(seed=16)
        write(d, tr, te, sub_val="No")
        return {"METRIC": "f1", "SUBMISSION_MODE": "label"}

    @v("text_and_one_to_one", "free-text complaint column + one-to-one demographics table")
    def _(d):
        tr, te, _ = base(seed=17)
        rng = np.random.default_rng(17)
        words = ["slow claim", "price too high", "agent never called", "app error", "happy with service", "moving abroad"]
        demo = pd.concat([tr, te])[["customer_id", "marital_status", "dependents"]].rename(columns={"marital_status": "marital2", "dependents": "kids"})
        for df in (tr, te):
            df["last_complaint_text"] = [" ".join(rng.choice(words, 3)) + f" ticket {i}" if rng.random() < 0.6 else np.nan for i in range(len(df))]
            df.drop(columns=["dependents"], inplace=True)
        write(d, tr, te)
        demo.to_csv(os.path.join(d, "data", "demographics.csv"), index=False)
        return {"EXTRA_ONE_TO_ONE": {"demo": {"path": "data/demographics.csv", "key": "customer_id"}}}

    @v("full_mode_small", "FULL mode (all 9 algorithms, Optuna, multi-seed) on 1,500 rows + PDF/autofit")
    def _(d):
        tr, te, cl = base(n=1500, n_test=400, seed=18)
        write(d, tr, te)
        return {"RUN_MODE": "full", "OPTUNA_TRIALS": 6, "OPTUNA_TIMEOUT": 60, "FINAL_SEEDS": [42, 7], "REPORT_AUTOFIT": True, "MAKE_PDF": True,
                "N_BOOTSTRAP": 200, "MODELS": ["logreg", "rf", "et", "hgb", "lgbm", "xgb", "catboost", "ebm", "mlp"],
                "ABLATION_MAX_GROUPS": 8, "CAUSAL_MAX_TREATMENTS": 6, "N_FOLDS": 3}

    return V


def run_one(name, desc, fn, out, py):
    d = os.path.join(out, name)
    os.makedirs(d, exist_ok=True)
    cfg = dict(BASE_CFG)
    cfg.update(fn(d) or {})
    cfg["TEAM_NAME"] = f"Stress_{name}"
    with open(os.path.join(d, "case_config.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    t0 = time.time()
    p = subprocess.run([py, os.path.join(HERE, "run_case.py"), "--config", os.path.join(d, "case_config.json")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    with open(os.path.join(d, "run.log"), "w", encoding="utf-8") as f:
        f.write(p.stdout + "\n" + p.stderr)
    res = {"variant": name, "description": desc, "exit": p.returncode, "minutes": round((time.time() - t0) / 60, 1)}
    sp = os.path.join(d, "outputs", "churn_insurance", "run_summary.json")
    if os.path.exists(sp):
        s = json.load(open(sp, encoding="utf-8"))
        res.update({"auc": round(s.get("final_oof_auc", float("nan")), 4), "churn_rate": round(s.get("churn_rate", float("nan")), 3),
                    "section_errors": "; ".join(f"{k}: {v[:120]}" for k, v in (s.get("section_errors") or {}).items()) or "none"})
    o = os.path.join(d, "outputs", "churn_insurance")
    res["report"] = os.path.exists(os.path.join(o, "REPORT_DRAFT.docx"))
    res["dashboard"] = os.path.exists(os.path.join(o, "dashboard", "data.js"))
    res["submission"] = os.path.exists(os.path.join(o, "submission.csv"))
    print(f"[{'OK ' if p.returncode == 0 else 'ERR'}] {name:<26} exit={p.returncode} {res.get('minutes')} min | {res.get('section_errors', 'NO SUMMARY')}")
    return res


def md_table(df):
    """Tabel markdown tanpa dependensi (tabulate tidak selalu terpasang)."""
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        lines.append("| " + " | ".join(str(v).replace("|", "/") for v in r) + " |")
    return "\n".join(lines)


def summarize(out):
    """Bangun ulang ringkasan dari folder hasil (tanpa menjalankan ulang)."""
    V = variants()
    rows = []
    for name in sorted(os.listdir(out)):
        d = os.path.join(out, name)
        sp = os.path.join(d, "outputs", "churn_insurance", "run_summary.json")
        if not os.path.isdir(d):
            continue
        r = {"variant": name, "description": V.get(name, ("",))[0]}
        if os.path.exists(sp):
            s = json.load(open(sp, encoding="utf-8"))
            errs = s.get("section_errors") or {}
            r.update({"status": "PASS" if not errs else "SECTION ERRORS", "auc": round(s.get("final_oof_auc", float("nan")), 4),
                      "n_train": s.get("n_train"), "target": s.get("target"), "section_errors": "; ".join(errs) or "none"})
        else:
            r.update({"status": "FAIL (no summary)"})
        o = os.path.join(d, "outputs", "churn_insurance")
        r["report"] = os.path.exists(os.path.join(o, "REPORT_DRAFT.docx"))
        r["dashboard"] = os.path.exists(os.path.join(o, "dashboard", "data.js"))
        r["submission"] = os.path.exists(os.path.join(o, "submission.csv"))
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="stress_runs")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--summarize", action="store_true", help="hanya bangun ulang STRESS_TEST_REPORT.md dari hasil yang ada")
    args = ap.parse_args()
    V = variants()
    os.makedirs(args.out, exist_ok=True)
    if not args.summarize:
        names = [n for n in V if not args.only or n in args.only.split(",")]
        with ThreadPoolExecutor(args.jobs) as ex:
            list(ex.map(lambda n: run_one(n, V[n][0], V[n][1], os.path.abspath(args.out), sys.executable), names))
    df = summarize(os.path.abspath(args.out))
    ok = int((df.get("status", pd.Series(dtype=str)) == "PASS").sum())
    with open(os.path.join(args.out, "STRESS_TEST_REPORT.md"), "w", encoding="utf-8") as f:
        f.write(f"# Stress test — {ok}/{len(df)} variants passed\n\n")
        f.write("Setiap varian = satu bentuk data asuransi berbeda, dijalankan end-to-end oleh `tools/run_case.py` (notebook utuh: "
                "cleaning → analisis → model → kausal → laporan DOCX → dashboard → submission). PASS = selesai tanpa satu pun section error.\n\n")
        f.write(md_table(df))
    print(f"\n{ok}/{len(df)} variants passed → {os.path.join(args.out, 'STRESS_TEST_REPORT.md')}")
    return 0 if ok == len(df) else 1


if __name__ == "__main__":
    sys.exit(main())
