import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import save_chart

TARGET = "Historical_Cost_of_Ride"
NUMERIC_COLUMNS = [
    "Number_of_Riders",
    "Number_of_Drivers",
    "Number_of_Past_Rides",
    "Average_Ratings",
    "Expected_Ride_Duration",
]
CATEGORICAL_COLUMNS = [
    "Location_Category",
    "Customer_Loyalty_Status",
    "Time_of_Booking",
    "Vehicle_Type",
]


def plot_numeric_scatter(dataframe, column, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.scatter(dataframe[column], dataframe[TARGET], alpha=0.4, s=15)

    slope, intercept = np.polyfit(dataframe[column], dataframe[TARGET], 1)
    x_line = np.array([dataframe[column].min(), dataframe[column].max()])
    plt.plot(x_line, slope * x_line + intercept, color="red")

    r = dataframe[column].corr(dataframe[TARGET])
    plt.xlabel(column, labelpad=15)
    plt.ylabel(TARGET, labelpad=15)
    plt.title(f"{column} vs Price (r = {r:.2f})")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, f"{column.lower()}_vs_price.png")
    else:
        plt.show()


def plot_correlation_heatmap(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    corr = dataframe[NUMERIC_COLUMNS + [TARGET]].corr()

    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    plt.colorbar(label="Correlation")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.index)), corr.index)
    plt.title("Correlation Heatmap")

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            plt.text(j, i, round(corr.iloc[i, j], 2), ha="center", va="center")

    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "correlation_heatmap.png")
    else:
        plt.show()


def plot_categorical_box(dataframe, column, save=False):
    groups = [group[TARGET].values for _, group in dataframe.groupby(column)]
    grand_mean = dataframe[TARGET].mean()
    k = len(groups)
    n = len(dataframe)
    ss_between = sum(len(group) * (group.mean() - grand_mean) ** 2 for group in groups)
    ss_within = sum(((group - group.mean()) ** 2).sum() for group in groups)
    f_stat = (ss_between / (k - 1)) / (ss_within / (n - k))

    ax = dataframe.boxplot(column=TARGET, by=column)
    fig = ax.get_figure()
    fig.set_size_inches(7, 4)

    plt.title(f"{column} (ANOVA F = {f_stat:.2f})")
    plt.suptitle("")
    plt.xlabel("")
    plt.ylabel(TARGET)
    plt.xticks(rotation=20)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, f"{column.lower()}_price_boxplot.png")
    else:
        plt.show()


def plot_demand_supply_scatter(dataframe, save=False):
    fig = plt.figure(figsize=(7, 4))

    plt.scatter(dataframe["Demand_Supply_Ratio"], dataframe[TARGET], alpha=0.4, s=15)

    slope, intercept = np.polyfit(dataframe["Demand_Supply_Ratio"], dataframe[TARGET], 1)
    x_line = np.array(
        [dataframe["Demand_Supply_Ratio"].min(), dataframe["Demand_Supply_Ratio"].max()]
    )
    plt.plot(x_line, slope * x_line + intercept, color="red")

    r = dataframe["Demand_Supply_Ratio"].corr(dataframe[TARGET])
    plt.xlabel("Demand-Supply Ratio", labelpad=15)
    plt.ylabel(TARGET, labelpad=15)
    plt.title(f"Demand-Supply Ratio vs Price (r = {r:.2f})")
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "demand_supply_ratio_vs_price.png")
    else:
        plt.show()


def plot_demand_supply_level(dataframe, save=False):
    dataframe["Demand_Supply_Level"] = pd.qcut(
        dataframe["Demand_Supply_Ratio"], 3, labels=["Low", "Medium", "High"]
    )

    ax = dataframe.boxplot(column=TARGET, by="Demand_Supply_Level")
    fig = ax.get_figure()
    fig.set_size_inches(7, 4)

    plt.title("Price by Demand-Supply Level")
    plt.suptitle("")
    plt.xlabel("Demand-Supply Level")
    plt.ylabel(TARGET)
    plt.tight_layout()

    if save:
        save_chart.save_chart(fig, "price_by_demand_supply_level.png")
    else:
        plt.show()
