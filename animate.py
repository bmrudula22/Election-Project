import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib.ticker as mtick

# Load polling day data
df = pd.read_csv("Data\\polling_day.csv")

# Convert EXIT_TIME to datetime (time only)
df['EXIT_TIME'] = pd.to_datetime(df['EXIT_TIME'], format='%H:%M:%S').dt.time

# Assume polls open at 08:00:00
poll_open = pd.to_datetime("08:00:00", format='%H:%M:%S').time()

# Convert times to "minutes since poll open"
def minutes_since_open(t):
    return (pd.Timestamp.combine(pd.Timestamp.today(), t) -
            pd.Timestamp.combine(pd.Timestamp.today(), poll_open)).seconds // 60

df['EXIT_MINUTES'] = df['EXIT_TIME'].apply(minutes_since_open)

# Sort by exit minutes
df = df.sort_values(by="EXIT_MINUTES").reset_index(drop=True)

# Total voters
total_voters = len(df)

# Animation data
cumulative_votes = []
time_steps = []

# Plot setup
plt.style.use("seaborn-v0_8")
plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))

# Secondary y-axis: Turnout %
ax2 = ax.twinx()
ax2.set_ylim(0, total_voters)
ax2.set_ylabel("Turnout %", fontsize=12, color="darkgreen")
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=total_voters))

# Initialize line object
line, = ax.plot([], [], color="royalblue", linewidth=2.5, marker="o", markersize=6)

# Titles and labels
ax.set_title("Polling Day Voter Turnout", fontsize=16, fontweight="bold", color="darkblue")
ax.set_xlabel("Minutes Since Polls Opened", fontsize=12)
ax.set_ylabel("Cumulative Votes Cast", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.6)

# Animation loop
for i in range(len(df)):
    # Stop if figure is closed
    if not plt.fignum_exists(fig.number):
        break

    cumulative_votes.append(i + 1)
    time_steps.append(df.loc[i, 'EXIT_MINUTES'])

    # Update every 100 votes or at the end
    if (i + 1) % 100 == 0 or (i + 1) == total_voters:
        # Update line data
        line.set_data(time_steps, cumulative_votes)

        # Update axes limits dynamically
        ax.set_xlim(0, max(time_steps) + 5)
        ax.set_ylim(0, max(cumulative_votes) + 10)

        # Dynamic annotation (remove old text to prevent overlap)
        for txt in ax.texts:
            txt.remove()
        ax.text(0.02, 0.95, f"Votes Counted: {i+1}/{total_voters}",
                transform=ax.transAxes, fontsize=12, color="black",
                bbox=dict(facecolor="white", alpha=0.7, boxstyle="round"))

        plt.tight_layout()
        plt.draw()
        plt.pause(0.001)
        time.sleep(1)

plt.ioff()
plt.show()