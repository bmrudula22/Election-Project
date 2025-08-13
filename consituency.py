# part1_constituencies.py
import pandas as pd

# Step 1: Create Constituencies Table (manual)
constituencies = [
    {"CON_ID": 1, "NAME": "East", "AREA": 350, "POPULATION": 128000},
    {"CON_ID": 2, "NAME": "West", "AREA": 230, "POPULATION": 152000},
    {"CON_ID": 3, "NAME": "North", "AREA": 210, "POPULATION": 95000},
    {"CON_ID": 4, "NAME": "South", "AREA": 230, "POPULATION": 110000},
    {"CON_ID": 5, "NAME": "North-East", "AREA": 110, "POPULATION": 102000},
    {"CON_ID": 6, "NAME": "South-East", "AREA": 120, "POPULATION": 118000},
    {"CON_ID": 7, "NAME": "North-West", "AREA": 130, "POPULATION": 88000},
    {"CON_ID": 8, "NAME": "South-West", "AREA": 150, "POPULATION": 99000},
]

df_const = pd.DataFrame(constituencies)
df_const.to_csv("constituencies.csv", index=False)

print("✅ Constituencies table created: constituencies.csv")