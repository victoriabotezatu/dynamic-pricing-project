import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

target = "Historical_Cost_of_Ride"
numeric_cols = [
    "Number_of_Riders",
    "Number_of_Drivers",
    "Number_of_Past_Rides",
    "Average_Ratings",
    "Expected_Ride_Duration",
]
categorical_cols = [
    "Location_Category",
    "Customer_Loyalty_Status",
    "Time_of_Booking",
    "Vehicle_Type",
]


def load_data():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(
        os.path.join(
            project_dir, "Data", "Cleaned", "cleaned_dynamic_pricing_with_features.csv"
        )
    )


# Price versus a single numeric factor
def plot_numeric_scatter(df, col):
    plt.scatter(df[col], df[target], alpha=0.4, s=15)

    slope, intercept = np.polyfit(df[col], df[target], 1)
    x_line = np.array([df[col].min(), df[col].max()])
    plt.plot(x_line, slope * x_line + intercept, color="red")

    r = df[col].corr(df[target])
    plt.xlabel(col, labelpad=15)
    plt.ylabel(target, labelpad=15)
    plt.title(f"{col} vs Price (r = {r:.2f})")
    plt.show()


# Correlation heatmap
def plot_correlation_heatmap(df):
    corr = df[numeric_cols + [target]].corr()

    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    plt.colorbar(label="Correlation")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.index)), corr.index)
    plt.title("Correlation Heatmap")

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            plt.text(j, i, round(corr.iloc[i, j], 2), ha="center", va="center")

    plt.tight_layout()
    plt.show()


# Effect of a single categorical factor on price
def plot_categorical_box(df, col):
    groups = [g[target].values for _, g in df.groupby(col)]
    grand_mean = df[target].mean()
    k = len(groups)
    n = len(df)
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)
    f_stat = (ss_between / (k - 1)) / (ss_within / (n - k))

    df.boxplot(column=target, by=col)
    plt.title(f"{col} (ANOVA F = {f_stat:.2f})")
    plt.suptitle("")
    plt.xlabel("")
    plt.ylabel(target)
    plt.xticks(rotation=20)
    plt.show()


# Price versus demand-supply pressure
def plot_demand_supply_scatter(df):
    plt.scatter(df["Demand_Supply_Ratio"], df[target], alpha=0.4, s=15)

    slope, intercept = np.polyfit(df["Demand_Supply_Ratio"], df[target], 1)
    x_line = np.array([df["Demand_Supply_Ratio"].min(), df["Demand_Supply_Ratio"].max()])
    plt.plot(x_line, slope * x_line + intercept, color="red")

    r = df["Demand_Supply_Ratio"].corr(df[target])
    plt.xlabel("Demand-Supply Ratio", labelpad=15)
    plt.ylabel(target, labelpad=15)
    plt.title(f"Demand-Supply Ratio vs Price (r = {r:.2f})")
    plt.show()


# Price by demand-supply level
def plot_demand_supply_level(df):
    df["Demand_Supply_Level"] = pd.qcut(
        df["Demand_Supply_Ratio"], 3, labels=["Low", "Medium", "High"]
    )

    df.boxplot(column=target, by="Demand_Supply_Level")
    plt.title("Price by Demand-Supply Level")
    plt.suptitle("")
    plt.xlabel("Demand-Supply Level")
    plt.ylabel(target)
    plt.show()


if __name__ == "__main__":
    df = load_data()

    for col in numeric_cols:
        plot_numeric_scatter(df, col)

    plot_correlation_heatmap(df)

    for col in categorical_cols:
        plot_categorical_box(df, col)

    plot_demand_supply_scatter(df)
    plot_demand_supply_level(df)
