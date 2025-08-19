import pandas as pd
from pathlib import Path
from part1_part2_solution import reconcile
from part3_solution import run_part3
from part4_solution import run_part4

# Setup paths

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "sample"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Load datasets

transactions_path = DATA_DIR / "Customer_Ledger_Entries_FULL.xlsx"
targets_path = DATA_DIR / "KH_Bank.XLSX"

transactions_df = pd.read_excel(transactions_path, sheet_name="Customer Ledger Entries")
targets_df = pd.read_excel(targets_path, sheet_name="Sheet1")

print(f" Loaded {transactions_df.shape[0]} transactions and {targets_df.shape[0]} targets.")


# Run Part 1 & 2: Brute Force (limit to first 100 targets)

report = reconcile(
    transactions_df,
    targets_df,
    tx_amount_col="Remaining Amt. (LCY)",
    tx_desc_col="Description", 
    tgt_amount_col="Statement.Entry.Amount.Value",
    tgt_ref_col="Statement.Entry.EntryReference",
    tolerance=0.01,
    limit_targets=100  #  Only first 100 targets for brute force
)

# Save Exact Matches
exact_rows = []
for tgt_idx, tx_idx in report.exact_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    tx_row = transactions_df.iloc[tx_idx]
    exact_rows.append({
        "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
        "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
        "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
        "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
        "Description": tx_row["Description"]
    })
pd.DataFrame(exact_rows).to_csv(OUTPUT_DIR / "exact_matches.csv", index=False, encoding="utf-8-sig")

# Save Subset Matches
subset_rows = []
for tgt_idx, tx_idxs in report.subset_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    for tx_idx in tx_idxs:
        tx_row = transactions_df.iloc[tx_idx]
        subset_rows.append({
            "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
            "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
            "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
            "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
            "Description": tx_row["Description"]
        })
pd.DataFrame(subset_rows).to_csv(OUTPUT_DIR / "subset_matches.csv", index=False, encoding="utf-8-sig")

print(" Part 1 & 2 results saved (only first 100 targets).")


# Run Part 3: Optimized Hash Matching (all 1221 targets)

report3 = run_part3(
    transactions_df,
    targets_df,
    tx_amount_col="Remaining Amt. (LCY)",
    tx_desc_col="Description",
    tgt_amount_col="Statement.Entry.Amount.Value",
    tgt_ref_col="Statement.Entry.EntryReference",
    tol=0.01
)

opt_rows = []
for tgt_idx, tx_idx in report3.optimized_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    tx_row = transactions_df.iloc[tx_idx]
    opt_rows.append({
        "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
        "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
        "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
        "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
        "Description": tx_row["Description"]
    })
pd.DataFrame(opt_rows).to_csv(OUTPUT_DIR / "optimized_matches.csv", index=False, encoding="utf-8-sig")
print(" Part 3 results saved (all targets).")


# Run Part 4: GA + Fuzzy (all 1221 targets)

report4, ga_fuzzy_matches, time_ga_fuzzy = run_part4(
    transactions_df,
    targets_df,
    tx_amount_col="Remaining Amt. (LCY)",
    tx_desc_col="Description",
    tgt_amount_col="Statement.Entry.Amount.Value",
    tgt_ref_col="Statement.Entry.EntryReference",
    tol=0.01
)

# Save GA Matches
ga_rows = []
for tgt_idx, tx_idxs in report4.ga_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    for tx_idx in tx_idxs:
        tx_row = transactions_df.iloc[tx_idx]
        ga_rows.append({
            "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
            "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
            "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
            "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
            "Description": tx_row["Description"]
        })
pd.DataFrame(ga_rows).to_csv(OUTPUT_DIR / "ga_matches.csv", index=False, encoding="utf-8-sig")

# Save Fuzzy Matches
fuzzy_rows = []
for tgt_idx, (tx_idx, score) in report4.fuzzy_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    tx_row = transactions_df.iloc[tx_idx]
    fuzzy_rows.append({
        "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
        "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
        "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
        "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
        "Description": tx_row["Description"],
        "Fuzzy_Score": score
    })
pd.DataFrame(fuzzy_rows).to_csv(OUTPUT_DIR / "fuzzy_matches.csv", index=False, encoding="utf-8-sig")

# Save GA+Fuzzy Matches
ga_fuzzy_rows = []
for tgt_idx, (tx_idx, score) in ga_fuzzy_matches.items():
    tgt_row = targets_df.iloc[tgt_idx]
    tx_row = transactions_df.iloc[tx_idx]
    ga_fuzzy_rows.append({
        "Target_Ref": tgt_row["Statement.Entry.EntryReference"],
        "Target_Amount": tgt_row["Statement.Entry.Amount.Value"],
        "Transaction_ID": tx_row["Document No."] if "Document No." in tx_row else tx_idx,
        "Transaction_Amount": tx_row["Remaining Amt. (LCY)"],
        "Description": tx_row["Description"],
        "Fuzzy_Score": score
    })
pd.DataFrame(ga_fuzzy_rows).to_csv(OUTPUT_DIR / "ga_fuzzy_matches.csv", index=False, encoding="utf-8-sig")

print(" Part 4 results saved (all targets).")


# Final Comparison Summary

summary_data = {
    "Metric": [
        "Exact Matches (Part 2.1, first 100)",
        "Subset Matches (Part 2.2 - brute force, first 100)",
        "Optimized Matches (Part 3, all)",
        "GA Matches (Part 4.1, all)",
        "Fuzzy Matches (Part 4.2, all)",
        "GA+Fuzzy Matches (Part 4.3, all)",
        "Time Exact (s)",
        "Time Subset (s)",
        "Time Optimized (s)",
        "Time GA (s)",
        "Time Fuzzy (s)",
        "Time GA+Fuzzy (s)"
    ],
    "Value": [
        len(report.exact_matches),
        len(report.subset_matches),
        len(report3.optimized_matches),
        len(report4.ga_matches),
        len(report4.fuzzy_matches),
        len(ga_fuzzy_matches),
        round(report.time_exact, 6),
        round(report.time_subset, 6),
        round(report3.time_optimized, 6),
        round(report4.time_ga, 6),
        round(report4.time_fuzzy, 6),
        round(time_ga_fuzzy, 6)
    ]
}

summary_df = pd.DataFrame(summary_data)

print("\n Comparison Summary")
print(summary_df.to_string(index=False))

summary_path = OUTPUT_DIR / "comparison_summary.csv"
summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")
print(f"\n Comparison summary saved to: {summary_path}")
