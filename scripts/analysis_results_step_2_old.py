import pandas as pd

# Load the Excel file
file_path = "/evaluation/analysis_of_results/to_analyze/results_step_2_old.xlsx"
df = pd.read_excel(file_path)

# Group by change_level and compute TP, FP, and Precision
grouped = df.groupby("change_level")[["TP", "FP"]].sum()
grouped["Precision"] = grouped["TP"] / (grouped["TP"] + grouped["FP"])

# Fill NaNs (e.g., 0/0 cases) with 0
grouped = grouped.fillna(0)

# Print results
print("Precision per Change Level (L1–L4):\n")
print(grouped)

# Save results to Excel (.xlsx or .xls)
grouped.to_excel("analysis_results_step_2.xlsx")  # or use .xls if preferred
