import os
import data_cleaning
import eda
import demand_supply
import pricing_factor_analysis


def run_pipeline(raw_file, cleaned_file, featured_file):
    dataframe = data_cleaning.run_data_cleaning(raw_file, cleaned_file)

    print("\nCleaned dataset loaded successfully.")

    eda.display_dataset_overview(dataframe)

    eda.display_categorical_overview(dataframe)
    featured_dataframe = eda.add_demand_supply_features(dataframe)
    pricing_factor_analysis.plot_demand_supply_level(featured_dataframe, False)
    return

    # print("\nDemand-and-supply variables:")
    # print(
    #     featured_dataframe[
    #         ["Demand_Supply_Ratio", "Demand_Supply_Difference"]
    #     ].describe()
    # )

    # output_folder = os.path.dirname(featured_file)

    # if not os.path.exists(output_folder):
    #     os.mkdir(output_folder)

    # featured_dataframe.to_csv(featured_file, index=False)

    # print("\nDataset with demand-and-supply " "variables saved successfully.")

    # print("Output file:", featured_file)

    # print("\nHistorical ride-cost statistics:")
    # print(featured_dataframe["Historical_Cost_of_Ride"].describe())

    # eda.display_category_summaries(featured_dataframe)

    # duration_vehicle_table = eda.create_duration_vehicle_table(featured_dataframe)

    # print("\nAverage historical ride cost by " "duration group and vehicle type:")

    # print(duration_vehicle_table)

    # eda.plot_historical_cost_distribution(featured_dataframe, save=True)

    # eda.create_category_charts(featured_dataframe, save=True)

    # eda.plot_duration_and_cost(featured_dataframe, save=True)

    # eda.plot_past_rides_and_cost(featured_dataframe, save=True)

    # eda.plot_ratings_and_cost(featured_dataframe, save=True)

    # print("\nEDA completed successfully.")

    # print("\nDemand-and-supply analysis:")

    # demand_supply.display_dataset_overview(featured_dataframe)

    # demand_supply.plot_overall_demand_supply(featured_dataframe, save=True)

    # demand_supply.plot_demand_vs_supply(featured_dataframe, save=True)

    # demand_supply_leveled = demand_supply.add_demand_supply_level(featured_dataframe)
    # pressure_summary = demand_supply.summarise_by_demand_supply_level(
    #     demand_supply_leveled
    # )

    # print("\nDemand-supply pressure levels:")
    # print(pressure_summary)

    # demand_supply.plot_demand_supply_levels(pressure_summary, save=True)

    # location_summary = demand_supply.summarise_by_location(featured_dataframe)

    # print("\nDemand and supply by location:")
    # print(location_summary)

    # demand_supply.plot_demand_supply_by_location(location_summary, save=True)

    # highest_pressure_location = location_summary["Demand_Supply_Ratio"].idxmax()
    # print(
    #     f"Highest demand pressure location: {highest_pressure_location} "
    #     f"(ratio = {location_summary['Demand_Supply_Ratio'].max():.2f})"
    # )

    # time_summary = demand_supply.summarise_by_time(featured_dataframe)

    # print("\nDemand and supply by time of booking:")
    # print(time_summary)

    # demand_supply.plot_demand_pressure_by_time(time_summary, save=True)

    # heatmap_data = demand_supply.create_demand_supply_heatmap(featured_dataframe)

    # print("\nDemand pressure by location and time:")
    # print(heatmap_data)

    # demand_supply.plot_demand_pressure_heatmap(heatmap_data, save=True)

    # surge_candidates = demand_supply.find_surge_candidates(featured_dataframe)

    # print("\nTop demand pressure situations:")
    # print(surge_candidates.head(10).round(2))

    # demand_supply.plot_top_surge_candidates(surge_candidates, save=True)

    # loyalty_summary = demand_supply.summarise_by_loyalty(featured_dataframe)

    # print("\nDemand and supply by loyalty status:")
    # print(loyalty_summary)

    # demand_supply.plot_demand_pressure_by_loyalty(loyalty_summary, save=True)

    # vehicle_summary = demand_supply.summarise_by_vehicle(featured_dataframe)

    # print("\nDemand and supply by vehicle type:")
    # print(vehicle_summary)

    # demand_supply.plot_demand_supply_by_vehicle(vehicle_summary, save=True)

    # for vehicle, ratio in vehicle_summary["Demand_Supply_Ratio"].items():
    #     print(f"{vehicle}: average demand-supply ratio = {ratio:.2f}")

    # print("\nDemand-and-supply analysis completed successfully.")

    # print("\nPricing factor analysis:")

    # for column in pricing_factor_analysis.NUMERIC_COLUMNS:
    #     pricing_factor_analysis.plot_numeric_scatter(featured_dataframe, column, save=True)

    # pricing_factor_analysis.plot_correlation_heatmap(featured_dataframe, save=True)

    # for column in pricing_factor_analysis.CATEGORICAL_COLUMNS:
    #     pricing_factor_analysis.plot_categorical_box(featured_dataframe, column, save=True)

    # pricing_factor_analysis.plot_demand_supply_scatter(featured_dataframe, save=True)

    # pricing_factor_analysis.plot_demand_supply_level(featured_dataframe, save=True)

    # print("\nPricing factor analysis completed successfully.")

    # return featured_dataframe


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_file = os.path.join(project_root, "Data", "Raw", "dynamic_pricing(in).csv")

    cleaned_file = os.path.join(
        project_root, "Data", "Cleaned", "cleaned_dynamic_pricing.csv"
    )

    featured_file = os.path.join(
        project_root, "Data", "Cleaned", "cleaned_dynamic_pricing_with_features.csv"
    )

    run_pipeline(raw_file, cleaned_file, featured_file)
