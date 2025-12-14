import pandas as pd
import random
import os
from datetime import datetime, timedelta
import numpy as np
import math

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

# Ensure folder exists
os.makedirs("Data", exist_ok=True)

# Sample data
male_first_names = ["Arun", "Ravi", "Suresh", "Vikram", "Rahul", "Anil", "Kiran", "Manoj", "Vijay", "Sanjay"]
female_first_names = ["Sita", "Radha", "Latha", "Anjali", "Priya", "Kavya", "Sneha", "Divya", "Meena", "Lakshmi"]
last_names = ["Sharma", "Reddy", "Kumar", "Verma", "Naidu", "Yadav", "Singh", "Joshi", "Das", "Babu"]
genders = ["Male", "Female"]

base_date = datetime(2025, 1, 1)

# Function to create unique EPIC number
existing_epic_ids = set()

def generate_epic_number():
    while True:
        letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        numbers = ''.join(random.choices("0123456789", k=7))
        epic = letters + numbers
        if epic not in existing_epic_ids:
            existing_epic_ids.add(epic)
            return epic

# Step 1: Generate voters data
def generate_voter_details(n=10000):
    records = []
    for i in range(n):
        gender = random.choice(genders)
        dob = base_date - timedelta(days=random.randint(18*365, 65*365))
        age = (base_date.date() - dob.date()).days // 365

        if gender == "Male":
            first_name = random.choice(male_first_names)
            relation_name = random.choice(male_first_names) + " " + random.choice(last_names)
        else:
            first_name = random.choice(female_first_names)
            # Married female check
            if age >= 25 and random.random() > 0.4:
                relation_name = random.choice(male_first_names) + " " + random.choice(last_names)  # Husband
            else:
                relation_name = random.choice(male_first_names) + " " + random.choice(last_names)  # Father

        full_name = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ". " + first_name + " " + random.choice(last_names)

        records.append({
            "Voter ID": generate_epic_number(),
            "Name": full_name,
            "Gender": gender,
            "DOB": dob.date(),
            "Father's Name / Husband's Name": relation_name
        })

    df = pd.DataFrame(records)
    df.to_csv("Data/voter_card.csv", index=False)
    print("📁 Generated: Data/voter_card.csv")
    return df

# Step 2: Assign polling booths and add Age column
def assign_polling_booths():
    df_voters = pd.read_csv("Data/voter_card.csv")
    df_booths = pd.read_csv("Data/polling_booths.csv")  # needs: CON_ID, POLLING_BOOTH_ID

    # Ensure DOB is datetime
    df_voters["DOB"] = pd.to_datetime(df_voters["DOB"], errors="coerce")

    # Age calculation
    reference_date = datetime(2025, 1, 1)  # or any fixed date you decide
    df_voters["Age"] = df_voters["DOB"].apply(
    lambda dob: reference_date.year - dob.year - ((reference_date.month, reference_date.day) < (dob.month, dob.day))
)

    # Select required voter card fields
    df_voter_card = df_voters[['Voter ID', 'Name', 'Gender', 'Age']].copy()

    # Booth columns
    df_booths = df_booths[['CON_ID', 'POLLING_BOOTH_ID']]

    num_voters = len(df_voter_card)
    num_booths = len(df_booths)

    repeat_count = math.ceil(num_voters / num_booths)
    booth_assignment_list = list(df_booths["POLLING_BOOTH_ID"]) * repeat_count
    booth_assignment_list = booth_assignment_list[:num_voters]
    random.shuffle(booth_assignment_list)

    df_voter_card["POLLING_BOOTH_ID"] = booth_assignment_list

    booth_map = df_booths.set_index("POLLING_BOOTH_ID")[["CON_ID"]].to_dict(orient="index")
    df_voter_card["CON_ID"] = df_voter_card["POLLING_BOOTH_ID"].map(lambda x: booth_map[x]["CON_ID"])

    df_final = df_voter_card[['CON_ID', 'POLLING_BOOTH_ID', 'Voter ID', 'Name', 'Gender', 'Age']]
    df_final.to_csv("Data/voter_table.csv", index=False)

    print("🎯 Final table saved: Data/voter_table.csv")
    return df_final

# Run full process
if __name__ == "__main__":
    generate_voter_details()
    assign_polling_booths()