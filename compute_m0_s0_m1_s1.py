import pandas as pd

base = r"C:\Users\ctint\Desktop\Scripts\repo_candidate\motif_results_robustness\peripheral_95"

df0 = pd.read_csv(base + r"\null_samples_candidate_0.csv", skiprows=3)
df1 = pd.read_csv(base + r"\null_samples_candidate_1.csv", skiprows=3)

m0 = df0['T_null'].mean()
s0 = df0['T_null'].std()

m1 = df1['T_null'].mean()
s1 = df1['T_null'].std()

print("m0 =", m0)
print("s0 =", s0)
print("m1 =", m1)
print("s1 =", s1)