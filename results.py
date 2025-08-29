import pandas as pd
import matplotlib.pyplot as plt


# Load simulated voting results

votes_df = pd.read_csv("Data\\polling_day.csv")

# Find winners per constituency
# Count votes for each candidate in each constituency
results = (
    votes_df.groupby(["CON_ID", "CANDIDATE_VOTED", "PARTY_VOTED"])
    .size()
    .reset_index(name="votes")
)

# Find candidate with maximum votes in each constituency

def party_winner(group):
    max_votes = group["votes"].max()
    top_candidates = group[group["votes"] == max_votes]

    if len(top_candidates) > 1:
        print(f"Tie in {group['CON_ID'].iloc[0]}! Deciding by lottery...")
        return top_candidates.sample(1)  # random pick like real election
    else:
        return top_candidates

winners = results.groupby("CON_ID", group_keys=False).apply(party_winner)
# Constituency → Winning Candidate
table_result = winners[["CON_ID", "CANDIDATE_VOTED"]]
print("\n=== Election Results: Constituency vs Winning Candidate ===\n")
print(table_result.to_string(index=False))

# Party-wise wins
party_wins = winners["PARTY_VOTED"].value_counts()

# Pie Chart (Parties vs Seats Won)
plt.figure(figsize=(7, 7))
party_wins.plot.pie(autopct="%1.1f%%", startangle=140)
plt.title("Party-wise Constituency Wins")
plt.legend(party_wins.index, loc="best")
plt.ylabel("")
plt.savefig("party_piecharts.png", dpi=300, bbox_inches="tight")
plt.show()

# Majority party
total_seats = len(winners)# should be 8
majority = total_seats // 2 + 1          # 5 seats needed for majority

winner_party = None
for party, seats in party_wins.items():
    if seats >= majority:
        winner_party = party
        break

if winner_party:
    print(f"The party that can form government is: {winner_party}")
else:
    print("No single party has majority (Hung Assembly).")
    
summary_df = winners.groupby("PARTY_VOTED").size().reset_index(name="Seats Won")
print("\n=== Party-wise Seat Summary ===\n")
print(summary_df.to_string(index=False))