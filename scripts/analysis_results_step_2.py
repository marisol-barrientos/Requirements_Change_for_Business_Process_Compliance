import pandas as pd

# ---------------------------------------------------
# Unified DataFrame with levels and results
# ---------------------------------------------------
df = pd.DataFrame([
    ["r1",  "change_in_activity",         "L4", "TP"],
    ["r2",  "change_in_role",             "L4", "FP"],
    ["r3",  "change_in_role",             "L4", "FP"],
    ["r3",  "add_precondition",           "L2", "TP"],
    ["r3",  "delete_norm",                "L2", "FN"],
    ["r4",  "add_precondition",           "L2", "TP"],
    ["r5",  "change_modality",            "L3", "TP"],
    ["r6",  "add_precondition",           "L2", "TP"],
    ["r7",  "switch_compliance_pattern",  "L4", "TP"],
    ["r8",  "change_modality",            "L3", "TP"],
    ["r9",  "add_requirement",            "L1", "TP"],
    ["r10", "change_in_role",             "L4", "FN"],
    ["r11", "change_modality",            "L3", "TP"],
    ["r11", "switch_pattern",             "L4", "TP"],
    ["r11", "add_norm",                   "L2", "TP"],
    ["r12", "delete_requirement",         "L1", "TP"],
    ["r13", "change_in_data",             "L4", "TP"],
    ["r14", "delete_precondition",        "L2", "TP"],
    ["r15", "delete_norm",                "L2", "FN"],
    ["r16", "delete_requirement",         "L1", "TP"],
    ["r17", "change_time_constraint",     "L4", "TP"],
    ["r17", "delete_action",              "L3", "TP"],
    ["r17", "delete_norm",                "L2", "TP"],
    ["r18", "add_requirement",            "L1", "TP"],
    ["r19", "change_modality",            "L3", "TP"],
    ["r20", "changed_logical_operator",   "L3", "FP"],
], columns=["requirement_id", "change_type", "level", "result"])


# ---------------------------------------------------
# Compute metrics per level
# ---------------------------------------------------
rows = []

for level in sorted(df["level"].unique()):
    sub = df[df["level"] == level]

    TP = (sub["result"] == "TP").sum()
    FP = (sub["result"] == "FP").sum()
    FN = (sub["result"] == "FN").sum()

    # Precision
    precision = TP / (TP + FP) if (TP + FP) > 0 else None

    # Recall
    recall = TP / (TP + FN) if (TP + FN) > 0 else None

    # F1-score
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = None

    rows.append([level, TP, FP, FN, precision, recall, f1])

results = pd.DataFrame(rows, columns=["level", "TP", "FP", "FN", "precision", "recall", "f1_score"])

print("\n=== METRICS PER LEVEL ===")
print(results.to_string(index=False))

output_path = "/evaluation/analysis_of_results/analyzed/analysis_results_step_2_by_level.xlsx"

results.to_excel(output_path, index=False)

print(f"\nSaved metrics to: {output_path}")
