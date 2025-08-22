import pandas as pd
import matplotlib.pyplot as plt
import squarify  # pip install squarify

# Load constituency dataset
df_const = pd.read_csv("constituencies.csv")

# Example: dataset should have columns: Constituency_ID, Constituency_Name, Area, Population

# Normalize population for coloring
norm = plt.Normalize(df_const["POPULATION"].min(), df_const["POPULATION"].max())
colors = [plt.cm.viridis(norm(value)) for value in df_const["POPULATION"]]

# Plot Treemap
plt.figure(figsize=(12, 8))
squarify.plot(
    sizes=df_const["AREA"], 
    label=df_const["NAME"], 
    color=colors, 
    alpha=0.8
)

plt.title("Constituency Treemap", fontsize=16, pad = 20)
plt.axis("off")  # remove axes
# Save treemap as PNG
plt.savefig("treemap.png", dpi=300, bbox_inches="tight")
plt.show()