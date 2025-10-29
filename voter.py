import pandas as pd
from datetime import datetime
import random
import math
import numpy as np

random.seed(42)
np.random.seed(42)

def generate_voters():
    print("🔄 Generating voter_table.csv...")

    # === Step 1: Read the voters dataset which has DOB ===
    df_voters = pd.read_csv("Data/Voter_Card.csv")

    # Ensure DOB is in datetime format
    df_voters['DOB'] = pd.to_datetime(df_voters['DOB'], errors='coerce')

    # === Step 2: Calculate Age from DOB ===
    def calculate_age(dob):
        reference_date = datetime(2025, 1, 1)
        if pd.isnull(dob):
            return None
        age = reference_date.year - dob.year - (
            (reference_date.month, reference_date.day) < (dob.month, dob.day)
        )
        return age

    df_voters['Age'] = df_voters['DOB'].apply(calculate_age)
    
          

    # === Step 3: Create simplified voter card (optional intermediate file) ===
    df_voter_card = df_voters[['Voter ID', 'Name', 'Gender', 'Age']]
    df_voter_card.to_csv("Data/voter_card_details.csv", index=False)

    # === Step 4: Read Polling Booths ===
    df_booths = pd.read_csv("Data/polling_booths.csv")[['CON_ID', 'POLLING_BOOTH_ID']]

    num_voters = len(df_voters)
    num_booths = len(df_booths)

    # Repeat each booth enough times to cover all voters
    repeat_count = math.ceil(num_voters / num_booths)
    booth_assignment_list = list(df_booths['POLLING_BOOTH_ID']) * repeat_count
    booth_assignment_list = booth_assignment_list[:num_voters]
    random.shuffle(booth_assignment_list)

    # Assign booths to voters
    df_voters['POLLING_BOOTH_ID'] = booth_assignment_list

    # Map CON_ID from booth
    booth_map = df_booths.set_index('POLLING_BOOTH_ID')[['CON_ID']].to_dict(orient='index')
    df_voters['CON_ID'] = df_voters['POLLING_BOOTH_ID'].map(lambda x: booth_map[x]['CON_ID'])

    # === Step 5: Create voter_table.csv ===
    df_table = df_voters[['CON_ID', 'POLLING_BOOTH_ID', 'Voter ID', 'Name', 'Gender', 'Age']]
    df_table.to_csv("Data/voter_table.csv", index=False)
    print("✅ Voter table created successfully (voter_table.csv)")

    # === Step 6: Combine with Voter_Card.csv to form voter_master.csv ===
    print("🔄 Combining with Voter_Card.csv to create voter_master.csv...")

    card = pd.read_csv("Data/Voter_Card.csv")
    table = pd.read_csv("Data/voter_table.csv")

    # Clean column names
    card.columns = card.columns.str.strip().str.upper()
    table.columns = table.columns.str.strip().str.upper()

    # Merge based on VOTER ID
    merged = pd.merge(
        card,
        table[["VOTER ID", "CON_ID", "POLLING_BOOTH_ID", "AGE"]],
        on="VOTER ID",
        how="left"
    )

    # Reorder final columns
    final_cols = [
        "CON_ID",
        "POLLING_BOOTH_ID",
        "VOTER ID",
        "NAME",
        "GENDER",
        "AGE",
        "DOB",
        "FATHER'S NAME / HUSBAND'S NAME"
    ]
    merged = merged[final_cols]
 

    # Save final voter_master.csv
    merged.to_csv("Data/voters_info.csv", index=False, encoding="utf-8")

    print("✅ Final voter_master.csv created successfully.")
    return merged


# Run only when this file is executed directly
if __name__ == "__main__":
    generate_voters()