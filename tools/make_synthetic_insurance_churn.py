"""
Generate a realistic, deliberately MESSY synthetic insurance churn dataset for practice.

Output (default ./data/):
    train.csv              -> features + target `churn` ("Yes"/"No")
    test.csv               -> features only
    sample_submission.csv  -> customer_id, churn
    claims.csv             -> one-to-many child table (customer_id, claim_date, claim_amount, status)

Known (planted) churn drivers, so you can check whether your analysis recovers them:
    + short tenure, + premium increase at last renewal (stronger for low income), + complaints,
    + rejected claims, + late payments, + slow claim settlement, + monthly payment, + online channel
    - auto-debit payment, - more products (bundling), - auto-renew, - digital engagement,
    U-shape on age (young & very old churn more)

Planted data problems:
    numeric stored as strings with thousand separators, inconsistent category spelling/whitespace,
    impossible ages (999, -1), missing values (MCAR + MNAR), constant column, duplicated rows,
    high-cardinality agent_id, date column, and a LEAKAGE column (`cancellation_reason`).

Usage:
    python make_synthetic_insurance_churn.py --n_train 8000 --n_test 2000 --out ./data --seed 42
"""
import argparse
import os

import numpy as np
import pandas as pd


def make_customers(n, rng, id_start=1):
    ids = [f"CUST{i:06d}" for i in range(id_start, id_start + n)]
    age = np.clip(rng.normal(42, 13, n), 18, 85).round()
    gender = rng.choice(["Male", "Female"], n, p=[0.52, 0.48])
    marital = rng.choice(["Single", "Married", "Divorced", "Widowed"], n, p=[0.3, 0.55, 0.1, 0.05])
    dependents = rng.poisson(1.2, n)
    region = rng.choice(
        ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Jawa Tengah", "Banten", "Bali",
         "Sumatera Utara", "Sulawesi Selatan", "Kalimantan Timur", "DI Yogyakarta"],
        n, p=[0.22, 0.18, 0.15, 0.12, 0.08, 0.05, 0.07, 0.05, 0.04, 0.04])
    income = np.exp(rng.normal(np.log(9e7), 0.6, n)).round(-5)  # annual income IDR
    policy_type = rng.choice(["Life", "Health", "Auto", "Property"], n, p=[0.3, 0.35, 0.25, 0.1])
    coverage = rng.choice(["Basic", "Standard", "Premium"], n, p=[0.4, 0.4, 0.2])
    channel = rng.choice(["Agent", "Online", "Bancassurance", "Broker"], n, p=[0.45, 0.25, 0.2, 0.1])
    pay_method = rng.choice(["Auto-debit", "Bank Transfer", "Credit Card", "Cash"], n, p=[0.35, 0.3, 0.25, 0.1])
    pay_freq = rng.choice(["Monthly", "Quarterly", "Annual"], n, p=[0.5, 0.2, 0.3])
    tenure = np.clip(rng.gamma(1.6, 18, n), 1, 180).round()
    start = pd.Timestamp("2025-06-30") - pd.to_timedelta(tenure * 30.4, unit="D")
    cov_mult = pd.Series(coverage).map({"Basic": 1.0, "Standard": 1.6, "Premium": 2.6}).values
    type_mult = pd.Series(policy_type).map({"Life": 1.2, "Health": 1.0, "Auto": 0.8, "Property": 1.4}).values
    premium = (3.5e6 * cov_mult * type_mult * (1 + (age - 40) / 100) * rng.lognormal(0, 0.25, n)).round(-3)
    premium_change = np.round(rng.normal(4, 7, n), 1)  # % change at last renewal
    sum_insured = (premium * rng.uniform(40, 120, n)).round(-5)
    n_products = 1 + rng.poisson(0.6, n)
    n_claims = rng.poisson(0.5 + 0.3 * (policy_type == "Health"), n)
    n_rejected = np.array([rng.binomial(k, 0.25) for k in n_claims])
    settle_days = np.where(n_claims > 0, np.round(rng.gamma(2.5, 6, n)), np.nan)
    complaints = rng.poisson(0.25 + 0.4 * (n_rejected > 0), n)
    late_pay = rng.poisson(0.4 + 0.6 * (pay_method == "Cash") + 0.3 * (pay_freq == "Monthly"), n)
    engagement = np.clip(rng.normal(50, 20, n) + 15 * (channel == "Online"), 0, 100).round()
    auto_renew = rng.choice(["Yes", "No"], n, p=[0.55, 0.45])
    agent_id = np.where(channel == "Agent", [f"AG{rng.integers(1, 400):04d}" for _ in range(n)], "NONE")

    # ---- churn mechanism (logit) ----
    low_income = (income < np.quantile(income, 0.3)).astype(float)
    logit = (
        -1.35
        - 0.022 * tenure
        + 0.055 * premium_change * (1 + 0.8 * low_income)
        + 0.45 * complaints
        + 0.55 * n_rejected
        + 0.30 * late_pay
        + 0.025 * np.nan_to_num(settle_days, nan=0)
        + 0.35 * (pay_freq == "Monthly")
        + 0.45 * (channel == "Online")
        - 0.70 * (pay_method == "Auto-debit")
        - 0.35 * (n_products - 1)
        - 0.60 * (auto_renew == "Yes")
        - 0.012 * (engagement - 50)
        + 0.0009 * (age - 45) ** 2
        - 0.2 * (marital == "Married")
    )
    p = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, p)

    df = pd.DataFrame({
        "customer_id": ids, "age": age, "gender": gender, "marital_status": marital,
        "dependents": dependents, "region": region, "annual_income": income,
        "policy_type": policy_type, "coverage_level": coverage, "sales_channel": channel,
        "agent_id": agent_id, "payment_method": pay_method, "payment_frequency": pay_freq,
        "policy_start_date": start.strftime("%Y-%m-%d"), "tenure_months": tenure,
        "annual_premium": premium, "premium_change_pct": premium_change, "sum_insured": sum_insured,
        "n_products": n_products, "n_claims_3y": n_claims, "n_claims_rejected": n_rejected,
        "avg_claim_settlement_days": settle_days, "n_complaints_12m": complaints,
        "late_payments_12m": late_pay, "digital_engagement_score": engagement,
        "auto_renew": auto_renew, "currency": "IDR",
    })
    reasons = rng.choice(["Price", "Service", "Moved", "Competitor offer", "Claim issue"], n)
    df["cancellation_reason"] = pd.Series(reasons, dtype=object).where(churn == 1, None).values  # LEAKAGE on purpose
    return df, churn


def add_mess(df, rng):
    df = df.copy()
    n = len(df)
    # inconsistent categorical spelling
    idx = rng.choice(n, n // 25, replace=False)
    df.loc[idx, "gender"] = df.loc[idx, "gender"].str.lower() + " "
    idx = rng.choice(n, n // 40, replace=False)
    df.loc[idx, "payment_method"] = df.loc[idx, "payment_method"].str.upper()
    # numeric as string with thousand separators
    df["annual_income"] = df["annual_income"].map(lambda v: f"{v:,.0f}")
    # impossible values
    df.loc[rng.choice(n, 6, replace=False), "age"] = 999
    df.loc[rng.choice(n, 3, replace=False), "age"] = -1
    # missing values
    for col, frac in [("annual_income", 0.08), ("marital_status", 0.03), ("digital_engagement_score", 0.10),
                      ("premium_change_pct", 0.04), ("region", 0.01)]:
        idx = rng.choice(n, int(n * frac), replace=False)
        df.loc[idx, col] = np.nan
    return df


def make_claims(df, rng):
    rows = []
    for cid, k, rej in zip(df["customer_id"], df["n_claims_3y"], df["n_claims_rejected"]):
        statuses = ["Rejected"] * int(rej) + ["Approved"] * int(k - rej)
        for s in statuses:
            rows.append({
                "customer_id": cid,
                "claim_date": (pd.Timestamp("2025-06-30") - pd.Timedelta(days=int(rng.integers(1, 1095)))).strftime("%Y-%m-%d"),
                "claim_amount": float(np.round(rng.lognormal(15, 0.8), -3)),
                "status": s,
            })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_train", type=int, default=8000)
    ap.add_argument("--n_test", type=int, default=2000)
    ap.add_argument("--out", default="./data")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    os.makedirs(args.out, exist_ok=True)

    full, churn = make_customers(args.n_train + args.n_test, rng)
    claims = make_claims(full, rng)
    full = add_mess(full, rng)
    full["churn"] = np.where(churn == 1, "Yes", "No")

    train = full.iloc[: args.n_train].copy()
    test = full.iloc[args.n_train:].copy()
    # duplicated rows in train
    train = pd.concat([train, train.sample(15, random_state=args.seed)], ignore_index=True)

    test_truth = test[["customer_id", "churn"]].copy()
    test = test.drop(columns=["churn"])
    sub = pd.DataFrame({"customer_id": test["customer_id"], "churn": 0.5})

    train.to_csv(os.path.join(args.out, "train.csv"), index=False)
    test.to_csv(os.path.join(args.out, "test.csv"), index=False)
    sub.to_csv(os.path.join(args.out, "sample_submission.csv"), index=False)
    claims.to_csv(os.path.join(args.out, "claims.csv"), index=False)
    test_truth.to_csv(os.path.join(args.out, "_test_truth_DO_NOT_USE.csv"), index=False)
    print(f"train {train.shape}, test {test.shape}, claims {claims.shape}, churn rate {churn[:args.n_train].mean():.3f}")


if __name__ == "__main__":
    main()
