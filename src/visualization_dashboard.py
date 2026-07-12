import os
import pandas as pd
import matplotlib.pyplot as plt
import eda


class PricingDashboard:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def _cost_distribution(self, ax):
        eda.plot_historical_cost_distribution(self.dataframe, ax)

    def _cost_by_vehicle(self, ax):
        vehicle_summary = eda.summarise_cost_by_category(self.dataframe, "Vehicle_Type")

        eda.plot_bar_chart(
            vehicle_summary["mean"],
            "Average Ride Cost by Vehicle Type",
            "Vehicle Type",
            "Average Historical Ride Cost",
            ax,
        )

    def _placeholder(self, ax, message):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.5, message, ha="center", va="center", wrap=True)

    def _demand_supply_panel(self, ax):
        self._placeholder(ax, "Pending: Sofia's demand/supply analysis")

    def _pricing_factors_panel(self, ax):
        self._placeholder(ax, "Pending: pricing factors analysis")

    def _fare_prediction_panel(self, ax):
        self._placeholder(ax, "Pending: fare prediction analysis")

    def _eta_prediction_panel(self, ax):
        self._placeholder(ax, "Pending: ETA prediction analysis")

    def build(self, save_path="pricing_dashboard.png"):
        fig, axes = plt.subplots(2, 3, figsize=(16, 9))

        self._cost_distribution(axes[0][0])
        self._cost_by_vehicle(axes[0][1])
        self._demand_supply_panel(axes[0][2])
        self._pricing_factors_panel(axes[1][0])
        self._fare_prediction_panel(axes[1][1])
        self._eta_prediction_panel(axes[1][2])

        fig.suptitle("Ride-Sharing Dynamic Pricing Dashboard")
        fig.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

        return fig


if __name__ == "__main__":
    input_file = "Data/Cleaned/" "cleaned_dynamic_pricing.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    dataframe = pd.read_csv(input_file)

    dashboard = PricingDashboard(dataframe)
    dashboard.build()

    print("Pricing dashboard saved successfully.")
