import matplotlib.pyplot as plt



#plots the spike times for a given well and duration
def plot_spikes(df, duration=120, well="A5"):
    "df: spikes recording per channel for a given well "
    plt.figure(figsize=(18, 5))
    for i, row in df.iterrows():
        plt.eventplot(row["Time"], orientation="horizontal",
                    lineoffsets=i, linelengths=0.8)

    plt.title(f"Raster Plot of Spike Times for Well {well}")
    plt.xlabel("Time (s)")
    plt.ylabel("Channel")
    plt.yticks(range(len(df)), df["Channel"])
    plt.xlim(0, duration)
    plt.tight_layout()
    plt.show()


def plot_spikes_with_bursts(df, bursts, duration=120, well="A7"):
    plt.figure(figsize=(18, 5))

    ax = plt.gca()

    # --- Burst overlay ---
    for start, end in bursts:
        ax.axvspan(start, end, color="red", alpha=0.3, label="Burst")

    # --- Raster ---
    for i, row in df.iterrows():
        plt.eventplot(
            row["Time"],
            orientation="horizontal",
            lineoffsets=i,
            linelengths=0.8,
            color="black"
        )

    plt.title(f"Raster Plot with Burst Overlay for Channel {well}")
    plt.xlabel("Time (s)")
    plt.ylabel("Channel")
    plt.yticks(range(len(df)), df["Channel"])
    plt.xlim(0, duration)

    # Avoid duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.tight_layout()
    plt.show()


def plot_histogram_with_bursts(spike_train, bursts,
                              duration=120, bin_size_factor=5,
                              well="A7", title=None):

    "spike_train: spikes time stamp for a given well"

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(24, 6), sharex=True,
        gridspec_kw={'height_ratios': [3, 1]}  # Make raster narrower
    )
    
    # -----------------------
    # 1. HISTOGRAM + BURSTS
    # -----------------------
    bins = int(30 * 60 * bin_size_factor)
    ax1.hist(spike_train, bins=bins, color="gray", edgecolor="none")
    ax1.set_xlim(0, duration)
    ax1.set_ylabel("Spike Count")

    for start, end in bursts:
        ax1.axvspan(start, end, color="red", alpha=0.3)

    if title:
        ax1.set_title(title)

    # -----------------------
    # 2. RASTER + BURSTS
    # -----------------------
    for start, end in bursts:
        ax2.axvspan(start, end, color="red", alpha=0.3)

    ax2.eventplot(
        [spike_train],
        orientation="horizontal",
        linelengths=0.8,
        linewidths=0.5,
        color="black"
    )

    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Channel")
    ax2.set_yticks([0])
    ax2.set_yticklabels([well])
    ax2.set_xlim(0, duration)

    plt.tight_layout()
    plt.show()
