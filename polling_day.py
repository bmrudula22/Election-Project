import pandas as pd
import random
from datetime import datetime, timedelta
import time
import numpy as np


# Timer Start
start_time = time.time()


class VotingDayRecord:
    random.seed(42)
    np.random.seed(42)
    def __init__(self, con_id, polling_booth_id, voter_id, entry_time, exit_time, candidate_voted, party_voted):
        self.con_id = con_id
        self.polling_booth_id = polling_booth_id
        self.voter_id = voter_id
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.candidate_voted = candidate_voted
        self.party_voted = party_voted

    def to_dict(self):
        return {
            "CON_ID": self.con_id,
            "POLLING_BOOTH_ID": self.polling_booth_id,
            "VOTER_ID": self.voter_id,
            "ENTRY_TIME": self.entry_time,
            "EXIT_TIME": self.exit_time,
            "CANDIDATE_VOTED": self.candidate_voted,
            "PARTY_VOTED": self.party_voted
        }


# Load existing voter file

df_voters = pd.read_csv("Data\\voter_table.csv")  # Your single CSV

# Load candidates file (already has Candidate_ID, Candidate_Name, Constituency_ID, Party_Name)
df_candidates = pd.read_csv("Data\\candidates.csv")

# ---- Election realism knobs (no manual party probabilities needed) ----
parties = sorted(df_candidates["Party_Name"].unique().tolist())

# National wave: one party randomly gets a mild to strong tailwind.
# Raise WAVE_STRENGTH_MAX for more single-party majorities, lower it for more hung assemblies.
WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX = 0.05, 0.50
wave_party = random.choices(parties)[0]
wave_strength = random.uniform(WAVE_STRENGTH_MIN, WAVE_STRENGTH_MAX)
national_wave = {p: (1.0 + wave_strength) if p == wave_party else 1.0 for p in parties}

# Constituency-specific tilt: each seat has its own favorite party & tilt strength.
# Strong seats ≈ 0.20–0.45; swing seats ≈ 0.00–0.15 (auto-chosen)
constituency_ids = sorted(df_candidates["Constituency_ID"].unique().tolist())
constituency_tilt = {}
for cid in constituency_ids:
    tilt_party = random.choices(parties)
    # mix of swing and strongholds
    tilt_strength = random.choices([random.uniform(0.00, 0.15),  # swingy
                                   random.uniform(0.20, 0.45)]) # stronghold
    constituency_tilt[cid] = (tilt_party, tilt_strength)

# Candidate quality: strong/weak candidates via a lognormal multiplier (center ~1.0)
candidate_quality = {}
if "Candidate_ID" in df_candidates.columns:
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_ID"]] = np.random.lognormal(mean=0.0, sigma=0.20)
else:
    # Fallback if Candidate_ID missing: use Candidate_Name as key
    for _, r in df_candidates.iterrows():
        candidate_quality[r["Candidate_Name"]] = np.random.lognormal(mean=0.0, sigma=0.20)

NOTA_BASE = 0.01  # ~1% baseline weight for NOTA

def weight_for_option(con_id, opt):
    # NOTA gets tiny, fixed weight
    if opt["Candidate_Name"] == "NOTA" and opt["Party_Name"] == "NOTA":
        return NOTA_BASE

    party = opt["Party_Name"]
    # pull candidate key (ID preferred; else name)
    cand_key = opt.get("Candidate_ID", opt["Candidate_Name"])

    w = 1.0
    # national wave factor
    w *= national_wave.get(party, 1.0)
    # constituency tilt factor
    tilt_party, tilt_strength = constituency_tilt[con_id]
    if party == tilt_party:
        w *= (1.0 + tilt_strength)
    # candidate quality
    w *= candidate_quality.get(cand_key, 1.0)
    return w

def normalized_weights(con_id, options):
    raw = [weight_for_option(con_id, o) for o in options]
    s = sum(raw)
    # guard against degenerate sums
    if s == 0:
        raw = [1.0 for _ in options]
        s = len(options)
    return [x / s for x in raw]

# Simulate voting day

turnout_fraction = 0.65  # 65% turnout
df_turnout = df_voters.sample(frac=turnout_fraction, random_state=42).reset_index(drop=True)

poll_start = datetime.strptime("08:00:00", "%H:%M:%S") # start time
poll_end = datetime.strptime("17:00:00", "%H:%M:%S")  # Polling end time


records = []


for _, voter in df_turnout.iterrows():
    con_id = voter["CON_ID"]

    # Get candidates for this voter's constituency
    con_candidates = df_candidates[df_candidates["Constituency_ID"] == con_id]

    # Add NOTA as an extra option
    options = con_candidates.to_dict("records") + [{"Candidate_Name": "NOTA", "Party_Name": "NOTA"}]

    weights = normalized_weights(con_id, options)
    # Pick candidate with probability
    choice = random.choices(options, weights=weights, k=1)[0]

    entry_time = poll_start + timedelta(seconds=random.randint(0, int((poll_end - poll_start).total_seconds())))
    vote_duration = random.randint(1, 3)
    exit_time = entry_time + timedelta(minutes=vote_duration)

   
    # Keep only required columns and add new ones

    record = VotingDayRecord(
        
        con_id=voter["CON_ID"],
        polling_booth_id=voter["POLLING_BOOTH_ID"],
        voter_id=voter["Voter ID"],
        entry_time=entry_time.strftime("%H:%M:%S"),
        exit_time=exit_time.strftime("%H:%M:%S"),
        candidate_voted=choice["Candidate_Name"],  
        party_voted=choice["Party_Name"]          
    )
    
    records.append(record.to_dict())

#Save final CSV
df_final = pd.DataFrame(records)

df_final.to_csv("Data\\polling_day.csv", index=False)
print("✅ Voting polling day events created!")


# Timer End
end_time = time.time()
execution_time = end_time - start_time

print("Voting polling day events created with class-based structure!")
print(f"Execution Time: {execution_time:.4f} seconds")