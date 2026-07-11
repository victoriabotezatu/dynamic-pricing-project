import os
import pandas as pd
import matplotlib.pyplot as plt

CATEGORICAL_COLUMNS = [
    "Location_Category",
    "Customer_Loyalty_Status",
    "Time_of_Booking",
    "Vehicle_Type"
]

def plot_bar_chart(series, title, xlabel, ylabel):
    plt.figure(figsize=(7, 4))
    plt.bar(series.index, series.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def summarise_cost_by_category(dataframe, category):
    summary = (dataframe.groupby(category)["Historical_Cost_of_Ride"].agg(["count", "mean", "median"]).round(2))
    return summary

def add_demand_supply_features(dataframe):
    featured_dataframe = dataframe.copy()

    featured_dataframe["Demand_Supply_Ratio"] = (featured_dataframe["Number_of_Riders"]/ featured_dataframe["Number_of_Drivers"])

    featured_dataframe["Demand_Supply_Difference"] = (featured_dataframe["Number_of_Riders"]- featured_dataframe["Number_of_Drivers"])

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

    analysis_dataframe["Duration_Group"] = (
        analysis_dataframe["Expected_Ride_Duration"].apply(classify_duration)
    )

    duration_vehicle_table = pd.pivot_table(
        analysis_dataframe,
        values="Historical_Cost_of_Ride",
        index="Duration_Group",
        columns="Vehicle_Type",
        aggfunc="mean"
    ).round(2)

    duration_vehicle_table = (duration_vehicle_table.reindex(["Short", "Medium", "Long"])
    )
    return duration_vehicle_table

def plot_historical_cost_distribution(dataframe):
    plt.figure(figsize=(7, 4))

    plt.hist(dataframe["Historical_Cost_of_Ride"],bins=20)
    plt.title("Distribution of Historical Ride Cost")
    plt.xlabel("Historical Cost of Ride")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def plot_duration_and_cost(dataframe):
    plt.figure(figsize=(7, 4))

    for vehicle_type in dataframe["Vehicle_Type"].unique():
        vehicle_data = dataframe[dataframe["Vehicle_Type"] == vehicle_type]

        plt.scatter(vehicle_data["Expected_Ride_Duration"],vehicle_data["Historical_Cost_of_Ride"],label=vehicle_type)

    plt.title(
        "Expected Ride Duration vs Historical Ride Cost "
        "by Vehicle Type"
    )

    plt.xlabel("Expected Ride Duration (minutes)")
    plt.ylabel("Historical Cost of Ride")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_past_rides_and_cost(dataframe):
    plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Number_of_Past_Rides"],dataframe["Historical_Cost_of_Ride"])

    plt.title("Number of Past Rides vs Historical Ride Cost")

    plt.xlabel("Number of Past Rides")
    plt.ylabel("Historical Cost of Ride")
    plt.tight_layout()
    plt.show()

def plot_ratings_and_cost(dataframe):
    plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Average_Ratings"],dataframe["Historical_Cost_of_Ride"])

    plt.title("Average Ratings vs Historical Ride Cost")

    plt.xlabel("Average Ratings")
    plt.ylabel("Historical Cost of Ride")
    plt.tight_layout()
    plt.show()

def display_dataset_overview(dataframe):
    print("\nDataset shape:")
    print(dataframe.shape)

    print("\nDataset information:")
    dataframe.info()

    print("\nDescriptive statistics:")
    print(dataframe.describe())

    structure_summary =pd.DataFrame({
        "Column": dataframe.columns,
        "Data Type": dataframe.dtypes.values,
        "Missing Values": (
            dataframe.isnull().sum().values
        ),
        "Unique Values": (
            dataframe.nunique().values
        )
    })

    print("\nDataset structure:")
    print(structure_summary)

def display_categorical_overview(dataframe):
    print("\nCategorical variables:")

    for column in CATEGORICAL_COLUMNS:
        print("\n", column)
        print(
            "Unique values:",
            dataframe[column].unique()
        )
        print(dataframe[column].value_counts())

def display_category_summaries(dataframe):
    vehicle_summary = summarise_cost_by_category(dataframe,"Vehicle_Type")
    location_summary = summarise_cost_by_category(dataframe,"Location_Category")

    time_summary = summarise_cost_by_category(dataframe,"Time_of_Booking")

    loyalty_summary = summarise_cost_by_category(dataframe,"Customer_Loyalty_Status")

    print("\nHistorical cost by vehicle type:")
    print(vehicle_summary)

    print("\nHistorical cost by location category:")
    print(location_summary)

    print("\nHistorical cost by time of booking:")
    print(time_summary)

    print("\nHistorical cost by loyalty status:")
    print(loyalty_summary)


def create_category_charts(dataframe):
    vehicle_cost = (
        dataframe.groupby("Vehicle_Type")["Historical_Cost_of_Ride"].mean().round(2))

    plot_bar_chart(vehicle_cost,"Average Ride Cost by Vehicle Type","Vehicle Type","Average Historical Ride Cost")

    location_cost = (dataframe.groupby("Location_Category")["Historical_Cost_of_Ride"].mean().round(2))

    plot_bar_chart(
        location_cost,
        "Average Ride Cost by Location Category",
        "Location Category",
        "Average Historical Ride Cost"
    )

    time_cost = (
        dataframe.groupby("Time_of_Booking")["Historical_Cost_of_Ride"].mean().round(2).reindex([
            "Morning",
            "Afternoon",
            "Evening",
            "Night"
        ])
    )

    plot_bar_chart(
        time_cost,
        "Average Ride Cost by Time of Booking",
        "Time of Booking",
        "Average Historical Ride Cost"
    )

    loyalty_cost = (dataframe.groupby("Customer_Loyalty_Status")["Historical_Cost_of_Ride"].mean().round(2).reindex([
            "Regular",
            "Silver",
            "Gold"
        ])
    )

    plot_bar_chart(
        loyalty_cost,
        "Average Ride Cost by Customer Loyalty Status",
        "Customer Loyalty Status",
        "Average Historical Ride Cost"
    )


def run_eda(input_file, output_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Dataset not found: {input_file}"
        )

    dataframe = pd.read_csv(input_file)

    print("Cleaned dataset loaded successfully.")

    display_dataset_overview(dataframe)

    display_categorical_overview(dataframe)
    featured_dataframe = add_demand_supply_features(
        dataframe
    )

    print("\nDemand-and-supply variables:")
    print(
        featured_dataframe[
            ["Demand_Supply_Ratio","Demand_Supply_Difference"]].describe()
    )

    output_folder = os.path.dirname(output_file)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    featured_dataframe.to_csv(
        output_file,
        index=False
    )

    print(
        "\nDataset with demand-and-supply "
        "variables saved successfully."
    )

    print("Output file:", output_file)

    print("\nHistorical ride-cost statistics:")
    print(featured_dataframe["Historical_Cost_of_Ride"].describe())

    display_category_summaries(
        featured_dataframe
    )

    duration_vehicle_table = (
        create_duration_vehicle_table(
            featured_dataframe
        )
    )

    print(
        "\nAverage historical ride cost by "
        "duration group and vehicle type:"
    )

    print(duration_vehicle_table)

    plot_historical_cost_distribution(
        featured_dataframe
    )

    create_category_charts(
        featured_dataframe
    )

    plot_duration_and_cost(
        featured_dataframe
    )

    plot_past_rides_and_cost(
        featured_dataframe
    )

    plot_ratings_and_cost(
        featured_dataframe
    )

    print("\nEDA completed successfully.")

    return featured_dataframe


if __name__ == "__main__":
    input_file = (
        "Data/Cleaned/"
        "cleaned_dynamic_pricing.csv"
    )

    output_file = (
        "Data/Cleaned/"
        "cleaned_dynamic_pricing_with_features.csv"
    )
    run_eda(
        input_file,
        output_file
    )