import pandas as pd
import re

# ==== STEP 1: Load the data ====
data = [
    ["2TP - precondition 2TP - norm completeness 2FP - norm compliance pattern", "emergencies_scenario", "r1"],
    ["2TN - precondition 1TP - norm completeness 1FN - norm completeness 1TP - norm compliance pattern 1FN - norm compliance pattern", "emergencies_scenario", "r2"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "emergencies_scenario", "r3"],
    ["1TP - precondition 1FP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "emergencies_scenario", "r4"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "emergencies_scenario", "r5"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "emergencies_scenario", "r6"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "emergencies_scenario", "r7"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "SIM_card_scenario", "r8"],
    ["1TP - precondition 1FP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "SIM_card_scenario", "r9"],
    ["2TP - precondition 2TP - norm completeness 2FP - norm compliance pattern", "SIM_card_scenario", "r10"],
    ["1FN - precondition 1TP - precondition 1FN - norm completeness 1TP - norm completeness 1TP - norm compliance pattern 1FN - norm compliance pattern", "SIM_card_scenario", "r11"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "SIM_card_scenario", "r12"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "SIM_card_scenario", "r13"],
    ["1TP - precondition 1TN - precondition 2TP - norm completeness 2TP - norm compliance pattern", "blood_donation_scenario", "r14"],
    ["1FN - precondition 1TP - precondition 2TP - norm completeness 2TP - norm compliance patten", "blood_donation_scenario", "r15"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "blood_donation_scenario", "r16"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "blood_donation_scenario", "r17"],
    ["1TN - precondition 1FP - precondition", "blood_donation_scenario", "r18"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "blood_donation_scenario", "r19"],
    ["2TP - precondition 2TP - norm completeness 2TP - norm compliance pattern", "blood_donation_scenario", "r20"],
]

df = pd.DataFrame(data, columns=["clean_formalization_eval", "scenario", "requirement_id"])

# ==== STEP 2: Extract component-level TP/FP/FN counts ====

components = ["precondition", "norm completeness", "norm compliance pattern"]
label_types = ["TP", "FP", "FN"]

def extract_component_labels(text):
    counts = {f"{label}_{comp}": 0 for label in label_types for comp in components}
    matches = re.findall(r"(\d+)(TP|FP|FN) - ([a-zA-Z ]+)", text)
    for count, label, comp in matches:
        key = f"{label}_{comp.strip()}"
        if key in counts:
            counts[key] += int(count)
    return counts

component_df = df["clean_formalization_eval"].apply(extract_component_labels).apply(pd.Series)
df = df.join(component_df)

# ==== STEP 3: Compute metrics per scenario (total TP, FP, FN) ====

def compute_metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

scenario_results = []
for scenario, group in df.groupby("scenario"):
    TP = group[[f"TP_{c}" for c in components]].sum().sum()
    FP = group[[f"FP_{c}" for c in components]].sum().sum()
    FN = group[[f"FN_{c}" for c in components]].sum().sum()
    precision, recall, f1 = compute_metrics(TP, FP, FN)
    scenario_results.append({
        "scenario": scenario,
        "precision": precision,
        "recall": recall,
        "f1": f1
    })
df_totals = pd.DataFrame(scenario_results)

# ==== STEP 4: Compute metrics per scenario AND component ====

scenario_component_results = []
for scenario, group in df.groupby("scenario"):
    for comp in components:
        TP = group[f"TP_{comp}"].sum()
        FP = group[f"FP_{comp}"].sum()
        FN = group[f"FN_{comp}"].sum()
        precision, recall, f1 = compute_metrics(TP, FP, FN)
        scenario_component_results.append({
            "scenario": scenario,
            "component": comp,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
df_components = pd.DataFrame(scenario_component_results)

# ==== STEP 5: Show or export ====
print("=== TOTALS BY SCENARIO ===")
print(df_totals.to_string(index=False))

print("\n=== BY SCENARIO AND COMPONENT ===")
print(df_components.to_string(index=False))

# Save to CSV
# df_totals.to_csv("totals_by_scenario.csv", index=False)
# df_components.to_csv("metrics_by_scenario_and_component.csv", index=False)
