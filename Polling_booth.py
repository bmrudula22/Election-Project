import pandas as pd
import random

# Step 1: Read Constituencies
df_constituencies = pd.read_csv("constituencies.csv")

# Step 2: Institution & locality names.
institutions = [
    "Government Primary School",
    "Municipal High School",
    "Zilla Parishad School",
    "Panchayat Bhawan",
    "Community Hall",
    "Government Girls High School",
    "Town Hall",
    "Library Building",
    "Anganwadi Centre",
    "Temple Hall"
]

localities = [
    "Gandhi Nagar", "MG Road", "Station Area", "Market Street",
    "Lakshmi Colony", "Ambedkar Chowk", "Temple Road", "Park View",
    "School Area", "Hospital Road"
]

# Step 3: Generate booths
polling_booths = [] 
#polling_booths will collect each booth as a list (later converted to a DataFrame).
booth_id_counter = 1
#booth_id_counter provides a unique numeric ID for every generated booth across all constituencies.


#Iterates rows of the DataFrame.
#_ receives the index (unused), row is a Series representing the row.
#Note: iterrows() is fine for moderate datasets but is slow for very large frames — vectorized approaches are faster
for _, row in df_constituencies.iterrows():
    # About 68% of India’s population are eligible voters (18+).
    estimated_voters = int(row["POPULATION"] * 0.68)  # 68% of population as voters 
    booths_by_area = row["AREA"]                     # 1 per sq km
    booths_by_voters = estimated_voters // 1000      # 1 per 1000 voters
    
    
    #booths_by_area → Minimum booths needed based on area.
    #booths_by_voters → Minimum booths needed based on number of voters.
    #max() → Choose whichever gives more booths (safer for avoiding overcrowding).
    total_booths = max(booths_by_area, booths_by_voters)

    for i in range(total_booths):
        institution_name = random.choice(institutions)
        locality_name = random.choice(localities)
        
        booth_name = f"{institution_name}, {locality_name} - Booth No. {i+1}" #→ numbering resets per constituency (1..N).
        address = f"{institution_name}, {locality_name}, {row['NAME']} Constituency"
        
        polling_booths.append([
            row["CON_ID"],
            booth_id_counter,
            booth_name,
            round(random.uniform(12.0, 28.0), 6),#random latitude between 12° and 28° (roughly India).
            round(random.uniform(72.0, 88.0), 6), #random longitude between 72° and 88°.
            address
        ])
        
        booth_id_counter += 1

# Step 4: Save
df_polling_booths = pd.DataFrame(
    polling_booths,
    columns=["CON_ID", "POLLING_BOOTH_ID", "NAME", "LOCATION_LAT", "LOCATION_LONG", "ADDRESS"]
)
df_polling_booths.to_csv("polling_booths.csv", index=False)

print("✅ Polling booths table created using estimated voters (68% of population).")