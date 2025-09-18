import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from consituency import get_constituencies

random.seed(42)
np.random.seed(42)


def generate_polling_booths(save_csv=True, plot=True):
# Get constituencies with rectangles
    df_constituencies = get_constituencies()


# Institution & locality names.
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
        booths_by_voters = estimated_voters // 1000 # 1 per 1000 voters
    
    
    #booths_by_area → Minimum booths needed based on area.
    #booths_by_voters → Minimum booths needed based on number of voters.
    #max() → Choose whichever gives more booths (safer for avoiding overcrowding).
        total_booths = max(booths_by_area, booths_by_voters)

        for i in range(total_booths):
            institution_name = random.choice(institutions)
            locality_name = random.choice(localities)
        
            booth_name = f"{institution_name}, {locality_name} - Booth No. {i+1}" #→ numbering resets per constituency (1..N).
            address = f"{institution_name}, {locality_name}, {row['NAME']} Constituency"
        
        # Place booth randomly inside constituency rectangle using x, y, WIDTH, HEIGHT
            LAT = row["x"] + random.random() * row["WIDTH"]
            LON = row["y"] + random.random() * row["HEIGHT"]
        
            polling_booths.append([
                row["CON_ID"],
                booth_id_counter,
                booth_name,
                LAT,
                LON,
                address
            ])
        
            booth_id_counter += 1

# Step 4: Save
    df_polling_booths = pd.DataFrame(
    polling_booths,
    columns=["CON_ID", "POLLING_BOOTH_ID", "NAME", "LAT", "LON", "ADDRESS"]
)
    if save_csv:
        df_polling_booths.to_csv("Data\\polling_booths.csv", index=False)

        print(" Polling booths table created and saved")


# Plot treemap with booths
    constituency_counts = (
        df_polling_booths.groupby("CON_ID")["POLLING_BOOTH_ID"]
        .count()
        .reset_index()
        .rename(columns={"POLLING_BOOTH_ID": "NUM_BOOTHS"})
)
    
    if plot:

# Colormap based on booth count
        norm = mcolors.Normalize(vmin=df_constituencies["POPULATION"].min(),
                         vmax=df_constituencies["POPULATION"].max())
        cmap = cm.Blues

# Plot
        fig, ax = plt.subplots(figsize=(12, 8))
        for _, row in df_constituencies.iterrows():
            x, y, w, h = row["x"], row["y"], row["WIDTH"], row["HEIGHT"]
            color = cmap(norm(row["POPULATION"]))  # ✅ population-based color



    # Constituency rectangle
            ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color))

    # Constituency label
            ax.text(x + w/2, y + h/2, f"{row['NAME']}",
            ha="center", va="center", fontsize=9, color="black")

    # Booths (black dots)
            booths_in_con = df_polling_booths[df_polling_booths["CON_ID"] == row["CON_ID"]]
            ax.scatter(booths_in_con["LAT"], booths_in_con["LON"], c="black", s=5, alpha=0.8)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal', adjustable='box')
    ax.axis("off")
    plt.savefig("treemap_polling_booth.png", dpi=300, bbox_inches="tight")
    plt.title("Treemap of Constituencies with Polling Booths", fontsize=14, pad=20)
    plt.show()

    return df_polling_booths


if __name__ == "__main__":
    generate_polling_booths()