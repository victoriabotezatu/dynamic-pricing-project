from scipy.stats import pearsonr
from sklearn.ensemble import GradientBoostingRegressor

import pricing


def test_recover_rate(data):
    params = pricing.per_vehicle_fit(data)
    economy_slope, economy_intercept = params["Economy"]
    premium_slope, premium_intercept = params["Premium"]

    assert abs(economy_intercept) < 10, f"Economy base fare {economy_intercept:.1f} not ~0"
    assert 30 < premium_intercept < 60, f"Premium base fare {premium_intercept:.1f} not ~46"
    assert abs(economy_slope - premium_slope) < 0.3, "per-minute slopes should match"
    assert 3.0 < economy_slope < 4.0 and 3.0 < premium_slope < 4.0


def test_formula_reproduces_data(train_df, test_df):

    from sklearn.metrics import r2_score

    params = pricing.per_vehicle_fit(train_df)
    formula_pred = pricing.formula_predict(test_df, params)
    formula_r2 = r2_score(test_df[pricing.TARGET], formula_pred)

    gbm_r2 = pricing.held_out_r2(
        train_df, test_df, pricing.ALL_FEATURES,
        GradientBoostingRegressor(random_state=pricing.SEED),
    )
    assert abs(formula_r2 - gbm_r2) < pricing.EPS, (
        f"hand formula R^2 {formula_r2:.4f} differs from GBM-on-everything "
        f"{gbm_r2:.4f} by more than EPS={pricing.EPS}"
    )


def test_residuals_are_noise(data):
    params = pricing.per_vehicle_fit(data)
    residual = data[pricing.TARGET] - pricing.formula_predict(data, params)

    for feature in pricing.NUMERIC_EXTRAS:
        r, _ = pearsonr(residual, data[feature])
        assert abs(r) < 0.15, f"residual has structure vs {feature}: |r| = {abs(r):.4f}"
        assert r ** 2 < 0.02, (
            f"{feature} explains {r ** 2:.1%} of residual variance -- more than a whisper"
        )
