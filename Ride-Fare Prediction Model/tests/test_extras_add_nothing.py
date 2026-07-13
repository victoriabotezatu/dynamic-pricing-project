import numpy as np
from scipy.stats import pearsonr
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression

import pricing


def test_extras_dont_help(data):
    base = pricing.mean_held_out_r2(data, pricing.BASE_FEATURES, LinearRegression())
    full = pricing.mean_held_out_r2(data, pricing.ALL_FEATURES, LinearRegression())
    assert full - base < pricing.EPS, (
        f"extras raised R^2 from {base:.4f} to {full:.4f} (>{pricing.EPS}) "
        "-- they would carry real signal"
    )


def test_line_beats_gbm_on_everything(data):
    line = pricing.mean_held_out_r2(data, pricing.BASE_FEATURES, LinearRegression())
    gbm_all = pricing.mean_held_out_r2(
        data, pricing.ALL_FEATURES, GradientBoostingRegressor(random_state=pricing.SEED)
    )
    assert line >= gbm_all - pricing.EPS, (
        f"line on [duration, vehicle] ({line:.4f}) lost to GBM-on-everything "
        f"({gbm_all:.4f}) by more than EPS={pricing.EPS}"
    )


def test_extras_no_better_than_random(data, train_df, test_df):
    rng = np.random.default_rng(pricing.SEED)
    random_col = "__random__"
    cols = pricing.ALL_FEATURES + [random_col]

    train = train_df.assign(**{random_col: rng.normal(size=len(train_df))})
    test = test_df.assign(**{random_col: rng.normal(size=len(test_df))})

    model = GradientBoostingRegressor(random_state=pricing.SEED)
    pipe = pricing.make_pipeline(cols, model).fit(train[cols], train[pricing.TARGET])
    result = permutation_importance(
        pipe, test[cols], test[pricing.TARGET],
        n_repeats=10, random_state=pricing.SEED, scoring="r2",
    )
    importance = dict(zip(cols, result.importances_mean))

    random_importance = importance[random_col]
    assert importance[pricing.DURATION] > random_importance + 10 * pricing.EPS

    for feature in pricing.EXTRA_FEATURES:
        assert importance[feature] <= random_importance + pricing.EPS, (
            f"{feature} importance {importance[feature]:.4f} exceeded the random "
            f"column ({random_importance:.4f}) by more than EPS={pricing.EPS}"
        )


def test_extras_not_significant(data):
    price = data[pricing.TARGET]
    for feature in pricing.NUMERIC_EXTRAS:
        r, p = pearsonr(data[feature], price)
        assert abs(r) < 0.1, f"{feature}: |r| = {abs(r):.4f}, expected < 0.1"
        assert p > 0.05, f"{feature}: p = {p:.4f}, expected > 0.05 (no real effect)"
