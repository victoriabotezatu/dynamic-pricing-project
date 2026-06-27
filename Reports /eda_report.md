# Exploratory Data Analysis Report

## Project Overview

This report summarizes the exploratory data analysis for the cleaned dynamic pricing ride-sharing dataset. The goal of the EDA was to understand patterns in ride cost, demand, supply, customer behavior, and ride characteristics.

The analysis focuses on identifying which factors may influence ride pricing and how these factors can support a dynamic pricing strategy.

## Dataset Overview

The cleaned dataset contains:

* 1000 rows
* 10 original columns

The dataset includes information about:

* rider demand
* driver supply
* location category
* customer loyalty status
* number of past rides
* average ratings
* time of booking
* vehicle type
* expected ride duration
* historical ride cost

The main pricing variable analyzed in this report is `Historical_Cost_of_Ride`.

## New Columns Created

Three new columns were created during the EDA process:

* `Demand_Supply_Ratio`: compares the number of riders to the number of available drivers.
* `Demand_Supply_Difference`: shows the difference between riders and drivers.
* `Cost_per_Minute`: compares ride cost while considering expected ride duration.

These columns were created because the dataset does not include real-time information such as customer coordinates, driver coordinates, waiting time, or driver arrival time.

The new columns help analyze demand pressure, supply availability, and pricing differences more clearly.

## Historical Ride Cost Distribution

Historical ride cost varies across the dataset.

Most ride costs are between approximately 221 and 510, based on the 25% and 75% values from the summary statistics. This shows that ride costs are spread across a wide range, making historical ride cost an important variable for pricing analysis.

The distribution of historical ride cost helps show how ride prices are spread and whether there are many low-cost or high-cost rides in the dataset.

## Average Ride Cost by Category

Average historical ride cost was compared across vehicle type, location category, time of booking, and customer loyalty status.

The main findings were:

* Premium rides have a higher average cost than economy rides.
* Rural locations have the highest average ride cost.
* Afternoon and morning bookings have slightly higher average ride costs than evening and night bookings.
* Customer loyalty status shows only small differences in average ride cost.

These results suggest that vehicle type, location category, time of booking, and customer loyalty status may be useful pricing factors.

## Demand and Supply Analysis

Demand and supply were analyzed using `Number_of_Riders`, `Number_of_Drivers`, `Demand_Supply_Ratio`, and `Demand_Supply_Difference`.

The analysis shows that rider demand is higher than driver supply across the dataset. On average, the dataset has around 60 riders and 27 available drivers per scenario.

Average demand-supply ratio by location:

* Rural: 3.51
* Suburban: 3.13
* Urban: 3.07

This means that rural areas have the highest number of riders per available driver on average. This may indicate stronger demand pressure in rural locations.

Average demand-supply ratio by time of booking:

* Afternoon: 3.12
* Evening: 3.19
* Morning: 3.19
* Night: 3.42

Night bookings have the highest average demand-supply ratio, which may suggest stronger demand pressure at night.

The scatter plot between demand-supply ratio and historical ride cost does not show a very clear linear relationship. However, demand and supply are still important to explore because they are central to dynamic pricing.

## Cost per Minute Analysis

Cost per minute was created to compare ride prices more fairly because longer rides usually have higher total costs.

The main findings were:

* Premium rides have a higher average cost per minute than economy rides.
* Cost per minute is similar across location categories.

This suggests that vehicle type may be an important pricing factor when ride duration is considered.

## Ride Duration and Ride Cost

Expected ride duration shows a clear positive relationship with historical ride cost.

This means that longer rides usually have higher costs. Expected ride duration appears to be one of the most important pricing factors in the dataset.

This relationship is important because ride duration directly affects the amount of time and resources needed for a ride.

## Customer History and Ratings

The number of past rides does not show a clear relationship with historical ride cost.

Average ratings also do not show a clear relationship with historical ride cost.

However, these variables are still useful to explore because they describe customer behavior and service quality. They may also be useful in later stages of the project if customer-based pricing patterns are explored further.

## Key Findings

* Premium rides cost more than economy rides.
* Rural locations have the highest average ride cost and the highest demand-supply ratio.
* Night bookings have the highest average demand-supply ratio.
* Afternoon and morning bookings have slightly higher average ride costs than evening and night bookings.
* Demand is higher than driver supply across the dataset.
* Demand-supply ratio does not show a clear linear relationship with ride cost.
* Expected ride duration has a clear positive relationship with historical ride cost.
* Cost per minute helps compare rides more fairly because it considers ride duration.
* Number of past rides and average ratings do not show a clear relationship with ride cost.

## Most Important Pricing Factors

Based on the EDA, the most important pricing factor appears to be expected ride duration because it shows a clear positive relationship with historical ride cost.

Vehicle type is also important because premium rides have higher average costs and higher cost per minute than economy rides.

Location category, time of booking, and demand-supply conditions may also affect pricing, but their relationships with ride cost are less direct than ride duration and vehicle type.

## Conclusion

The EDA shows that expected ride duration and vehicle type are the strongest pricing factors in the dataset. Location category, time of booking, and demand-supply conditions also provide useful context for dynamic pricing.

These insights can support the next steps of the project, including pricing factor analysis, ride fare prediction, and business recommendations.
