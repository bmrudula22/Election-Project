import pandas as pd
import random
import numpy as np
import argparse
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class VotingMachine:
    def __init__(self, df_candidates, national_wave, constituency_tilt, candidate_quality, poll_start, poll_end):
        self.df_candidates = df_candidates
        self.national_wave = national_wave
        self.constituency_tilt = constituency_tilt
        self.candidate_quality = candidate_quality
        self.poll_start = poll_start
        self.poll_end = poll_end
        self.nota_base = 0.01

    def weight_for_option(self, con_id, opt):
        if opt["Candidate_Name"] == "NOTA" and opt["Party_Name"] == "NOTA":
            return self.nota_base

        party = opt["Party_Name"]
        cand_key = opt.get("Candidate_ID", opt["Candidate_Name"])

        w = 1.0
        w *= self.national_wave.get(party, 1.0)
        tilt_party, tilt_strength = self.constituency_tilt[con_id]
        if party == tilt_party:
            w *= (1.0 + tilt_strength)
        w *= self.candidate_quality.get(cand_key, 1.0)
        return w

    def normalized_weights(self, con_id, options):
        raw = [self.weight_for_option(con_id, o) for o in options]
        s = sum(raw)
        if s == 0:
            raw = [1.0 for _ in options]
            s = len(options)
        return [x / s for x in raw]

    def simulate_vote(self, voter):
        con_id = voter["CON_ID"]
        con_candidates = self.df_candidates[self.df_candidates["Constituency_ID"] == con_id]
        options = con_candidates.to_dict("records") + [{"Candidate_Name": "NOTA", "Party_Name": "NOTA"}]
        weights = self.normalized_weights(con_id, options)
        choice = random.choices(options, weights=weights, k=1)[0]

        entry_time = self.poll_start + timedelta(seconds=random.randint(0, int((self.poll_end - self.poll_start).total_seconds())))
        vote_duration = random.randint(1, 3)
        exit_time = entry_time + timedelta(minutes=vote_duration)

        return {
            "CON_ID": voter["CON_ID"],
            "POLLING_BOOTH_ID": voter["POLLING_BOOTH_ID"],
            "VOTER_ID": voter["Voter ID"],
            "ENTRY_TIME": entry_time.strftime("%H:%M:%S"),
            "EXIT_TIME": exit_time.strftime("%H:%M:%S"),
            "CANDIDATE_VOTED": choice["Candidate_Name"],
            "PARTY_VOTED": choice["Party_Name"],
            "MACHINE_ID": voter.get("MACHINE_ID", "M1")  # Include machine ID in output
        }

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
wave_party = random.choice(parties)
wave_strength = random.uniform(0.05, 0.50)
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

# Simulate voting with multiple voting machines
turnout_fraction = 0.65
df_turnout = df_voters.sample(frac=turnout_fraction, random_state=42).reset_index(drop=True)

poll_start = datetime.strptime("08:00:00", "%H:%M:%S")
poll_end = datetime.strptime("17:00:00", "%H:%M:%S")

# Number of voting machines per polling booth
NUM_MACHINES_PER_BOOTH = 3  # Adjustable parameter

# Assign voters to machines within each polling booth
records = []
polling_booths = df_turnout["POLLING_BOOTH_ID"].unique()

for booth_id in polling_booths:
    booth_voters = df_turnout[df_turnout["POLLING_BOOTH_ID"] == booth_id].copy()
    num_voters = len(booth_voters)
    
    # Create multiple voting machines for this booth
    machines = [VotingMachine(df_candidates, national_wave, constituency_tilt, candidate_quality, poll_start, poll_end) 
                for _ in range(NUM_MACHINES_PER_BOOTH)]
    
    # Assign voters to machines
    machine_ids = [f"M{i+1}" for i in range(NUM_MACHINES_PER_BOOTH)]
    booth_voters["MACHINE_ID"] = [random.choice(machine_ids) for _ in range(num_voters)]
    
    # Simulate votes for each machine
    for machine_id, machine in zip(machine_ids, machines):
        machine_voters = booth_voters[booth_voters["MACHINE_ID"] == machine_id]
        for _, voter in machine_voters.iterrows():
            vote = machine.simulate_vote(voter)
            records.append(vote)

# Save results
df_final = pd.DataFrame(records)
output_path = f"Data\\polling_day_{year}.csv"
df_final.to_csv(output_path, index=False)
print(f"✅ Voting polling day events created for {year} with {NUM_MACHINES_PER_BOOTH} machines per booth!")

# Aggregate vote share
vote_counts = df_final["PARTY_VOTED"].value_counts(normalize=True) * 100
vote_summary = vote_counts.reset_index()
vote_summary.columns = ["Party", "Vote_Share"]
vote_summary["Year"] = year

summary_path = "Data\\vote_share_by_year.csv"
try:
    df_existing = pd.read_csv(summary_path)
    df_combined = pd.concat([df_existing, vote_summary], ignore_index=True)
except FileNotFoundError:
    df_combined = vote_summary

df_combined.to_csv(summary_path, index=False)
print("📊 Vote share summary updated!")

# Plotting
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
print(f"Execution Time: {end_time - start_time:.2f} seconds")