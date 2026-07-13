import pandas as pd
import matplotlib.pyplot as plt
import save_chart

CATEGORICAL_COLUMNS = [
    "Location_Category",
    "Customer_Loyalty_Status",
    "Time_of_Booking",
    "Vehicle_Type",
]


def plot_bar_chart(series, title, xlabel, ylabel, filename, save=False):
    fig = plt.figure(figsize=(7, 4))
    plt.bar(series.index, series.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, filename)
    else:
        plt.show()


def summarise_cost_by_category(dataframe, category):
    summary = (
        dataframe.groupby(category)["Historical_Cost_of_Ride"]
        .agg(["count", "mean", "median"])
        .round(2)
    )
    return summary


def add_demand_supply_features(dataframe):
    featured_dataframe = dataframe.copy()

    featured_dataframe["Demand_Supply_Ratio"] = (
        featured_dataframe["Number_of_Riders"] / featured_dataframe["Number_of_Drivers"]
    )

    featured_dataframe["Demand_Supply_Difference"] = (
        featured_dataframe["Number_of_Riders"] - featured_dataframe["Number_of_Drivers"]
    )

    return featured_dataframe


def classify_duration(minutes):
    if minutes <= 60:
        return "Short"

    elif minutes <= 120:
        return "Medium"

    else:
        return "Long"


def create_duration_vehicle_table(dataframe):
    analysis_dataframe = dataframe.copy()

    analysis_dataframe["Duration_Group"] = analysis_dataframe[
        "Expected_Ride_Duration"
    ].apply(classify_duration)

    duration_vehicle_table = pd.pivot_table(
        analysis_dataframe,
        values="Historical_Cost_of_Ride",
        index="Duration_Group",
        columns="Vehicle_Type",
        aggfunc="mean",
    ).round(2)

    duration_vehicle_table = duration_vehicle_table.reindex(["Short", "Medium", "Long"])
    return duration_vehicle_table


def plot_historical_cost_distribution(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.hist(dataframe["Historical_Cost_of_Ride"], bins=20)
    plt.title("Distribution of Historical Ride Cost")
    plt.xlabel("Historical Cost of Ride")
    plt.ylabel("Frequency")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "historical_cost_distribution.png")
    else:
        plt.show()


def plot_duration_and_cost(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    for vehicle_type in dataframe["Vehicle_Type"].unique():
        vehicle_data = dataframe[dataframe["Vehicle_Type"] == vehicle_type]

        plt.scatter(
            vehicle_data["Expected_Ride_Duration"],
            vehicle_data["Historical_Cost_of_Ride"],
            label=vehicle_type,
        )

    plt.title("Expected Ride Duration vs Historical Ride Cost " "by Vehicle Type")

    plt.xlabel("Expected Ride Duration (minutes)")
    plt.ylabel("Historical Cost of Ride")
    plt.legend()
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "duration_vs_cost_by_vehicle_type.png")
    else:
        plt.show()


def plot_past_rides_and_cost(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Number_of_Past_Rides"], dataframe["Historical_Cost_of_Ride"])

    plt.title("Number of Past Rides vs Historical Ride Cost")

    plt.xlabel("Number of Past Rides")
    plt.ylabel("Historical Cost of Ride")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "past_rides_vs_cost.png")
    else:
        plt.show()


def plot_ratings_and_cost(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Average_Ratings"], dataframe["Historical_Cost_of_Ride"])

    plt.title("Average Ratings vs Historical Ride Cost")

    plt.xlabel("Average Ratings")
    plt.ylabel("Historical Cost of Ride")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "ratings_vs_cost.png")
    else:
        plt.show()


def display_dataset_overview(dataframe):
    print("\nDataset shape:")
    print(dataframe.shape)

    print("\nDataset information:")
    dataframe.info()

    print("\nDescriptive statistics:")
    print(dataframe.describe())

    structure_summary = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Data Type": dataframe.dtypes.values,
            "Missing Values": (dataframe.isnull().sum().values),
            "Unique Values": (dataframe.nunique().values),
        }
    )

    print("\nDataset structure:")
    print(structure_summary)


def display_categorical_overview(dataframe):
    print("\nCategorical variables:")

    for column in CATEGORICAL_COLUMNS:
        print("\n", column)
        print("Unique values:", dataframe[column].unique())
        print(dataframe[column].value_counts())


def display_category_summaries(dataframe):
    vehicle_summary = summarise_cost_by_category(dataframe, "Vehicle_Type")
    location_summary = summarise_cost_by_category(dataframe, "Location_Category")

    time_summary = summarise_cost_by_category(dataframe, "Time_of_Booking")

    loyalty_summary = summarise_cost_by_category(dataframe, "Customer_Loyalty_Status")

    print("\nHistorical cost by vehicle type:")
    print(vehicle_summary)

    print("\nHistorical cost by location category:")
    print(location_summary)

    print("\nHistorical cost by time of booking:")
    print(time_summary)

    print("\nHistorical cost by loyalty status:")
    print(loyalty_summary)


def create_category_charts(dataframe, save=False):
    vehicle_cost = (
        dataframe.groupby("Vehicle_Type")["Historical_Cost_of_Ride"].mean().round(2)
    )

    plot_bar_chart(
        vehicle_cost,
        "Average Ride Cost by Vehicle Type",
        "Vehicle Type",
        "Average Historical Ride Cost",
        "average_cost_by_vehicle_type.png",
        save,
    )

    location_cost = (
        dataframe.groupby("Location_Category")["Historical_Cost_of_Ride"]
        .mean()
        .round(2)
    )

    plot_bar_chart(
        location_cost,
        "Average Ride Cost by Location Category",
        "Location Category",
        "Average Historical Ride Cost",
        "average_cost_by_location_category.png",
        save,
    )

    time_cost = (
        dataframe.groupby("Time_of_Booking")["Historical_Cost_of_Ride"]
        .mean()
        .round(2)
        .reindex(["Morning", "Afternoon", "Evening", "Night"])
    )

    plot_bar_chart(
        time_cost,
        "Average Ride Cost by Time of Booking",
        "Time of Booking",
        "Average Historical Ride Cost",
        "average_cost_by_time_of_booking.png",
        save,
    )

    loyalty_cost = (
        dataframe.groupby("Customer_Loyalty_Status")["Historical_Cost_of_Ride"]
        .mean()
        .round(2)
        .reindex(["Regular", "Silver", "Gold"])
    )

    plot_bar_chart(
        loyalty_cost,
        "Average Ride Cost by Customer Loyalty Status",
        "Customer Loyalty Status",
        "Average Historical Ride Cost",
        "average_cost_by_loyalty_status.png",
        save,
    )
