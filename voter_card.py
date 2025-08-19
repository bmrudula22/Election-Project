import pandas as pd
import random
from datetime import datetime, timedelta

# Seed for reproducibility
random.seed(42)

# Sample data
male_first_names = ["Arun", "Ravi", "Suresh", "Vikram", "Rahul", "Anil", "Kiran", "Manoj", "Vijay", "Sanjay"]
female_first_names = ["Sita", "Radha", "Latha", "Anjali", "Priya", "Kavya", "Sneha", "Divya", "Meena", "Lakshmi"]
last_names = ["Sharma", "Reddy", "Kumar", "Verma", "Naidu", "Yadav", "Singh", "Joshi", "Das", "Babu"]
genders = ["Male", "Female"]

base_date = datetime(2025, 1, 1)


def generate_epic_number():
    letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numbers = ''.join(random.choices("0123456789", k=7))
    return letters + numbers

def generate_voters(n=10000):
    records = []
    for i in range(n):
        gender = random.choice(genders)
        dob = base_date - timedelta(days=random.randint(18*365, 65*365))  
        # Fixed range
        age = (base_date.date() - dob.date()).days // 365  
        # Use base_date to calculate age
        
        
        #Female voters over 25 years old have a 60% chance of showing husband's name.
        #Others show father's name.
        #Male voters always show father’s name.
        if gender == "Male":
            first_name = random.choice(male_first_names)
            relation_name = random.choice(male_first_names) + " " + random.choice(last_names)
        else:
            first_name = random.choice(female_first_names)
            if age >= 25 and random.random() > 0.4:  # 60% married females over 25
                relation_name = random.choice(male_first_names) + " " + random.choice(last_names)  # Husband
            else:
                relation_name = random.choice(male_first_names) + " " + random.choice(last_names)  # Father
        
        
        #Adds a random initial like "R. Arun Kumar"
        full_name = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ". " + first_name + " " + random.choice(last_names)
        

        records.append({
            "Voter ID": generate_epic_number(),
            "Name": full_name,
            "Gender": gender,
            "DOB": dob.date(),
            "Father's Name / Husband's Name": relation_name
        })

    return pd.DataFrame(records)

# Generate and export
df = generate_voters()
df.to_csv("Voter_Card.csv", index=False)
print("File 'Voter_card.csv' generated successfully.")