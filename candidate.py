import pandas as pd
import random

# Load voters dataset
df_voters = pd.read_csv("voter_table.csv")

# List of realistic parties
parties = [
    "BJP", "INC", "AAP", "TDP", "BRS", "CPI", "CPM", 
    "YSRCP", "DMK", "AIADMK", "SP", "BSP", "JD(U)", "Independent"
]

candidates = []

# Loop through each constituency
for con_id in df_voters['CON_ID'].unique():
    # Get voters belonging to this constituency
    voters_in_con = df_voters[df_voters['CON_ID'] == con_id]

    # Decide number of candidates (between 3 and 5)
    num_candidates = random.randint(3, 5)

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

# Save to CSV
df_candidates.to_csv("candidates.csv", index=False)

print("✅ Candidates dataset created successfully with 30 realistic candidates")