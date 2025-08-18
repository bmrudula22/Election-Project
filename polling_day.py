import pandas as pd
import random
from datetime import datetime, timedelta

# Step 1: Load existing voter file

df_voters = pd.read_csv("voter_table.csv")  # Your single CSV


# Step 2: Enter candidates manually

num_candidates = int(input("Enter number of candidates: "))
candidates = [input(f"Enter name of candidate {i+1}: ") for i in range(num_candidates)]
print("Candidates contesting are:", candidates)


# Step 3: Simulate voting day

turnout_fraction = 0.65  # 60% turnout
df_turnout = df_voters.sample(frac=turnout_fraction, random_state=42).reset_index(drop=True)

poll_start = datetime.strptime("08:00:00", "%H:%M:%S") # start time
poll_end = datetime.strptime("17:00:00", "%H:%M:%S")  # Polling end time
entry_times = []
exit_times = []
votes = []

for _ in range(len(df_turnout)):

    entry = poll_start + timedelta(seconds=random.randint(0, int((poll_end - poll_start).total_seconds())))
    vote_duration = random.randint(1, 3)
    exit_time = entry + timedelta(minutes=vote_duration)

    # Assign random candidate
    candidate = random.choice(candidates)

    # Append to lists
    entry_times.append(entry.strftime("%H:%M:%S"))
    exit_times.append(exit_time.strftime("%H:%M:%S"))
    votes.append(candidate)

    # Update start_time for next voter
    start_time = exit_time

# Step 4: Keep only required columns and add new ones

df_final = pd.DataFrame({
    "CON_ID": df_turnout["CON_ID"],
    "POLLING_BOOTH_ID": df_turnout["POLLING_BOOTH_ID"],
    "VOTER_ID": df_turnout["Voter ID"],
    "ENTRY_TIME": entry_times,
    "EXIT_TIME": exit_times,
    "CANDIDATE_VOTED": votes
})

# Step 5: Save final CSV

df_final.to_csv("polling_day.csv", index=False)

print("✅ Voting polling day events created!")