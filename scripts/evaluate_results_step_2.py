import pandas as pd
import re

# === Data ===
data = [
    ["emergencies_scenario", "r1", "1/2 TP\n1/2 FP"],
    ["emergencies_scenario", "r2", "1FP"],
    ["emergencies_scenario", "r3", "1/2 TP\n1/2 FP"],
    ["emergencies_scenario", "r4", "1/2 TP\n1/2 FP"],
    ["emergencies_scenario", "r5", "1TP"],
    ["emergencies_scenario", "r6", "1TP"],
    ["emergencies_scenario", "r7", "1/2 TP\n1/2 FP"],
    ["SIM_card_scenario", "r8", "1/2 TP\n1/2 FP"],
    ["SIM_card_scenario", "r9", "-"],
    ["SIM_card_scenario", "r10", "1FP"],
    ["SIM_card_scenario", "r11", "1TP"],
    ["SIM_card_scenario", "r12", "-"],
    ["SIM_card_scenario", "r13", "1TP"],
    ["blood_donation_scenario", "r14", "1TP"],
    ["blood_donation_scenario", "r15", "1FP"],
    ["blood_donation_scenario", "r16", "-"],
    ["blood_donation_scenario", "r17", "1TP"],
    ["blood_donation_scenario", "r18", "-"],
    ["blood_donation_scenario", "r19", "1TP"],
    ["blood_donation_scenario", "r20", "1FP"]
]

df = pd.DataFrame(data, columns=["scenario", "requirement_id", "clean_delta_eval"])

# === Function to parse TP/FP/FN ===
def parse_delta_eval(cell):
    counts = {"TP": 0.0, "FP": 0.0, "FN": 0.0}
    if isinstance(cell, str):
        matches = re.findall(r"([\d/]+)\s*(TP|FP|FN)", cell)
        for val, label in matches:
            if '/' in val:
                num, denom = map(int, val.split('/'))
                counts[label] += num / denom
            else:
                counts[label] += int(val)
    return counts

# === Apply parsing ===
parsed_df = df["clean_delta_eval"].apply(parse_delta_eval).apply(pd.Series)
df = df.join(parsed_df)

# === Compute metrics per scenario ===
def compute_metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

# === Print results ===
print("\n=== Delta Evaluation Metrics by Scenario ===")
for scenario, group in df.groupby("scenario"):
    TP = group["TP"].sum()
    FP = group["FP"].sum()
    FN = group["FN"].sum()
    precision, recall, f1 = compute_metrics(TP, FP, FN)
    print(f"\nScenario: {scenario}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
