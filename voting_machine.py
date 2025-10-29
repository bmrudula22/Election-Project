import random
import numpy as np
from datetime import datetime, timedelta

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


class VotingMachine:
    """Each polling booth has one voting machine that simulates voting process."""
    def __init__(self, polling_booth_id, df_candidates, national_wave, constituency_tilt, candidate_quality):
        self.polling_booth_id = polling_booth_id
        self.df_candidates = df_candidates
        self.national_wave = national_wave
        self.constituency_tilt = constituency_tilt
        self.candidate_quality = candidate_quality
        self.poll_start = datetime.strptime("08:00:00", "%H:%M:%S")
        self.poll_end = datetime.strptime("17:00:00", "%H:%M:%S")
        self.NOTA_BASE = 0.01

    def weight_for_option(self, con_id, opt):
        """Same voting weight logic as before."""
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

    def cast_vote(self, voter):
        """Simulates a single voter using this booth's voting machine."""
        con_id = voter["CON_ID"]
        con_candidates = self.df_candidates[self.df_candidates["Constituency_ID"] == con_id]
        options = con_candidates.to_dict("records") + [{"Candidate_Name": "NOTA", "Party_Name": "NOTA"}]

        weights = self.normalized_weights(con_id, options)
        choice = random.choices(options, weights=weights, k=1)[0]

        entry_time = self.poll_start + timedelta(seconds=random.randint(0, int((self.poll_end - self.poll_start).total_seconds())))
        vote_duration = random.randint(1, 3)
        exit_time = entry_time + timedelta(minutes=vote_duration)

        return VotingDayRecord(
            con_id=voter["CON_ID"],
            polling_booth_id=voter["POLLING_BOOTH_ID"],
            voter_id=voter["Voter ID"],
            entry_time=entry_time.strftime("%H:%M:%S"),
            exit_time=exit_time.strftime("%H:%M:%S"),
            candidate_voted=choice["Candidate_Name"],
            party_voted=choice["Party_Name"]
        )