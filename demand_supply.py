import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("cleaned_dynamic_pricing_with_features.csv")

print(df.head())


df.info()
print("Location categories:", df["Location_Category"].unique())
print("Customer loyalty statuses:", df["Customer_Loyalty_Status"].unique())
print("Times of booking:", df["Time_of_Booking"].unique())
print("Vehicle types:", df["Vehicle_Type"].unique())


print(df[["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]].head())


overall_demand_supply = df[["Number_of_Riders", "Number_of_Drivers"]].mean()

print(overall_demand_supply)

# Overall demand and supply
plt.bar(["Demand: Riders", "Supply: Drivers"], overall_demand_supply.values)

plt.title("Average Demand and Supply")
plt.ylabel("Average Number")
plt.tick_params(axis="x", pad=10)
plt.show()


# Demand versus Supply
plt.scatter(df["Number_of_Drivers"], df["Number_of_Riders"], alpha=0.5)

plt.xlabel("Number of Drivers - Supply", labelpad=15)
plt.ylabel("Number of Riders - Demand", labelpad=15)
plt.title("Demand vs Supply")
plt.show()


df["Demand_Supply_Level"] = pd.qcut(
    df["Demand_Supply_Ratio"],
    3,
    labels=["Low", "Medium", "High"]
)

print(df[["Demand_Supply_Ratio", "Demand_Supply_Level"]].head())
print(df["Demand_Supply_Level"].value_counts())


pressure_summary = df.groupby("Demand_Supply_Level", observed=False)[
    ["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]
].mean()

pressure_summary = pressure_summary.reindex(["Low", "Medium", "High"])

print(pressure_summary.round(2))

# Summary by demand pressure level
plt.bar(pressure_summary.index, pressure_summary["Demand_Supply_Ratio"])

plt.xlabel("Demand-Supply Level", labelpad=15)
plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
plt.title("Demand Pressure Levels")
plt.tick_params(axis="x", pad=10)

for i, value in enumerate(pressure_summary["Demand_Supply_Ratio"]):
    plt.text(i, value, round(value, 2), ha="center", va="bottom")

plt.show()


location_order = ["Rural", "Suburban", "Urban"]

location_summary = df.groupby("Location_Category")[
    ["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]
].mean()

location_summary = location_summary.reindex(location_order)

print(location_summary.round(2))

# Demand and supply by location
location_summary[["Number_of_Riders", "Number_of_Drivers"]].plot(kind="bar")

plt.xlabel("Location Category", labelpad=15)
plt.ylabel("Average Number", labelpad=15)
plt.title("Average Demand and Supply by Location")
plt.tick_params(axis="x", pad=10)
plt.xticks(rotation=0)
plt.show()


highest_pressure_location = location_summary["Demand_Supply_Ratio"].idxmax()
print(f"Highest demand pressure location: {highest_pressure_location} "
      f"(ratio = {location_summary['Demand_Supply_Ratio'].max():.2f})")


time_order = ["Morning", "Afternoon", "Evening", "Night"]

time_summary = df.groupby("Time_of_Booking")[
    ["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]
].mean()

time_summary = time_summary.reindex(time_order)

print(time_summary.round(2))

# Demand and supply by time of booking
plt.plot(time_summary.index, time_summary["Demand_Supply_Ratio"], marker="o")

plt.xlabel("Time of Booking", labelpad=15)
plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
plt.title("Demand Pressure by Time of Booking")
plt.tick_params(axis="x", pad=10)
plt.show()


heatmap_data = pd.pivot_table(
    df,
    values="Demand_Supply_Ratio",
    index="Location_Category",
    columns="Time_of_Booking",
    aggfunc="mean"
)

heatmap_data = heatmap_data.reindex(
    index=["Rural", "Suburban", "Urban"],
    columns=["Morning", "Afternoon", "Evening", "Night"]
)

print(heatmap_data.round(2))

# Location and time together
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

plt.show()


surge_candidates = df.groupby(["Location_Category", "Time_of_Booking"])[
    "Demand_Supply_Ratio"
].mean().reset_index()

surge_candidates = surge_candidates.sort_values("Demand_Supply_Ratio", ascending=False)

print(surge_candidates.head(10).round(2))
top_surge = surge_candidates.head(5).copy()
top_surge["Market_Situation"] = top_surge["Location_Category"] + " - " + top_surge["Time_of_Booking"]

# Top demand pressure situations
plt.bar(top_surge["Market_Situation"], top_surge["Demand_Supply_Ratio"])

plt.xlabel("Market Situation", labelpad=15)
plt.ylabel("Average Demand-Supply Ratio", labelpad=15)
plt.title("Top 5 Demand Pressure Situations")
plt.tick_params(axis="x", pad=10)
plt.xticks(rotation=30)

for i, value in enumerate(top_surge["Demand_Supply_Ratio"]):
    plt.text(i, value, round(value, 2), ha="center", va="bottom")

plt.show()


loyalty_order = ["Regular", "Silver", "Gold"]

loyalty_summary = df.groupby("Customer_Loyalty_Status")[
    ["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]
].mean()

loyalty_summary = loyalty_summary.reindex(loyalty_order)

print(loyalty_summary.round(2))

# Demand pressure by customer loyalty status
plt.barh(loyalty_summary.index, loyalty_summary["Demand_Supply_Ratio"])

plt.xlabel("Average Demand-Supply Ratio", labelpad=15)
plt.ylabel("Customer Loyalty Status", labelpad=15)
plt.title("Demand Pressure by Customer Loyalty Status")
plt.show()


vehicle_order = ["Economy", "Premium"]

vehicle_summary = df.groupby("Vehicle_Type")[
    ["Number_of_Riders", "Number_of_Drivers", "Demand_Supply_Difference", "Demand_Supply_Ratio"]
].mean()

vehicle_summary = vehicle_summary.reindex(vehicle_order)

print(vehicle_summary.round(2))

# Demand and supply by vehicle type
vehicle_summary[["Number_of_Riders", "Number_of_Drivers"]].plot(kind="bar")

plt.xlabel("Vehicle Type", labelpad=15)
plt.ylabel("Average Number", labelpad=15)
plt.title("Average Demand and Supply by Vehicle Type")
plt.tick_params(axis="x", pad=10)
plt.xticks(rotation=0)
plt.show()
for vehicle, ratio in vehicle_summary["Demand_Supply_Ratio"].items():
    print(f"{vehicle}: average demand-supply ratio = {ratio:.2f}")


