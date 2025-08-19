# 📘 Financial Data Parser & Reconciliation Engine

A modular Python application that can **parse complex Excel financial data (Phase 1)** and perform **transaction-to-statement reconciliation with multiple strategies (Phase 2)**.  

Designed to handle messy Excel formats, detect column types, and provide structured outputs for **financial analysis, reconciliation, and reporting**.

---

## ✨ Features

### 🔹 **Phase 1 – Financial Data Parsing**
- Load multiple Excel files (with multiple sheets)  
- Automatically detect column types: **date**, **number**, **string**  
- Parse currency formats (₹, $, €, K, M, B) and Excel serial dates  
- Query datasets with custom conditions (e.g., `Amount > 1000`)  
- Group and aggregate data (e.g., totals by category or month)  
- Fully unit-tested with `unittest`  

### 🔹 **Phase 2 – Transaction Reconciliation**
- Match **bank statement targets** with **customer ledger transactions**  
- Implements multiple reconciliation strategies:
  - **Part 1:** Exact 1-to-1 matches  
  - **Part 2:** Subset sum (small groups of transactions)  
  - **Part 3:** Optimized hash-based pair matching  
  - **Part 4:** Genetic-inspired (GA-like) + fuzzy text matching  
  - **Part 5:** Consolidated reporting & visualization  
- Saves structured outputs to **CSV & Excel**  
- Generates summary charts:
  - Matches per method  
  - Matched vs unmatched (pie chart)  
  - Execution time per method  

---

## 📂 Project Structure

financial-data-parser/
├── main.py # Entry point (runs reconciliation Parts 1–4)
├── part1_part2_solution.py # Exact + Subset brute-force reconciliation
├── part3_solution.py # Optimized hash-based reconciliation
├── part4_solution.py # GA-inspired + fuzzy reconciliation
├── part5_solution.py # Reporting & visualization
├── src/ # Phase 1 parsing logic
│ └── core/
│ ├── data_storage.py
│ ├── data_type_detector.py
│ ├── excel_processor.py
│ ├── format_parser.py
├── config/
│ └── settings.py # Excel file paths & data dir
├── data/
│ ├── sample/ # Input Excel files (ledger + bank)
│ └── processed/ # Outputs: matches, reports, charts
├── tests/ # Unit tests (Phase 1)
├── examples/ # Demo scripts (Phase 1)
├── scripts/
│ └── run_benchmarks.py # Phase 1 performance benchmarking
├── requirements.txt # Dependencies
└── README.md # This file

## ⚙️ Installation & Environment Setup

Make sure you have **Python 3.11+** installed.

### 1️⃣ Clone repository
```bash
git clone https://github.com/kshahen905/Financial-Data-Parser-.git
cd Financial-Data-Parser-

2️⃣ Create virtual environment (recommended)
python -m venv venv
Activate it:

Windows (PowerShell):

venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ How to Run
🔹 Phase 1 – Parsing & Querying
python src/core/excel_processor.py

🔹 Phase 2 – Reconciliation

Step 1: Run Parts 1–4

python main.py


Generates reconciliation results in data/processed/.

Step 2: Reporting (Part 5)

python part5_solution.py


Generates:

part5_summary.csv

part5_report.xlsx (multi-sheet Excel with all results)

unmatched_targets.csv

Charts: matches_bar.png, time_bar.png, matched_vs_unmatched_pie.png

📊 Example Results (Phase 2 run)

Transactions: 5505

Targets: 1221

Method	Matches	Time (s)	Coverage %
Exact (Part 1)	17	0.13	1.39%
Subset (Part 2, first 100)	24	1286.91	1.96%
Optimized (Part 3)	186	6.50	15.24%
GA (Part 4.1)	186	5.95	15.24%
Fuzzy (Part 4.2)	0	3.99	0%
GA+Fuzzy (Part 4.3)	186	0.02	15.24%