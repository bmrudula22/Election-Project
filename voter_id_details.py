
import pandas as pd
from datetime import datetime

# Read the voters dataset which has DOB
df_voters = pd.read_csv("voter_Card.csv")

# Ensure DOB is in datetime format
df_voters['DOB'] = pd.to_datetime(df_voters['DOB'], errors='coerce')

# Function to calculate age from DOB
def calculate_age(dob):
    if pd.isnull(dob):
        return None
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Create AGE column from DOB
df_voters['Age'] = df_voters['DOB'].apply(calculate_age)

# Create voter card CSV with only required fields
df_voter_card = df_voters[['Voter ID', 'Name', 'Gender', 'Age']]

# Save to CSV
df_voter_card.to_csv("voter_card_details.csv", index=False)

print("Voter card CSV created with AGE extracted from DOB!")


# Read existing voters table with VOTER_ID, NAME, AGE, GENDER
df_voters = pd.read_csv("voter_card_details.csv")  # your existing file

# Read constituency and polling booth tables
df_constituencies = pd.read_csv("constituencies.csv")
df_polling_booths = pd.read_csv("polling_booths.csv")

total_voters = len(df_voters)

# -------------------------------
# Assign voters to constituencies based on population
# -------------------------------
df_constituencies["VOTERS_PER_CONSTITUENCY"] = (
    (df_constituencies["POPULATION"] / df_constituencies["POPULATION"].sum()) * total_voters
).astype(int)

voter_index = 0
con_ids = []
booth_ids = []

for _, constituency in df_constituencies.iterrows():
    con_id = constituency["CON_ID"]
    num_voters_con = constituency["VOTERS_PER_CONSTITUENCY"]
    
    booths = df_polling_booths[df_polling_booths["CON_ID"] == con_id]
    num_booths = len(booths)
    
    # Distribute voters among booths
    base_voters_per_booth = num_voters_con // num_booths
    remainder = num_voters_con % num_booths
    
    for i, (_, booth) in enumerate(booths.iterrows()):
        voters_in_booth = base_voters_per_booth + remainder if i == num_booths - 1 else base_voters_per_booth
        
        for _ in range(voters_in_booth):
            if voter_index < total_voters:
                con_ids.append(con_id)
                booth_ids.append(booth["POLLING_BOOTH_ID"])
                voter_index += 1

# Add the new columns to existing voters table
df_voters['CON_ID'] = con_ids
df_voters['POLLING_BOOTH_ID'] = booth_ids

# Save the updated CSV
df_voters.to_csv("voters_with_con_booth.csv", index=False)

print("Voter table updated with CON_ID and POLLING_BOOTH_ID!")