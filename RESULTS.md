## Tests: 11/11 passed

```
dynamicPricing/tests/test_duration_alone_explains_most.py::test_duration_alone_explains_most PASSED
dynamicPricing/tests/test_duration_alone_explains_most.py::test_linear_is_enough PASSED
dynamicPricing/tests/test_extras_add_nothing.py::test_extras_dont_help PASSED
dynamicPricing/tests/test_extras_add_nothing.py::test_line_beats_gbm_on_everything PASSED
dynamicPricing/tests/test_extras_add_nothing.py::test_extras_no_better_than_random PASSED
dynamicPricing/tests/test_extras_add_nothing.py::test_extras_not_significant PASSED
dynamicPricing/tests/test_positive_controls.py::test_vehicle_type_matters PASSED
dynamicPricing/tests/test_positive_controls.py::test_duration_matters PASSED
dynamicPricing/tests/test_reconstruct_generator.py::test_recover_rate PASSED
dynamicPricing/tests/test_reconstruct_generator.py::test_formula_reproduces_data PASSED
dynamicPricing/tests/test_reconstruct_generator.py::test_residuals_are_noise PASSED

11 passed in 1.10s
```

## Pricing: the recovered generator

`price = base[vehicle] + slope[vehicle] * Expected_Ride_Duration + noise`

| Vehicle | Base fare | Per-minute rate |
|---------|-----------|------------------|
| Economy | ~$0 (fit: -$5.53) | $3.56/min |
| Premium | ~$46 (fit: $46.15) | $3.50/min |

The per-minute rate is essentially identical across vehicles; the only real
difference is Premium's flat base fare.

## Model comparison (held-out R²)

| Model | R² |
|-------|-----|
| Duration only (linear) | 0.850 |
| Hand formula (base + slope·duration) | 0.869 |
| Line on [duration, vehicle] (mean, 5 seeds) | 0.878 |
| Gradient boosting on **all** features (mean, 5 seeds) | 0.870 |

**Takeaway:** a 3-line formula using only ride duration and vehicle type
matches (and even edges out) a gradient-boosted model given every available
feature. Riders, drivers, location, loyalty status, ratings, and time of
booking add no real predictive signal — their effect is statistically
indistinguishable from noise (see `test_extras_add_nothing.py`).
