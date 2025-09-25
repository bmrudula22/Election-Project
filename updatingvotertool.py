import pandas as pd
import re
import os

# CSV file path
csv_path = "Data\\Voter_Card.csv"

# Ensure CSV exists with correct headers
if not os.path.exists(csv_path):
    pd.DataFrame(columns=[
        "Voter ID", "Name", "Gender", "DOB", "Father's Name / Husband's Name"
    ]).to_csv(csv_path, index=False)

# Load CSV
voter_df = pd.read_csv(csv_path)

def get_voter_details(voter_id):
    match = voter_df[voter_df['Voter ID'] == voter_id]
    return match if not match.empty else None

def validate_details(name, gender, dob, relation_name):
    if not re.match(r'^[A-Za-z\s]{3,}$', name):
        return False, "Name must be alphabetic and at least 3 characters"
    if gender not in ['Male', 'Female', 'Other']:
        return False, "Gender must be 'Male', 'Female', or 'Other'"
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
        return False, "DOB must be in YYYY-MM-DD format"
    if not re.match(r'^[A-Za-z\s]{3,}$', relation_name):
        return False, "Relation name must be alphabetic and at least 3 characters"
    return True, "Valid"

def add_or_update_voter(voter_id, name, gender, dob, relation_name):
    global voter_df
    index = voter_df[voter_df['Voter ID'] == voter_id].index
    valid, message = validate_details(name, gender, dob, relation_name)
    if not valid:
        return f"❌ Validation failed: {message}"

    if index.empty:
        new_row = pd.DataFrame([{
            'Voter ID': voter_id,
            'Name': name,
            'Gender': gender,
            'DOB': dob,
            "Father's Name / Husband's Name": relation_name
        }])
        voter_df = pd.concat([voter_df, new_row], ignore_index=True)
        action = "added"
    else:
        voter_df.loc[index, ['Name', 'Gender', 'DOB', "Father's Name / Husband's Name"]] = [name, gender, dob, relation_name]
        action = "updated"

    voter_df.to_csv(csv_path, index=False)
    return f"✅ Voter details {action} successfully."

def delete_voter(voter_id):
    global voter_df
    index = voter_df[voter_df['Voter ID'] == voter_id].index
    if index.empty:
        return "❌ Voter ID not found."
    voter_df = voter_df.drop(index)
    voter_df.to_csv(csv_path, index=False)
    return "🗑️ Voter entry deleted successfully."

def main():
    while True:
        print("\n🔧 Voter Management Menu")
        print("1. View Voter Details")
        print("2. Add or Update Voter")
        print("3. Delete Voter")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            voter_id = input("Enter Voter ID to view: ").strip()
            result = get_voter_details(voter_id)
            if result is None:
                print("❌ Voter ID not found.")
            else:
                print("\n📋 Voter Details:")
                print(result.to_string(index=False))

        elif choice == "2":
            voter_id = input("Voter ID: ").strip()
            name = input("Name: ").strip()
            gender = input("Gender (Male/Female/Other): ").strip()
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            relation_name = input("Father's Name / Husband's Name: ").strip()
            result = add_or_update_voter(voter_id, name, gender, dob, relation_name)
            print(result)

        elif choice == "3":
            voter_id = input("Enter Voter ID to delete: ").strip()
            result = delete_voter(voter_id)
            print(result)

        elif choice == "4":
            print("👋 Exiting voter management tool.")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()