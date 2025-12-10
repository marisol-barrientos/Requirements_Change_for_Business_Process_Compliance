import pandas as pd
import re
from collections import defaultdict

# === Step 1: Load data from Excel file ===
file_path = "/home/marisolbarrientosmoreno/Desktop/ER_2025/repo/Requirements_Change_for_Business_Process_Compliance/evaluation/analysis_of_results/to_analyze/results_step_3.xlsx"  # Adjust path if needed
df = pd.read_excel(file_path)

# === Step 2: Helper to extract TP, FP, FN ===
def extract_counts(field):
    counts = defaultdict(float)
    if pd.isna(field):
        return counts
    entries = re.split(r',\s*', str(field))
    for entry in entries:
        match = re.match(r'(\d+)(?:/(\d+))?([A-Z]+)', entry)
        if match:
            if match.group(2):  # Fraction like 1/2TP
                num = float(match.group(1)) / float(match.group(2))
                label = match.group(3)
                counts[label] += num
                if label == 'TP':
                    counts['FP'] += num  # ambiguous true positive also contributes to FP
                elif label == 'FN':
                    counts['TP'] += num  # ambiguous false negative also contributes to TP
                # You can extend this if needed
            else:
                num = float(match.group(1))
                label = match.group(3)
                counts[label] += num
    return counts


# === Step 3: Aggregate TP/FP/FN ===
def aggregate_confusion(row):
    tp = fp = fn = 0.0
    for field in [row['deviation_type'], row['reasoning_about_root_cause'], row['reference_in_model']]:
        counts = extract_counts(field)
        tp += counts['TP']
        fp += counts['FP']
        fn += counts['FN']
    return pd.Series({'TP': tp, 'FP': fp, 'FN': fn})

df[['TP', 'FP', 'FN']] = df.apply(aggregate_confusion, axis=1)

# === Step 4: Compute metrics per row ===
df['precision'] = df['TP'] / (df['TP'] + df['FP'])
df['recall'] = df['TP'] / (df['TP'] + df['FN'])
df['f1'] = 2 * df['precision'] * df['recall'] / (df['precision'] + df['recall'])
df.fillna({'precision': 0.0, 'recall': 0.0, 'f1': 0.0}, inplace=True)

# === Step 5: Normalize 'non_impacting_changes?' column ===
df['non_impacting_changes?'] = df['non_impacting_changes?'].astype(str).str.strip().str.lower()

# === Step 6: Metrics per (scenario, execution) ===
metrics_per_exec = (
    df.groupby(['scenario_id', 'execution_id'])
    .agg({
        'precision': 'mean',
        'recall': 'mean',
        'f1': 'mean',
        'non_impacting_changes?': lambda x: (x == 'false').mean() * 100
    })
    .rename(columns={'non_impacting_changes?': '%_non_impacting_FALSE'})
    .reset_index()
)

# === Step 7: Aggregate per execution ===
agg_per_execution = (
    metrics_per_exec.groupby('execution_id')
    .agg({
        'precision': ['mean', 'std'],
        'recall': ['mean', 'std'],
        'f1': ['mean', 'std'],
        '%_non_impacting_FALSE': ['mean', 'std']
    })
)
agg_per_execution.columns = ['_'.join(col).strip() for col in agg_per_execution.columns.values]
agg_per_execution = agg_per_execution.reset_index()

# === Step 8: Aggregate per scenario ===
agg_per_scenario = (
    metrics_per_exec.groupby('scenario_id')
    .agg({
        'precision': ['mean', 'std'],
        'recall': ['mean', 'std'],
        'f1': ['mean', 'std'],
        '%_non_impacting_FALSE': ['mean', 'std']
    })
)
agg_per_scenario.columns = ['_'.join(col).strip() for col in agg_per_scenario.columns.values]
agg_per_scenario = agg_per_scenario.reset_index()

# === Step 9: Save all three to Excel ===
output_file = "/home/marisolbarrientosmoreno/Desktop/ER_2025/repo/Requirements_Change_for_Business_Process_Compliance/evaluation/analysis_of_results/analyzed/analyzed_results_step_3.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    metrics_per_exec.to_excel(writer, sheet_name="Per Scenario Execution", index=False)
    agg_per_execution.to_excel(writer, sheet_name="Aggregated Per Execution", index=False)
    agg_per_scenario.to_excel(writer, sheet_name="Aggregated Per Scenario", index=False)

print(f" All results written to '{output_file}' with 3 sheets.")
