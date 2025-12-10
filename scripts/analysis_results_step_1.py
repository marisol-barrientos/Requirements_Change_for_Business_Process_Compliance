import pandas as pd
import re
from collections import defaultdict

# === Step 1: Load the Excel file ===
file_path = "/home/marisolbarrientosmoreno/Desktop/ER_2025/repo/Requirements_Change_for_Business_Process_Compliance/ground_truth_sum_analysis_results/analysis_results_step_1.xlsx"
df = pd.read_excel(file_path)

# === Step 2: Assign scenario based on requirement_id ===
def get_scenario(req_id):
    num = int(req_id[1:])
    if 1 <= num <= 7:
        return "emergencies_scenario"
    elif 8 <= num <= 13:
        return "SIM_card_scenario"
    elif 14 <= num <= 20:
        return "blood_donation_scenario"
    else:
        return "unknown"

df["scenario"] = df["requirement_id"].apply(get_scenario)

# === Step 3: Parse each annotation line ===
def parse_lines_simple(text):
    counts = defaultdict(float)
    if pd.isna(text):
        return counts
    for line in str(text).splitlines():
        match = re.match(r'(\d+)([A-Z]+)\s*-\s*(precondition|norm)', line.strip(), re.IGNORECASE)
        if match:
            count = int(match.group(1))
            label = match.group(2).upper()
            target = match.group(3).lower()
            counts[(target, label)] += count
    return counts

# === Step 4: Compute metrics with optional TN ===
def compute_all_metrics(tp, fp, fn, tn=None):
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    accuracy = (tp + tn) / (tp + fp + fn + tn) if tn is not None and (tp + fp + fn + tn) else 0
    specificity = tn / (tn + fp) if tn is not None and (tn + fp) else 0
    balanced_accuracy = (recall + specificity) / 2 if tn is not None else None
    return precision, recall, f1, accuracy, specificity, balanced_accuracy

# === Step 5: Evaluate per scenario ===
for scenario, group in df.groupby("scenario"):
    print(f"\n=== Scenario: {scenario} ===")
    totals = defaultdict(float)

    for _, row in group.iterrows():
        counts = parse_lines_simple(row["clean_formalization_eval_v2"])
        for key, value in counts.items():
            totals[key] += value

    for target in ["precondition", "norm"]:
        tp = totals[(target, "TP")]
        fp = totals[(target, "FP")]
        fn = totals[(target, "FN")]
        tn = totals[(target, "TN")] if (target, "TN") in totals else None

        precision, recall, f1, accuracy, specificity, balanced_accuracy = compute_all_metrics(tp, fp, fn, tn)

        print(f"\nTarget: {target.capitalize()}")
        print(f"  TP = {tp}, FP = {fp}, FN = {fn}" + (f", TN = {tn}" if tn is not None else ""))
        print(f"  Precision (correctness)      = {precision:.3f}")
        print(f"  Recall (completeness)        = {recall:.3f}")
        print(f"  F1-score                     = {f1:.3f}")
        if tn is not None:
            print(f"  Accuracy                     = {accuracy:.3f}")
            print(f"  Specificity (true negative)  = {specificity:.3f}")
            print(f"  Balanced Accuracy            = {balanced_accuracy:.3f}")
