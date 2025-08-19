import pandas as pd
import time
from dataclasses import dataclass
from typing import List, Dict
from part1_part2_solution import Transaction, Target, prepare_transactions, prepare_targets
from tqdm import tqdm  # progress bar


@dataclass
class ReportPart3:
    optimized_matches: Dict
    time_optimized: float


# Optimized Approach (Hash-based pair sum)

def optimized_match(transactions: List[Transaction], targets: List[Target], tol: float = 0.0):
    """
    Optimized pair-matching using hashing (O(n) per target).
    Only checks pairs (subset size = 2).
    """
    start = time.perf_counter()
    matches = {}

    # Pre-build hashmap: amount -> list of transaction indices
    amount_map = {}
    for tx in transactions:
        amount_map.setdefault(round(tx.amount, 2), []).append(tx.idx)

    # tqdm progress bar for targets
    for tgt in tqdm(targets, desc="⚡ Part 3: Optimized Matching", unit="target"):
        target_val = round(tgt.target, 2)
        found = False
        for tx in transactions:
            need = round(target_val - tx.amount, 2)
            if need in amount_map:
                # found a pair (tx + some other tx = target)
                pair = [tx.idx, amount_map[need][0]]
                matches[tgt.idx] = pair
                found = True
                break
        if found:
            continue

    elapsed = time.perf_counter() - start
    print(f" Optimized matching complete: {len(matches)} matches found in {elapsed:.4f}s")
    return ReportPart3(matches, elapsed)


# Orchestration for Part 3

def run_part3(tx_df, tgt_df,
              tx_amount_col, tx_desc_col,
              tgt_amount_col, tgt_ref_col,
              tol: float = 0.0):
    """
    Prepares data, runs optimized match, and returns a report.
    """
    print("\n Starting Part 3: Optimized Approach...")
    txs = prepare_transactions(tx_df, tx_amount_col, tx_desc_col)
    tgts = prepare_targets(tgt_df, tgt_amount_col, tgt_ref_col)

    report = optimized_match(txs, tgts, tol)
    return report
