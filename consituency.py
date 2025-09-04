# part1_constituencies.py
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np 

#Create Constituencies Table (manual)
constituencies = [
    {"CON_ID": 1, "NAME": "East", "AREA": 350, "POPULATION": 128000,"LAT_MIN": 28.6100, "LAT_MAX": 28.6200, "LON_MIN": 77.2050, "LON_MAX": 77.2150},
    {"CON_ID": 2, "NAME": "West", "AREA": 230, "POPULATION": 152000,"LAT_MIN": 27.1750, "LAT_MAX": 27.1800, "LON_MIN": 78.0050, "LON_MAX": 78.0100},
    {"CON_ID": 3, "NAME": "North", "AREA": 210, "POPULATION": 95000,"LAT_MIN": 28.7000, "LAT_MAX": 28.7100, "LON_MIN": 77.1000, "LON_MAX": 77.1100},
    {"CON_ID": 4, "NAME": "South", "AREA": 230, "POPULATION": 110000,"LAT_MIN": 26.9100, "LAT_MAX": 26.9150, "LON_MIN": 75.7800, "LON_MAX": 75.7900},
    {"CON_ID": 5, "NAME": "North-East", "AREA": 110, "POPULATION": 102000,"LAT_MIN": 22.5700, "LAT_MAX": 22.5750, "LON_MIN": 88.3600, "LON_MAX": 88.3650},
    {"CON_ID": 6, "NAME": "South-East", "AREA": 120, "POPULATION": 118000,"LAT_MIN": 19.0750, "LAT_MAX": 19.0800, "LON_MIN": 72.8750, "LON_MAX": 72.8800},
    {"CON_ID": 7, "NAME": "North-West", "AREA": 130, "POPULATION": 88000,"LAT_MIN": 23.0200, "LAT_MAX": 23.0250, "LON_MIN": 72.5700, "LON_MAX": 72.5750},
    {"CON_ID": 8, "NAME": "South-West", "AREA": 150, "POPULATION": 99000,"LAT_MIN": 12.9700, "LAT_MAX": 12.9750, "LON_MIN": 77.5900, "LON_MAX": 77.5950},
]

df_const = pd.DataFrame(constituencies)
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
    alpha=0.8)  

plt.title("Constituency Treemap", fontsize=16, pad = 20)
plt.axis("off")  # remove axes
# Save treemap as PNG
plt.savefig("treemap.png", dpi=300, bbox_inches="tight")
plt.show()