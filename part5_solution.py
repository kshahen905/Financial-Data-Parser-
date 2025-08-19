import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Utility: Safe CSV Loader

def safe_read_csv(path, columns=None):
    """Safely read CSV, return empty DataFrame if file missing or empty."""
    try:
        df = pd.read_csv(path)
        return df
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=columns if columns else [])


# Paths

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Load CSV results from Part 1–4 (safe)

exact_df = safe_read_csv(OUTPUT_DIR / "exact_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description"])

subset_df = safe_read_csv(OUTPUT_DIR / "subset_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description"])

opt_df = safe_read_csv(OUTPUT_DIR / "optimized_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description"])

ga_df = safe_read_csv(OUTPUT_DIR / "ga_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description"])

fuzzy_df = safe_read_csv(OUTPUT_DIR / "fuzzy_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description","Fuzzy_Score"])

ga_fuzzy_df = safe_read_csv(OUTPUT_DIR / "ga_fuzzy_matches.csv",
    ["Target_Ref","Target_Amount","Transaction_ID","Transaction_Amount","Description","Fuzzy_Score"])

# Total targets

TOTAL_TARGETS = 1221

# Match counts & times (from last run)

summary_data = {
    "Method": [
        "Exact (Part 1)",
        "Subset (Part 2, first 100)",
        "Optimized (Part 3)",
        "GA (Part 4.1)",
        "Fuzzy (Part 4.2)",
        "GA+Fuzzy (Part 4.3)"
    ],
    "Matches": [
        len(exact_df),
        len(subset_df["Target_Ref"].unique()),
        len(opt_df["Target_Ref"].unique()),
        len(ga_df["Target_Ref"].unique()),
        len(fuzzy_df["Target_Ref"].unique()),
        len(ga_fuzzy_df["Target_Ref"].unique())
    ],
    "Time (s)": [
        0.1302,      # Exact
        1286.9182,   # Subset
        6.5003,      # Optimized
        5.9511,      # GA
        3.9913,      # Fuzzy
        0.0237       # GA+Fuzzy
    ]
}
summary_df = pd.DataFrame(summary_data)

# Coverage % column
summary_df["Coverage (%)"] = (summary_df["Matches"] / TOTAL_TARGETS * 100).round(2)

summary_df.to_csv(OUTPUT_DIR / "part5_summary.csv", index=False, encoding="utf-8-sig")

print("\n Consolidated Summary with Coverage %")
print(summary_df)


# Unmatched Targets

all_matched = set(exact_df["Target_Ref"]) \
              | set(subset_df["Target_Ref"]) \
              | set(opt_df["Target_Ref"]) \
              | set(ga_df["Target_Ref"]) \
              | set(fuzzy_df["Target_Ref"]) \
              | set(ga_fuzzy_df["Target_Ref"])

# Load original targets file
targets_path = BASE_DIR / "data" / "sample" / "KH_Bank.XLSX"
targets_df = pd.read_excel(targets_path, sheet_name="Sheet1")

unmatched_df = targets_df[~targets_df["Statement.Entry.EntryReference"].isin(all_matched)].copy()
unmatched_df.rename(columns={
    "Statement.Entry.EntryReference": "Target_Ref",
    "Statement.Entry.Amount.Value": "Target_Amount"
}, inplace=True)

unmatched_df.to_csv(OUTPUT_DIR / "unmatched_targets.csv", index=False, encoding="utf-8-sig")

print(f"\n Unmatched targets saved ({len(unmatched_df)} out of {TOTAL_TARGETS}).")


# Visualization

plt.figure(figsize=(8,6))
plt.bar(summary_df["Method"], summary_df["Matches"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Number of Matches")
plt.title("Matches per Method")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "matches_bar.png")
plt.close()

plt.figure(figsize=(6,6))
matched_total = len(all_matched)
unmatched_total = TOTAL_TARGETS - matched_total
plt.pie([matched_total, unmatched_total],
        labels=["Matched", "Unmatched"],
        autopct="%1.1f%%",
        startangle=90)
plt.title("Matched vs Unmatched Targets")
plt.savefig(OUTPUT_DIR / "matched_vs_unmatched_pie.png")
plt.close()

plt.figure(figsize=(8,6))
plt.bar(summary_df["Method"], summary_df["Time (s)"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Time (seconds)")
plt.title("Execution Time per Method")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "time_bar.png")
plt.close()


# Excel Report (multi-sheet)

excel_path = OUTPUT_DIR / "part5_report.xlsx"
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    exact_df.to_excel(writer, sheet_name="Exact Matches", index=False)
    subset_df.to_excel(writer, sheet_name="Subset Matches", index=False)
    opt_df.to_excel(writer, sheet_name="Optimized Matches", index=False)
    ga_df.to_excel(writer, sheet_name="GA Matches", index=False)
    fuzzy_df.to_excel(writer, sheet_name="Fuzzy Matches", index=False)
    ga_fuzzy_df.to_excel(writer, sheet_name="GA+Fuzzy Matches", index=False)
    unmatched_df.to_excel(writer, sheet_name="Unmatched Targets", index=False)

print(f"\n Excel report saved to: {excel_path}")
print("\n Part 5 completed successfully.")
