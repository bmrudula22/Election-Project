import pandas as pd
from datetime import datetime

# Read the voters dataset which has DOB
df_voters = pd.read_csv("voter_Card.csv")

# Ensure DOB is in datetime format
df_voters['DOB'] = pd.to_datetime(df_voters['DOB'], errors='coerce')

# Function to calculate age from DOB(date of birth)
def calculate_age(dob):
    if pd.isnull(dob):
        return None
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Create AGE column from DOB(date of birth)
df_voters['Age'] = df_voters['DOB'].apply(calculate_age)

# Create voter card CSV with only required fields
df_voter_card = df_voters[['Voter ID', 'Name', 'Gender', 'Age']]

# Save to CSV
df_voter_card.to_csv("voter_card_details.csv", index=False)

#After the pdf is generated the print will be executed
print("Voter card CSV created with AGE extracted from DOB!")