import pandas as pd
from datetime import datetime
import random
import math
import numpy as np

random.seed(42)
np.random.seed(42)

def generate_voters():
# Read the voters dataset which has DOB
    df_voters = pd.read_csv("Data\\voter_card.csv")

# Ensure DOB is in datetime format
    df_voters['DOB'] = pd.to_datetime(df_voters['DOB'], errors='coerce')

# Function to calculate age from DOB(date of birth)
    def calculate_age(dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

# Create AGE column from DOB(date of birth)
    df_voters['Age'] = df_voters['DOB'].apply(calculate_age)

# Create voter card CSV with only required fields
    df_voter_card = df_voters[['Voter ID', 'Name', 'Gender', 'Age']]


#Read CSV files
    df_booths = pd.read_csv("Data\\polling_booths.csv")  # CON_ID, POLLING_BOOTH_ID, NAME, LOCATION_LAT, LOCATION_LONG, ADDRESS
    df_voters = pd.read_csv("Data\\voter_card_details.csv") # VOTER_ID, NAME, AGE, GENDER

# Keep only needed booth columns
    df_booths = df_booths[['CON_ID', 'POLLING_BOOTH_ID']]


    num_voters = len(df_voters)
    num_booths = len(df_booths)


# Repeat each booth enough times to cover all voters
    repeat_count = math.ceil(num_voters / num_booths)  # e.g., ceil(10000/1531) = 7
    booth_assignment_list = list(df_booths['POLLING_BOOTH_ID']) * repeat_count

# Trim to exactly match number of voters
    booth_assignment_list = booth_assignment_list[:num_voters]

# Shuffle the list to randomize voter assignment
    random.shuffle(booth_assignment_list)

# Assign booths to voters
    df_voters['POLLING_BOOTH_ID'] = booth_assignment_list

# Map CON_ID and ADDRESS from booth
    booth_map = df_booths.set_index('POLLING_BOOTH_ID')[['CON_ID']].to_dict(orient='index')

    df_voters['CON_ID'] = df_voters['POLLING_BOOTH_ID'].map(lambda x: booth_map[x]['CON_ID'])

# Step 5: Select final columns

    df_final = df_voters[['CON_ID', 'POLLING_BOOTH_ID', 'Voter ID', 'Name', 'Gender', 'Age',]]

# Step 6: Save final CSV
    df_final.to_csv("Data\\voter_table.csv", index=False)

    print("✅ Voter table created successfully ")
    return df_final

# This part runs only if you execute voters.py directly
if __name__ == "__main__":
    generate_voters()