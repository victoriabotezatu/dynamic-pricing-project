from scipy.stats import pearsonr, ttest_ind

import pricing


def test_vehicle_type_matters(data):
    cpm = pricing.cost_per_minute(data)
    economy = cpm[data[pricing.VEHICLE] == "Economy"]
    premium = cpm[data[pricing.VEHICLE] == "Premium"]

    t_stat, p_value = ttest_ind(economy, premium, equal_var=False)
    assert p_value < 1e-3, f"vehicle cost/min t-test p = {p_value:.2e}, expected < 1e-3"
    assert abs(economy.mean() - premium.mean()) > 0.5, "cost/min gap should be large"


def test_duration_matters(data):
    r, _ = pearsonr(data[pricing.DURATION], data[pricing.TARGET])
    assert r > 0.8, f"corr(duration, price) = {r:.4f}, expected > 0.8"
