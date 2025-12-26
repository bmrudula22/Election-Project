import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# Setup argument parser
parser = argparse.ArgumentParser(description="Election Results Analyzer")
parser.add_argument("csv_file", help="Path to the Data/polling_day.csv file")
args = parser.parse_args()

# Validate file existence
if not os.path.exists(args.csv_file):
    print(f"❌ File not found: {args.csv_file}")
    exit(1)

# Load voting data
votes_df = pd.read_csv(args.csv_file)
# Count votes for each candidate in each constituency
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
        coalition_name = f"The {largest_party} Coalition"
        
        # Create a new party_wins entry for the coalition
        coalition_parties = [largest_party] + allies
        coalition_total_seats = sum(party_wins.loc[p] for p in coalition_parties)
        
        # Remove the individual parties and add the new coalition
        party_wins_final = party_wins.drop(coalition_parties)
        party_wins_final[coalition_name] = coalition_total_seats
        
        print("\n=== Final Winner: Coalition Government! ===\n")
        print(party_wins_final.reset_index(name="Seats Won").to_string(index=False))
        
        # You can also add code to re-plot the pie chart here
        # to show the coalition as a single entity
    else:
        print("❌ A coalition could not be formed to reach a majority.")