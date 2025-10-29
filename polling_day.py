import pandas as pd
import random
import time
import numpy as np
import argparse
import matplotlib.pyplot as plt
from voting_machine import VotingMachine  # Import the VotingMachine class

# Timer Start
start_time = time.time()
parser = argparse.ArgumentParser(description="Simulate voting day for given year(s)")
parser.add_argument('--year', type=int, help='Single election year to simulate')
parser.add_argument('--from_year', type=int, help='Start year for multi-year simulation')
parser.add_argument('--to_year', type=int, help='End year for multi-year simulation')
args = parser.parse_args()

# Determine which years to simulate
if args.from_year and args.to_year:
    years = range(args.from_year, args.to_year + 1)
elif args.year:
    years = [args.year]
else:
    from datetime import datetime
    years = [datetime.now().year]  # default year if not specified

for year in years:
    print(f"\n🗳️ Simulating election for year: {year}")
    
# Use the election year as a seed so same year always gives same results
random.seed(year)
np.random.seed(year)

# Load voter and candidate data
df_voters = pd.read_csv("Data\\voter_table.csv")
df_candidates = pd.read_csv("Data\\candidates.csv")

# ---- Election realism knobs ----
parties = sorted(df_candidates["Party_Name"].unique().tolist())

WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX = 0.05, 0.50
wave_party = random.choices(parties)[0]
wave_strength = random.uniform(WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX)
national_wave = {p: (1.0 + wave_strength) if p == wave_party else 1.0 for p in parties}

constituency_ids = sorted(df_candidates["Constituency_ID"].unique().tolist())
constituency_tilt = {}
for cid in constituency_ids:
    tilt_party = random.choices(parties)
    tilt_strength = random.choices([random.uniform(0.00, 0.15), random.uniform(0.20, 0.45)])
    constituency_tilt[cid] = (tilt_party, tilt_strength)

candidate_quality = {}
if "Candidate_ID" in df_candidates.columns:
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_ID"]] = np.random.lognormal(mean=0.0, sigma=0.20)
else:
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_Name"]] = np.random.lognormal(mean=0.0, sigma=0.20)

# ---- Voting Simulation ----
turnout_fraction = 0.65
df_turnout = df_voters.sample(frac=turnout_fraction, random_state=42).reset_index(drop=True)

# Create one voting machine per polling booth
polling_booths = df_turnout["POLLING_BOOTH_ID"].unique()
machines = {
    pb: VotingMachine(pb, df_candidates, national_wave, constituency_tilt, candidate_quality)
    for pb in polling_booths
}

records = []

# Each voter uses the machine assigned to their polling booth
for _, voter in df_turnout.iterrows():
    machine = machines[voter["POLLING_BOOTH_ID"]]
    record = machine.cast_vote(voter)
    records.append(record.to_dict())

# Save final CSV
df_final = pd.DataFrame(records)
output_path = f"Data\\polling_day_{year}.csv"
df_final.to_csv(output_path, index=False)
print(f"✅ Voting polling day events created for {year}!")

# Aggregate vote share for this year
vote_counts = df_final["PARTY_VOTED"].value_counts(normalize=True) * 100
vote_summary = vote_counts.reset_index()
vote_summary.columns = ["Party", "Vote_Share"]
vote_summary["Year"] = year

summary_path = "Data\\vote_share_by_year.csv"

try:
    df_existing = pd.read_csv(summary_path)
    df_existing = df_existing[df_existing["Year"] != year]
    df_combined = pd.concat([df_existing, vote_summary], ignore_index=True)
except FileNotFoundError:
    df_combined = vote_summary

df_combined.to_csv(summary_path, index=False)
print("📊 Vote share summary updated!")


df_combined.to_csv(summary_path, index=False)
print("📊 Vote share summary updated!")

# ---- Plot Multi-Year Vote Share ----
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

# Timer End
end_time = time.time()
execution_time = end_time - start_time

print("Voting polling day events created with class-based structure!")
print(f"Execution Time: {execution_time:.4f} seconds")