import pandas as pd
import random

# Load voters dataset
df_voters = pd.read_csv("voter_table.csv")

# List of realistic parties
parties = [
    "BJP", "INC", "AAP", "TDP", "BRS", "CPI", "CPM", 
    "YSRCP", "DMK", "AIADMK", "SP", "BSP", "JD(U)", "Independent"
]

# Pick ~30 random candidates from voter dataset
df_candidates = df_voters.sample(n=30, random_state=42)[['Voter ID', 'Name', 'CON_ID']]

# Assign random party to each candidate
df_candidates['Party_Name'] = [random.choice(parties) for _ in range(len(df_candidates))]

# Rename columns for candidate dataset
df_candidates = df_candidates.rename(columns={
    'Voter ID': 'Candidate_ID',
    'Name': 'Candidate_Name',
    'CON_ID': 'Constituency_ID'
})

# Save to CSV
df_candidates.to_csv("candidates.csv", index=False)

print("✅ Candidates dataset created successfully with 30 realistic candidates")