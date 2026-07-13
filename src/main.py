import os
import data_cleaning
import eda


def run_pipeline(raw_file, cleaned_file, featured_file):
    dataframe = data_cleaning.run_data_cleaning(raw_file, cleaned_file)

    print("\nCleaned dataset loaded successfully.")

    eda.display_dataset_overview(dataframe)

    eda.display_categorical_overview(dataframe)
    featured_dataframe = eda.add_demand_supply_features(dataframe)

    print("\nDemand-and-supply variables:")
    print(
        featured_dataframe[
            ["Demand_Supply_Ratio", "Demand_Supply_Difference"]
        ].describe()
    )

    output_folder = os.path.dirname(featured_file)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    featured_dataframe.to_csv(featured_file, index=False)

    print("\nDataset with demand-and-supply " "variables saved successfully.")

    print("Output file:", featured_file)

    print("\nHistorical ride-cost statistics:")
    print(featured_dataframe["Historical_Cost_of_Ride"].describe())

    eda.display_category_summaries(featured_dataframe)

    duration_vehicle_table = eda.create_duration_vehicle_table(featured_dataframe)

    print("\nAverage historical ride cost by " "duration group and vehicle type:")

    print(duration_vehicle_table)

    eda.plot_historical_cost_distribution(featured_dataframe, save=True)

    eda.create_category_charts(featured_dataframe, save=True)

    eda.plot_duration_and_cost(featured_dataframe, save=True)

    eda.plot_past_rides_and_cost(featured_dataframe, save=True)

    eda.plot_ratings_and_cost(featured_dataframe, save=True)

    print("\nEDA completed successfully.")

    return featured_dataframe


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_file = os.path.join(project_root, "Data", "Raw", "dynamic_pricing(in).csv")

    cleaned_file = os.path.join(project_root, "Data", "Cleaned", "cleaned_dynamic_pricing.csv")

    featured_file = os.path.join(
        project_root, "Data", "Cleaned", "cleaned_dynamic_pricing_with_features.csv"
    )

    run_pipeline(raw_file, cleaned_file, featured_file)
