import pandas as pd

# Load the Excel file
file_path = "/home/marisolbarrientosmoreno/Desktop/ER_2025/repo/Requirements_Change_for_Business_Process_Compliance/ground_truth_sum_analysis_results/analysis_results_step_2_v2.xlsx"  # adjust path if needed
df = pd.read_excel(file_path)

# Group by change_level and compute TP, FP, and Precision
grouped = df.groupby("change_level")[["TP", "FP"]].sum()
grouped["Precision"] = grouped["TP"] / (grouped["TP"] + grouped["FP"])

# Fill NaNs (e.g., 0/0 cases) with 0
grouped = grouped.fillna(0)

# Print results
print("Precision per Change Level (L1–L4):\n")
print(grouped)

# Optional: save results to a CSV
grouped.to_csv("analysis_results_step_2.csv")
