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
    winner_row = group.loc[group["votes"].idxmax()]
    return winner_row

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

print("\n=== Party-wise Seat Summary ===\n")
print(party_wins.reset_index(name='Seats Won').to_string(index=False))

# Check for a single-party majority
largest_party = party_wins.idxmax()
largest_seats = party_wins.max()

if largest_seats >= majority:
    print(f"\n🎉 The winner is {largest_party} with {largest_seats} seats!")
    print(f"They have a clear majority of {majority} seats.")
else:
    print("\n❌ No single party has a majority. Hung Assembly!")
    
    # Building a coalition
    print("\n🤝 Forming a coalition...")
    
    # Sort parties by seats won, excluding the largest one
    coalition_partners = party_wins.drop(largest_party).sort_values(ascending=False)
    
    current_coalition_seats = largest_seats
    allies = []
    
    for party, seats in coalition_partners.items():
        if current_coalition_seats < majority:
            allies.append(party)
            current_coalition_seats += seats
    
    if current_coalition_seats >= majority:
        print(f"✅ The most likely coalition is {largest_party} + {', '.join(allies)}.")
        print(f"Total seats: {current_coalition_seats} (a majority of {majority}).")
    else:
        print("❌ A coalition could not be formed to reach a majority.")