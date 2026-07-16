# Data Pipeline & Dashboard Architecture Report

## Scope

This report covers the data pipeline that turns the raw ride-sharing CSV into cleaned data, engineered
features, and PNG charts, and the static dashboard that displays them: `data_cleaning.py`, `eda.py`,
`demand_supply.py`, `pricing_factor_analysis.py`, `save_chart.py`, `main.py`, and `Dasboard/`. The
ride-fare prediction model (`Ride-Fare Prediction Model/pricing.py`) is out of scope.

## Data / Input Structure

Input: `Data/Raw/dynamic_pricing(in).csv` — 1,000 rows, 10 columns, no unique ride ID or timestamp.

| Type | Columns |
|---|---|
| Numerical (6) | `Number_of_Riders`, `Number_of_Drivers`, `Number_of_Past_Rides`, `Average_Ratings`, `Expected_Ride_Duration`, `Historical_Cost_of_Ride` |
| Categorical (4) | `Location_Category`, `Customer_Loyalty_Status`, `Time_of_Booking`, `Vehicle_Type` |

The pipeline writes two derived CSVs to `Data/Cleaned/`: `cleaned_dynamic_pricing.csv` (post-cleaning)
and `cleaned_dynamic_pricing_with_features.csv` (post-cleaning + engineered demand/supply columns).

## Methodology / Workflow

`main.run_pipeline()` is the single orchestrator, called once from `if __name__ == "__main__"` with
project-relative paths. It runs one linear, non-branching pass:

1. **Clean & validate** (`data_cleaning.run_data_cleaning`) — load raw CSV, strip column/category
   whitespace, drop exact-duplicate rows, tally data-quality issues, assert zero issues remain, save.
2. **Feature engineering** (`eda.add_demand_supply_features`) — add `Demand_Supply_Ratio` and
   `Demand_Supply_Difference`; save the featured CSV.
3. **EDA charts** (`eda.py`) — distribution, category, and relationship charts against
   `Historical_Cost_of_Ride`.
4. **Demand/supply analysis** (`demand_supply.py`) — grouped summaries and pressure charts by location,
   time, loyalty, vehicle, and a location×time heatmap.
5. **Pricing-factor analysis** (`pricing_factor_analysis.py`) — correlation/regression/ANOVA-style views
   of numeric and categorical drivers of cost.

Every chart call passes `save=True`, so each function routes through `save_chart.save_chart()` instead
of `plt.show()`, writing a PNG into project-root `Charts/`.

## Code Architecture

| Module | Responsibility | Key functions |
|---|---|---|
| `data_cleaning.py` | Load, strip, dedupe, quality-check, assert, persist | `clean_text_values`, `count_unexpected_categories`, `count_textual_missing_values`, `count_invalid_numerical_values`, `clean_dataset` (builds a summary `DataFrame`), `validate_dataset` (hard assertions — quality gate), `run_data_cleaning` (I/O orchestrator) |
| `eda.py` | Feature engineering + descriptive/relationship charts | `add_demand_supply_features`, `classify_duration` / `create_duration_vehicle_table` (pivot: duration bucket × vehicle type), `plot_bar_chart` (generic helper reused by `create_category_charts`), `plot_historical_cost_distribution`, `plot_duration_and_cost`, `plot_past_rides_and_cost`, `plot_ratings_and_cost`, `display_*` (console-only summaries) |
| `demand_supply.py` | Demand-pressure grouping and charts | `add_demand_supply_level` (tertile bucketing via `qcut`), `summarise_by_location/time/loyalty/vehicle/demand_supply_level` (grouped means, fixed category order via `reindex`), `create_demand_supply_heatmap`, `find_surge_candidates`, 8 `plot_*` functions (bar, scatter, line, heatmap, horizontal bar) |
| `pricing_factor_analysis.py` | Cost-driver relationships | `plot_numeric_scatter` (fitted line + Pearson r, looped over `NUMERIC_COLUMNS`), `plot_correlation_heatmap`, `plot_categorical_box` (boxplot + manually computed one-way ANOVA F-statistic), `plot_demand_supply_scatter`, `plot_demand_supply_level` |
| `save_chart.py` | Single I/O sink for all charts | `save_chart(fig, filename)` — resolves/creates project-root `Charts/`, saves at `dpi=150`, `bbox_inches="tight"` |
| `main.py` | Orchestration only, no logic of its own | `run_pipeline(raw_file, cleaned_file, featured_file)` sequences steps 1–5 above and returns the final `DataFrame` |

Each plotting function follows the same pattern: build the figure with matplotlib, then branch on
`save` — `save_chart.save_chart(...)` for batch/pipeline use or `plt.show()` for interactive/notebook use.
Chart functions take already-summarised data (or the full featured `DataFrame`) as input and have no
side effects beyond producing a figure — all grouping/aggregation happens in sibling `summarise_*`/`create_*`
functions, keeping computation and rendering separate.

## Assumptions

- Categorical values are validated against a fixed whitelist (`EXPECTED_CATEGORIES`); anything else is
  **counted**, not corrected or dropped.
- A fixed list of textual missing-value markers (`NA`, `N/A`, `Unknown`, `None`, `-`) is treated as
  missing; no imputation is implemented (the pipeline assumes/requires the input already satisfies all
  checks — `validate_dataset` hard-asserts zero violations rather than fixing them).
- Duplicates are detected only as fully identical rows, since there is no ride ID to disambiguate
  genuinely repeated rides from coincidentally similar ones.
- Numeric validity ranges (riders/drivers > 0, past rides ≥ 0, ratings 1–5, duration > 0, cost > 0) are
  business-rule assumptions, not statistically derived.
- `Demand_Supply_Ratio`/`Difference` assume `Number_of_Riders` and `Number_of_Drivers` are simultaneous,
  comparable snapshot counts.
- `qcut`-based Low/Medium/High demand-supply tertiles assume a large-enough, roughly continuous
  distribution to split evenly.
- Correlation, regression-line, and ANOVA outputs throughout are descriptive associations only — the
  code makes no causal claims.

## Chart Generation → Dashboard Integration

All chart functions write static PNGs into `Charts/` (project root, created on demand). The dashboard
(`Dasboard/index.html`) is a plain static page with four `<section class="view">` blocks (EDA,
Demand & Supply, Pricing Factors, Fare Prediction) toggled by `script.js`, which just adds/removes an
`active` class on nav-button click — there is no build step, server, or dynamic data loading; each
`<img>` tag points directly at a relative `../Charts/<file>.png` path produced by the pipeline.
**Current limitation:** all four sections currently reference the same set of 7 EDA PNGs — the
demand-supply and pricing-factor charts generated by the pipeline are not yet wired into their
corresponding dashboard sections.
