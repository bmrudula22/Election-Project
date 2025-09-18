import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import squarify

def get_constituencies(save_csv=True, plot=True):
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

    # Normalize AREA for layout
    sizes = df_const["AREA"].values
    normed_sizes = squarify.normalize_sizes(sizes, 100, 100)
    rects = squarify.squarify(normed_sizes, 0, 0, 100, 100)

    df_rects = pd.DataFrame(rects).rename(columns={"dx": "WIDTH", "dy": "HEIGHT"})
    df_const = pd.concat([df_const, df_rects[["x", "y", "WIDTH", "HEIGHT"]]], axis=1)

  
    # Save CSV if requested
    if save_csv:
        df_const.to_csv("Data\\constituencies.csv", index=False)

    # --- Plot treemap ---
    if plot:
        norm = mcolors.Normalize(vmin=df_const["POPULATION"].min(), vmax=df_const["POPULATION"].max())
        cmap = cm.Blues

        fig, ax = plt.subplots(figsize=(12, 8))
        for _, row in df_const.iterrows():
            x, y, w, h = row["x"], row["y"], row["WIDTH"], row["HEIGHT"]
            color = cmap(norm(row["POPULATION"]))
            ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color))
            ax.text(x + w/2, y + h/2, row["NAME"], ha="center", va="center", fontsize=9)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    plt.title("Constituency Treemap (Population Colored)", fontsize=14, pad=20)
    plt.savefig("treemap.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("✅ Constituencies treemap saved.")
    
    return df_const
  
 # Only runs if you execute this file directly, not when imported   
if __name__ == "__main__":
    df = get_constituencies()