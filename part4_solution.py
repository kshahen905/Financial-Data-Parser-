import time
from dataclasses import dataclass
from typing import Dict, List, Tuple
from tqdm import tqdm
from rapidfuzz import fuzz   # Faster fuzzy matching than difflib


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
class Report4:
    ga_matches: Dict[int, List[int]]
    fuzzy_matches: Dict[int, Tuple[int, int]]
    time_ga: float
    time_fuzzy: float


# Optimized GA Matching

def ga_match(transactions: List[Transaction], targets: List[Target], tol: float = 0.01):
    """
    Optimized GA-like matching using:
    - Filtering candidates by tolerance range
    - Hash-based 2-sum lookup (like Part 3)
    """
    start = time.perf_counter()
    matches = {}

    # Prebuild hashmap for fast lookups
    amount_map = {}
    for tx in transactions:
        amount_map.setdefault(round(tx.amount, 2), []).append(tx.idx)

    for tgt in tqdm(targets, desc=" Part 4.1: GA (Optimized)", unit="target"):
        target_val = round(tgt.target, 2)

        # 1. Direct single transaction match
        if target_val in amount_map:
            matches[tgt.idx] = [amount_map[target_val][0]]
            continue

        # 2. Try 2-sum pairs
        found = False
        for tx in transactions:
            need = round(target_val - tx.amount, 2)
            if need in amount_map:
                matches[tgt.idx] = [tx.idx, amount_map[need][0]]
                found = True
                break
        if found:
            continue

    elapsed = time.perf_counter() - start
    print(f" Part 4.1 (GA Optimized) found {len(matches)} matches in {elapsed:.4f}s")
    return matches, elapsed


# Optimized Fuzzy Matching

def fuzzy_match(transactions: List[Transaction], targets: List[Target], threshold: int = 80):
    """
    Optimized fuzzy matching using RapidFuzz (much faster than difflib).
    """
    start = time.perf_counter()
    matches = {}

    for tgt in tqdm(targets, desc=" Part 4.2: Fuzzy (Optimized)", unit="target"):
        best_score = -1
        best_tx = None
        tgt_str = str(tgt.reference)

        for tx in transactions:
            score = fuzz.ratio(tgt_str, tx.description)
            if score > best_score:
                best_score = score
                best_tx = tx

        if best_tx and best_score >= threshold:
            matches[tgt.idx] = (best_tx.idx, best_score)

    elapsed = time.perf_counter() - start
    print(f" Part 4.2 (Fuzzy Optimized) found {len(matches)} matches in {elapsed:.4f}s")
    return matches, elapsed


# Orchestration for Part 4

def run_part4(tx_df, tgt_df, tx_amount_col, tx_desc_col, tgt_amount_col, tgt_ref_col, tol=0.01):
    # Prepare transactions
    transactions = []
    for idx, row in tx_df.iterrows():
        try:
            amt = float(row[tx_amount_col])
        except Exception:
            continue
        desc = str(row[tx_desc_col]) if tx_desc_col in tx_df.columns else ""
        transactions.append(Transaction(idx=idx, amount=amt, description=desc))

    # Prepare targets
    targets = []
    for idx, row in tgt_df.iterrows():
        try:
            amt = float(row[tgt_amount_col])
        except Exception:
            continue
        ref = str(row[tgt_ref_col]) if tgt_ref_col in tgt_df.columns else ""
        targets.append(Target(idx=idx, target=amt, reference=ref))

    # Run GA Matching (Optimized)
    ga_matches, time_ga = ga_match(transactions, targets, tol)

    # Run Fuzzy Matching (Optimized)
    fuzzy_matches, time_fuzzy = fuzzy_match(transactions, targets)

    # Combine GA + Fuzzy
    start_comb = time.perf_counter()
    ga_fuzzy_matches = {}
    for tgt_idx, tx_idxs in ga_matches.items():
        tx = transactions[tx_idxs[0]]
        tgt_ref = str(tgt_df.iloc[tgt_idx][tgt_ref_col])
        score = fuzz.ratio(tgt_ref, tx.description)
        ga_fuzzy_matches[tgt_idx] = (tx.idx, score)
    time_comb = time.perf_counter() - start_comb
    print(f" Part 4.3 (GA+Fuzzy) combined {len(ga_fuzzy_matches)} matches in {time_comb:.4f}s")

    report4 = Report4(
        ga_matches=ga_matches,
        fuzzy_matches=fuzzy_matches,
        time_ga=time_ga,
        time_fuzzy=time_fuzzy,
    )

    return report4, ga_fuzzy_matches, time_comb
