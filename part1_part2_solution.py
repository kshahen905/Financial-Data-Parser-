import pandas as pd
import itertools
import time
from dataclasses import dataclass
from typing import Dict, List
from tqdm import tqdm


@dataclass
class Transaction:
    idx: int
    amount: float
    description: str


@dataclass
class Target:
    idx: int
    target: float
    reference: str


@dataclass
class Report:
    exact_matches: Dict[int, int]       # target_idx -> transaction_idx
    subset_matches: Dict[int, List[int]]  # target_idx -> [transaction_idx...]
    time_exact: float
    time_subset: float



# Prepare data

def prepare_transactions(df: pd.DataFrame, amount_col: str, desc_col: str) -> List[Transaction]:
    transactions = []
    for idx, row in df.iterrows():
        try:
            amt = float(row[amount_col])
        except Exception:
            continue
        desc = str(row[desc_col]) if desc_col in df.columns else ""
        transactions.append(Transaction(idx=idx, amount=amt, description=desc))
    return transactions


def prepare_targets(df: pd.DataFrame, amount_col: str, ref_col: str) -> List[Target]:
    targets = []
    for idx, row in df.iterrows():
        try:
            amt = float(row[amount_col])
        except Exception:
            continue
        ref = str(row[ref_col]) if ref_col in df.columns else ""
        targets.append(Target(idx=idx, target=amt, reference=ref))
    return targets


# Reconciliation (Part 1 & 2)

def reconcile(tx_df: pd.DataFrame,
              tgt_df: pd.DataFrame,
              tx_amount_col: str,
              tx_desc_col: str,
              tgt_amount_col: str,
              tgt_ref_col: str,
              tolerance: float = 0.01,
              limit_targets: int = None) -> Report:
    """
    Part 1 & 2:
    - Direct 1-to-1 exact matches (with tolerance)
    - Subset sum matches (brute force, small subsets only)
    """

    transactions = prepare_transactions(tx_df, tx_amount_col, tx_desc_col)
    targets = prepare_targets(tgt_df, tgt_amount_col, tgt_ref_col)

    if limit_targets:
        targets = targets[:limit_targets]

    exact_matches = {}
    subset_matches = {}

    # Exact matches 
    start = time.perf_counter()
    for tgt in targets:
        for tx in transactions:
            if abs(tx.amount - tgt.target) <= tolerance:
                exact_matches[tgt.idx] = tx.idx
                break
    time_exact = time.perf_counter() - start
    print(f" Part 1 (Exact) found {len(exact_matches)} matches in {time_exact:.4f}s")

    # Subset matches (brute force)
    start = time.perf_counter()
    max_subset = 2  # limit to 3 transactions per target for feasibility
    for tgt in tqdm(targets, desc=" Part 2: Subset Sum", unit="target"):
        found = False
        for r in range(2, max_subset + 1):  # subsets of size 2..3
            for combo in itertools.combinations(transactions, r):
                total = sum(tx.amount for tx in combo)
                if abs(total - tgt.target) <= tolerance:
                    subset_matches[tgt.idx] = [tx.idx for tx in combo]
                    found = True
                    break
            if found:
                break
    time_subset = time.perf_counter() - start
    print(f" Part 2 (Subset Sum) found {len(subset_matches)} matches in {time_subset:.4f}s")

    return Report(
        exact_matches=exact_matches,
        subset_matches=subset_matches,
        time_exact=time_exact,
        time_subset=time_subset
    )
