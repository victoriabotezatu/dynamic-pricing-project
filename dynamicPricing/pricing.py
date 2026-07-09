
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# --- constants (defined once, reused everywhere) ---------------------------
SEED = 42
EPS = 0.02
SEEDS = (0, 1, 2, 3, 4)
TEST_SIZE = 0.25

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(_REPO_ROOT, "Data ", "Raw", "cleaned_dynamic_pricing.csv")

# --- columns ----------------------------------------------------------------
TARGET = "Historical_Cost_of_Ride"
DURATION = "Expected_Ride_Duration"
VEHICLE = "Vehicle_Type"

DURATION_ONLY = [DURATION]
BASE_FEATURES = [DURATION, VEHICLE]

# Everything except duration/vehicle
EXTRA_FEATURES = [
    "Number_of_Riders",
    "Number_of_Drivers",
    "Location_Category",
    "Customer_Loyalty_Status",
    "Number_of_Past_Rides",
    "Average_Ratings",
    "Time_of_Booking",
]
NUMERIC_EXTRAS = [
    "Number_of_Riders",
    "Number_of_Drivers",
    "Number_of_Past_Rides",
    "Average_Ratings",
]
ALL_FEATURES = EXTRA_FEATURES + BASE_FEATURES

# Columns that need one-hot encoding
CATEGORICAL = ["Location_Category", "Customer_Loyalty_Status", "Time_of_Booking", VEHICLE]


# --- data / pipeline --------------------------------------------------------
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def make_pipeline(cols, model):
   
    cat = [c for c in cols if c in CATEGORICAL]
    num = [c for c in cols if c not in CATEGORICAL]
    pre = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
            ("num", "passthrough", num),
        ]
    )
    return Pipeline([("pre", pre), ("model", model)])


def split_data(df: pd.DataFrame, *, seed: int = SEED, test_size: float = TEST_SIZE):
    
    return train_test_split(df, test_size=test_size, random_state=seed)


def held_out_r2(train_df, test_df, cols, model) -> float:
    pipe = make_pipeline(cols, clone(model)).fit(train_df[cols], train_df[TARGET])
    return float(r2_score(test_df[TARGET], pipe.predict(test_df[cols])))


def held_out_r2_seed(df, cols, model, *, seed: int = SEED) -> float:
    train_df, test_df = split_data(df, seed=seed)
    return held_out_r2(train_df, test_df, cols, model)


def mean_held_out_r2(df, cols, model, seeds=SEEDS) -> float:
    return float(np.mean([held_out_r2_seed(df, cols, clone(model), seed=s) for s in seeds]))


# --- the generator ------------------------------------------------
def per_vehicle_fit(df: pd.DataFrame) -> dict[str, tuple[float, float]]:
    params: dict[str, tuple[float, float]] = {}
    for vehicle, group in df.groupby(VEHICLE):
        lr = LinearRegression().fit(group[[DURATION]], group[TARGET])
        params[vehicle] = (float(lr.coef_[0]), float(lr.intercept_))
    return params


def formula_predict(df: pd.DataFrame, params: dict[str, tuple[float, float]]) -> pd.Series:
    slope = df[VEHICLE].map(lambda v: params[v][0])
    intercept = df[VEHICLE].map(lambda v: params[v][1])
    return intercept + slope * df[DURATION]


def cost_per_minute(df: pd.DataFrame) -> pd.Series:
    return df[TARGET] / df[DURATION]
