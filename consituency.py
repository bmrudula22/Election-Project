# part1_constituencies.py
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np 

#Create Constituencies Table (manual)
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

rects = squarify.squarify(
    sizes=df_const["AREA"],
    x=0,
    y=0,
    dx=12,   # width of plotting area
    dy=8     # height of plotting area
)

# Step 2: Add rectangle data (x, y, dx, dy) to dataframe
df_rects = pd.DataFrame(rects).rename(columns={"dx": "WIDTH", "dy": "HEIGHT"})


df_const = pd.concat([df_const, df_rects[["x", "y", "WIDTH", "HEIGHT"]]], axis=1)

# Step 3: Save updated constituency table with coordinates
#Generate treemap rectangles (coordinates)

df_const.to_csv("Data\\constituencies.csv", index=False)

# Normalize population for coloring
norm = plt.Normalize(df_const["POPULATION"].min(), df_const["POPULATION"].max())
colors = [plt.cm.Blues(norm(value)) for value in df_const["POPULATION"]]

# Plot Treemap
plt.figure(figsize=(12, 8))
squarify.plot(
    sizes=df_const["AREA"], 
    label=df_const["NAME"], 
    color=colors, 
    alpha=0.8,
)  

plt.title("Constituency Treemap", fontsize=16, pad = 20)
plt.axis("off")  # remove axes
# Save treemap as PNG
plt.savefig("treemap.png", dpi=300, bbox_inches="tight")
plt.show()