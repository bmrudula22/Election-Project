import pandas as pd
import random
from datetime import datetime, timedelta
import time
import numpy as np
import argparse
import matplotlib.pyplot as plt
from voting_machine import VotingMachine

# Timer Start
start_time = time.time()
parser = argparse.ArgumentParser(description="Simulate voting day for a given year")
parser.add_argument('--year', type=int, required=True, help='Election year to simulate')
args = parser.parse_args()
year = args.year

# Load data
df_voters = pd.read_csv("Data\\voter_table.csv")
df_candidates = pd.read_csv("Data\\candidates.csv")

# Setup realism knobs
parties = sorted(df_candidates["Party_Name"].unique())
WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX = 0.05, 0.50
wave_party = random.choice(parties)
wave_strength = random.uniform(WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX)
national_wave = {p: (1.0 + wave_strength) if p == wave_party else 1.0 for p in parties}

constituency_ids = sorted(df_candidates["Constituency_ID"].unique())
constituency_tilt = {}
for cid in constituency_ids:
    tilt_party = random.choice(parties)
    tilt_strength = random.choice([random.uniform(0.00, 0.15), random.uniform(0.20, 0.45)])
    constituency_tilt[cid] = (tilt_party, tilt_strength)

candidate_quality = {}
if "Candidate_ID" in df_candidates.columns:
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_ID"]] = np.random.lognormal(mean=0.0, sigma=0.20)
else:
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_Name"]] = np.random.lognormal(mean=0.0, sigma=0.20)

# Voting parameters
turnout_fraction = 0.65
df_turnout = df_voters.sample(frac=turnout_fraction, random_state=42).reset_index(drop=True)
poll_start = datetime.strptime("08:00:00", "%H:%M:%S")
poll_end = datetime.strptime("17:00:00", "%H:%M:%S")

# Count polling booths
num_polling_booths = df_voters["POLLING_BOOTH_ID"].nunique()
print(f"🗳️ Simulating {num_polling_booths} voting machines — one per polling booth.")

# Initialize machine
machine = VotingMachine(
    df_candidates=df_candidates,
    national_wave=national_wave,
    constituency_tilt=constituency_tilt,
    candidate_quality=candidate_quality,
    poll_start=poll_start,
    poll_end=poll_end
)

# Simulate booth-by-booth with delays
records = []
grouped = df_turnout.groupby("POLLING_BOOTH_ID")
for booth_id, voters in grouped:
    booth_delay = timedelta(minutes=random.randint(0, 15))
    for _, voter in voters.iterrows():
        record = machine.simulate_vote(voter, booth_delay=booth_delay)
        records.append(record)

# Save polling day results
df_final = pd.DataFrame(records)
output_path = f"Data\\polling_day_{year}.csv"
df_final.to_csv(output_path, index=False)
print(f"✅ Voting polling day events created for {year}!")

# Vote share summary
vote_counts = df_final["PARTY_VOTED"].value_counts(normalize=True) * 100
vote_summary = vote_counts.reset_index()
vote_summary.columns = ["Party", "Vote_Share"]
vote_summary["Year"] = year

summary_path = "Data\\vote_share_by_year.csv"
try:
    df_existing = pd.read_csv(summary_path)
    if year in df_existing["Year"].values:
        print(f"⚠️ Vote share for {year} already exists. Skipping append.")
        df_combined = df_existing
    else:
        df_combined = pd.concat([df_existing, vote_summary], ignore_index=True)
        df_combined.to_csv(summary_path, index=False)
        print("📊 Vote share summary updated!")
except FileNotFoundError:
    df_combined = vote_summary
    df_combined.to_csv(summary_path, index=False)
    print("📊 Vote share summary created!")

# Plot vote share trend
df = pd.read_csv("Data\\vote_share_by_year.csv")
parties = sorted(df["Party"].unique())
years = sorted(df["Year"].unique())
x = np.arange(len(years))
bar_width = 0.8 / len(parties)

for i, party in enumerate(parties):
    shares = [df[(df["Year"] == y) & (df["Party"] == party)]["Vote_Share"].sum() for y in years]
    offset = x + i * bar_width
    plt.bar(offset, shares, width=bar_width, label=party)

plt.xlabel("Election Year")
plt.ylabel("Vote Share (%)")
plt.title("Multi-Year Vote Share Trend")
plt.xticks(x + bar_width * (len(parties) / 2), years)
plt.legend()
plt.tight_layout()
plt.show()

# Final stats
end_time = time.time()
print(f"🧮 Total votes cast: {machine.vote_count}")
print(f"⏱️ Execution Time: {end_time - start_time:.2f} seconds")