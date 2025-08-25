import pandas as pd
import random
from datetime import datetime, timedelta
import time

# Timer Start
start_time = time.time()


class VotingDayRecord:
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

    # Randomly select candidate
    choice = random.choice(options)

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
df_final = pd.DataFrame()

print("✅ Voting polling day events created!")


# Timer End
end_time = time.time()
execution_time = end_time - start_time

print("Voting polling day events created with class-based structure!")
print(f"Execution Time: {execution_time:.4f} seconds")