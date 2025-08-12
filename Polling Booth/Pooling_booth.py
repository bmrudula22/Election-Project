import pandas as pd
import random

# -------------------------------
# Step 1: Setup booth parameters
# -------------------------------

# We define 5 constituency names for our example
constituencies = ["North", "South", "East", "West", "Central","North-east","South-east","North-West","South-west"]


# Number of polling booths we want to create
num_booths = 20

# We store all booth records here
booth_data = []

# Population density range (people per sq km)
# In India, urban dense areas can go 5,000+ people/km²
# Rural areas may have lower densities.
population_density_range = (200, 10000)

# -------------------------------
# Step 2: Generate booth details
# -------------------------------
for booth_id in range(1, num_booths + 1):

    # Booth name can be simple — "Booth <id>"
    booth_name = f"Booth {booth_id}"

    # Assign a constituency randomly from our list
    constituency = random.choice(constituencies)

    # Random population density for that booth's area
    pop_density = random.randint(
        population_density_range[0],
        population_density_range[1]
    )

    # Add this booth's details into our list
    booth_data.append({
        "booth_id": booth_id,
        "booth_name": booth_name,
        "constituency": constituency,
        "population_density": pop_density
    })

# -------------------------------
# Step 3: Save to CSV
# -------------------------------
booth_df = pd.DataFrame(booth_data)
booth_df.to_csv("polling_booth.csv", index=False)

print("Polling booth details file created: polling_booth_details.csv")