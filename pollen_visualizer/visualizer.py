from pollen_visualizer.request import fetch_data

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


plt.rcParams['mathtext.fontset'] = 'stix'


def visualize():
    data = fetch_data()
    data["date"] = [" ".join(d[:-12].split("T")) + "H" for d in data["date"]]
    start = data["date"].iloc[0]
    end = data["date"].iloc[-1]
    start_date = "".join(start.split("-")[1:3])[:4]
    end_date = "".join(end.split("-")[1:3])[:4]
    year = start[:4]

    _, ax = plt.subplots()
    ax.set_title(f"{year} from {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Particle/$m^2$")
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.plot(data["date"], data["pollen"])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    ax.grid()
    plt.show()


if __name__ == "__main__":
    visualize()
