import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# Load voters dataset
df_voters = pd.read_csv("Data\\voter_table.xyz")

# List of realistic parties
parties = [
    "BJP", "INC", "AAP", "TDP", "BRS", "CPI", "CPM", 
    "YSRCP", "DMK", "SP", "BSP", "JD(U)"
]

candidates = []

# Get all constituencies
constituencies = df_voters['CON_ID'].unique()
total_candidates = 30
num_constituencies = len(constituencies)

# Determine how many candidates per constituency
base = total_candidates // num_constituencies
remainder = total_candidates % num_constituencies
candidates_per_con = [base + 1 if i < remainder else base for i in range(num_constituencies)]

for con_id, num_candidates in zip(constituencies, candidates_per_con ):
    voters_in_con = df_voters[df_voters['CON_ID'] == con_id].copy()

    # Randomly select parties without repetition
    selected_parties = random.sample(parties, num_candidates)

    # For each party, pick 1 random voter as candidate
    for party in selected_parties:
        voter = voters_in_con.sample(n=1).iloc[0]
        candidates.append({
            "Candidate_ID": voter["Voter ID"],
            "Candidate_Name": voter["Name"],
            "Constituency_ID": con_id,
            "Party_Name": party
        })

# Create DataFrame
df_candidates = pd.DataFrame(candidates)

df_candidates = df_candidates.sort_values(by=["Constituency_ID", "Party_Name"]).reset_index(drop=True)

# Save to CSV
df_candidates.to_csv("Data\\candidates.csv", index=False)

print("✅ Candidates dataset created successfully with 30 realistic candidates")