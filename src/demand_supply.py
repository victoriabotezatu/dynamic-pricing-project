import pandas as pd
import matplotlib.pyplot as plt
import save_chart

LOCATION_ORDER = ["Rural", "Suburban", "Urban"]
TIME_ORDER = ["Morning", "Afternoon", "Evening", "Night"]
LOYALTY_ORDER = ["Regular", "Silver", "Gold"]
VEHICLE_ORDER = ["Economy", "Premium"]

DEMAND_SUPPLY_COLUMNS = [
    "Number_of_Riders",
    "Number_of_Drivers",
    "Demand_Supply_Difference",
    "Demand_Supply_Ratio",
]


def display_dataset_overview(dataframe):
    print(dataframe.head())
    dataframe.info()

    print("Location categories:", dataframe["Location_Category"].unique())
    print("Customer loyalty statuses:", dataframe["Customer_Loyalty_Status"].unique())
    print("Times of booking:", dataframe["Time_of_Booking"].unique())
    print("Vehicle types:", dataframe["Vehicle_Type"].unique())

    print(dataframe[DEMAND_SUPPLY_COLUMNS].head())


def add_demand_supply_level(dataframe):
    featured_dataframe = dataframe.copy()

    featured_dataframe["Demand_Supply_Level"] = pd.qcut(
        featured_dataframe["Demand_Supply_Ratio"], 3, labels=["Low", "Medium", "High"]
    )

    return featured_dataframe


def summarise_by_demand_supply_level(dataframe):
    summary = dataframe.groupby("Demand_Supply_Level", observed=False)[
        DEMAND_SUPPLY_COLUMNS
    ].mean()

    return summary.reindex(["Low", "Medium", "High"]).round(2)


def summarise_by_location(dataframe):
    summary = dataframe.groupby("Location_Category")[DEMAND_SUPPLY_COLUMNS].mean()
    return summary.reindex(LOCATION_ORDER).round(2)


def summarise_by_time(dataframe):
    summary = dataframe.groupby("Time_of_Booking")[DEMAND_SUPPLY_COLUMNS].mean()
    return summary.reindex(TIME_ORDER).round(2)


def summarise_by_loyalty(dataframe):
    summary = dataframe.groupby("Customer_Loyalty_Status")[DEMAND_SUPPLY_COLUMNS].mean()
    return summary.reindex(LOYALTY_ORDER).round(2)


def summarise_by_vehicle(dataframe):
    summary = dataframe.groupby("Vehicle_Type")[DEMAND_SUPPLY_COLUMNS].mean()
    return summary.reindex(VEHICLE_ORDER).round(2)


def create_demand_supply_heatmap(dataframe):
    heatmap_data = pd.pivot_table(
        dataframe,
        values="Demand_Supply_Ratio",
        index="Location_Category",
        columns="Time_of_Booking",
        aggfunc="mean",
    )

    return heatmap_data.reindex(index=LOCATION_ORDER, columns=TIME_ORDER)


def find_surge_candidates(dataframe):
    surge_candidates = (
        dataframe.groupby(["Location_Category", "Time_of_Booking"])["Demand_Supply_Ratio"]
        .mean()
        .reset_index()
    )

    return surge_candidates.sort_values("Demand_Supply_Ratio", ascending=False)


def plot_overall_demand_supply(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    overall_demand_supply = dataframe[["Number_of_Riders", "Number_of_Drivers"]].mean()
    plt.bar(["Demand: Riders", "Supply: Drivers"], overall_demand_supply.values)

    plt.title("Average Demand and Supply")
    plt.ylabel("Average Number")
    plt.tick_params(axis="x", pad=10)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "average_demand_and_supply.png")
    else:
        plt.show()


def plot_demand_vs_supply(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Number_of_Drivers"], dataframe["Number_of_Riders"], alpha=0.5)

    plt.xlabel("Number of Drivers - Supply", labelpad=15)
    plt.ylabel("Number of Riders - Demand", labelpad=15)
    plt.title("Demand vs Supply")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_vs_supply.png")
    else:
        plt.show()


def plot_demand_supply_levels(pressure_summary, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.bar(pressure_summary.index, pressure_summary["Demand_Supply_Ratio"])

    plt.xlabel("Demand-Supply Level", labelpad=15)
    plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
    plt.title("Demand Pressure Levels")
    plt.tick_params(axis="x", pad=10)

    for i, value in enumerate(pressure_summary["Demand_Supply_Ratio"]):
        plt.text(i, value, round(value, 2), ha="center", va="bottom")

    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_pressure_levels.png")
    else:
        plt.show()


def plot_demand_supply_by_location(location_summary, save=False):
    ax = location_summary[["Number_of_Riders", "Number_of_Drivers"]].plot(kind="bar")
    fig = ax.get_figure()
    fig.set_size_inches(7, 4)

    plt.xlabel("Location Category", labelpad=15)
    plt.ylabel("Average Number", labelpad=15)
    plt.title("Average Demand and Supply by Location")
    plt.tick_params(axis="x", pad=10)
    plt.xticks(rotation=0)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_supply_by_location.png")
    else:
        plt.show()


def plot_demand_pressure_by_time(time_summary, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.plot(time_summary.index, time_summary["Demand_Supply_Ratio"], marker="o")

    plt.xlabel("Time of Booking", labelpad=15)
    plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
    plt.title("Demand Pressure by Time of Booking")
    plt.tick_params(axis="x", pad=10)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_pressure_by_time.png")
    else:
        plt.show()


def plot_demand_pressure_heatmap(heatmap_data, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.imshow(heatmap_data, cmap="coolwarm")

    plt.colorbar(label="Demand-Supply Ratio")
    plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns)
    plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)

    plt.xlabel("Time of Booking")
    plt.ylabel("Location Category")
    plt.title("Demand Pressure by Location and Time")

    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]
            plt.text(j, i, round(value, 2), ha="center", va="center")

    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_pressure_heatmap.png")
    else:
        plt.show()


def plot_top_surge_candidates(surge_candidates, save=False):
    top_surge = surge_candidates.head(5).copy()

    top_surge["Market_Situation"] = (
        top_surge["Location_Category"] + " - " + top_surge["Time_of_Booking"]
    )

    fig = plt.figure(figsize=(7, 4))

    plt.bar(top_surge["Market_Situation"], top_surge["Demand_Supply_Ratio"])

    plt.xlabel("Market Situation", labelpad=15)
    plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
    plt.title("Top 5 Demand Pressure Situations")
    plt.tick_params(axis="x", pad=10)
    plt.xticks(rotation=30)

    for i, value in enumerate(top_surge["Demand_Supply_Ratio"]):
        plt.text(i, value, round(value, 2), ha="center", va="bottom")

    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "top_demand_pressure_situations.png")
    else:
        plt.show()


def plot_demand_pressure_by_loyalty(loyalty_summary, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.barh(loyalty_summary.index, loyalty_summary["Demand_Supply_Ratio"])

    plt.xlabel("Average Demand-Supply Ratio", labelpad=15)
    plt.ylabel("Customer Loyalty Status", labelpad=15)
    plt.title("Demand Pressure by Customer Loyalty Status")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_pressure_by_loyalty.png")
    else:
        plt.show()


def plot_demand_supply_by_vehicle(vehicle_summary, save=False):
    ax = vehicle_summary[["Number_of_Riders", "Number_of_Drivers"]].plot(kind="bar")
    fig = ax.get_figure()
    fig.set_size_inches(7, 4)

    plt.xlabel("Vehicle Type", labelpad=15)
    plt.ylabel("Average Number", labelpad=15)
    plt.title("Average Demand and Supply by Vehicle Type")
    plt.tick_params(axis="x", pad=10)
    plt.xticks(rotation=0)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_supply_by_vehicle.png")
    else:
        plt.show()
