import pandas as pd

base = r"C:\Users\ctint\Desktop\Scripts\repo_candidate\motif_results_robustness\peripheral_95"
df0 = pd.read_csv(base + r"\null_samples_candidate_0.csv")

print(df0.head())
print(df0.columns)