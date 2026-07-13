from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

import pricing


def test_duration_alone_explains_most(train_df, test_df):
    r2 = pricing.held_out_r2(train_df, test_df, pricing.DURATION_ONLY, LinearRegression())
    assert r2 > 0.80, f"duration-only held-out R^2 = {r2:.4f}, expected > 0.80"


def test_linear_is_enough(data):
   
    linear = pricing.mean_held_out_r2(data, pricing.BASE_FEATURES, LinearRegression())
    gbm = pricing.mean_held_out_r2(
        data, pricing.BASE_FEATURES, GradientBoostingRegressor(random_state=pricing.SEED)
    )
    assert gbm - linear < pricing.EPS, (
        f"GBM ({gbm:.4f}) beat linear ({linear:.4f}) by more than EPS={pricing.EPS} "
        "-- there would be real curvature to model"
    )
