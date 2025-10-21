import random
from datetime import datetime, timedelta
import numpy as np

class VotingMachine:
    def __init__(self, df_candidates, national_wave, constituency_tilt, candidate_quality, poll_start, poll_end):
        self.df_candidates = df_candidates
        self.national_wave = national_wave
        self.constituency_tilt = constituency_tilt
        self.candidate_quality = candidate_quality
        self.poll_start = poll_start
        self.poll_end = poll_end
        self.NOTA_BASE = 0.01
        self.vote_count = 0

    def weight_for_option(self, con_id, opt):
        if opt["Candidate_Name"] == "NOTA" and opt["Party_Name"] == "NOTA":
            return self.NOTA_BASE

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

    def simulate_vote(self, voter, booth_delay=None):
        self.vote_count += 1
        con_id = voter["CON_ID"]
        con_candidates = self.df_candidates[self.df_candidates["Constituency_ID"] == con_id]
        options = con_candidates.to_dict("records") + [{"Candidate_Name": "NOTA", "Party_Name": "NOTA"}]
        weights = self.normalized_weights(con_id, options)
        choice = random.choices(options, weights=weights, k=1)[0]

        delay = booth_delay if booth_delay else timedelta(minutes=0)
        entry_time = self.poll_start + delay + timedelta(seconds=random.randint(0, int((self.poll_end - self.poll_start).total_seconds())))
        vote_duration = random.randint(1, 3)
        exit_time = entry_time + timedelta(minutes=vote_duration)

        return {
            "CON_ID": voter["CON_ID"],
            "POLLING_BOOTH_ID": voter["POLLING_BOOTH_ID"],
            "VOTER_ID": voter["Voter ID"],
            "ENTRY_TIME": entry_time.strftime("%H:%M:%S"),
            "EXIT_TIME": exit_time.strftime("%H:%M:%S"),
            "CANDIDATE_VOTED": choice["Candidate_Name"],
            "PARTY_VOTED": choice["Party_Name"]
        }