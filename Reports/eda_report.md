# Exploratory Data Analysis Report

## Project Overview

This report has the main goal to explain the process and findings of the exploratory data analysis of the cleaned dynamic-pricing ride-sharing dataset. 
Therefore, we tried to keep it coincise and put forward only the main findings. 

The main objective of the analysis was to describe the distribution of historical ride cost and identify ride characteristics that show the clearest descriptive relationships with cost.

It is important to note that the analysis focuses on descriptive associations and does not attempt to establish causal relationships


## Research Questions

The exploratory analysis addresses the following questions:

1. Which ride characteristics show the clearest relationship with historical ride cost?

2. How does historical ride cost differ across vehicle types, locations, booking times and customer loyalty groups, and does the vehicle-type difference remain visible across different ride-duration groups?

## Dataset Information

The analysis used the cleaned dataset from the data cleaning analysis saved as:

`Data/Cleaned/cleaned_dynamic_pricing.csv`

The dataset contains:

- 1,000 observations
- 10 original variables
- 6 numerical variables
- 4 categorical variables

The target variable examined in this report is:

`Historical_Cost_of_Ride`

## Analysis Methods

The exploratory analysis included:

- descriptive statistics
- category frequencies
- histograms
- grouped summaries using count, mean, and median
- bar charts for categorical comparisons
- scatterplots for numerical comparisons
- duration-group classification
- a pivot table comparing vehicle type across duration groups

Additionaly, two additional demand-and-supply variables were also prepared for the team member responsible for the detailed demand-and-supply analysis.

## Demand-and-Supply Feature Preparation

The following variables were created:

### Demand-Supply Ratio

`Demand_Supply_Ratio = Number_of_Riders / Number_of_Drivers`

### Demand-Supply Difference

`Demand_Supply_Difference = Number_of_Riders - Number_of_Drivers`

These variables were added for reuse in the separate demand-and-supply analysis. 

- Note: The detailed interpretation of demand–supply conditions or surge-pricing situations is not made in this report in order to avoid overlap with the work of the team member responsible for that analysis

The updated dataset containing the two additional variables was saved as:

`Data/Cleaned/cleaned_dynamic_pricing_with_features.csv`

## Historical Ride-Cost Distribution

Historical ride cost has the following main descriptive statistics:

| Statistic | Historical ride cost |
|---|---:|
| Count | 1,000 |
| Mean | 372.50 |
| Median | 362.02 |
| Standard deviation | 187.16 |
| Minimum | 25.99 |
| First quartile | 221.37 |
| Third quartile | 510.50 |
| Maximum | 836.12 |

Observations: 

- The mean is slightly higher than the median, indicating that some higher-cost observations raise the average

- The middle 50% of observations have historical ride costs between approximately 221.37 and 510.50

- The highest observations were retained because they were associated with long rides and did not violate the data-quality rules

## Historical Ride Cost by Vehicle Type

Premium rides have a higher average historical ride cost than economy rides.

| Vehicle type | Average historical cost |
|---|---:|
| Economy | 346.57 |
| Premium | 396.25 |

Observations: 

- The average difference is approximately 49.68.

- Vehicle type shows the clearest difference among the categorical comparisons included in this EDA.

- This difference should still be interpreted carefully because other variables, especially ride duration, may also contribute to the observed cost difference

## Historical Ride Cost by Location Category

Rural rides have the highest average historical ride cost, followed by suburban and urban rides.

However, the differences between the location categories are relatively small compared with the difference between vehicle types.

The observed location differences may also reflect differences in ride duration or other ride characteristics. 

It is important to note that the categories only describe broad location types and do not provide exact origins, destinations, or routes

## Historical Ride Cost by Time of Booking

Afternoon bookings have the highest average historical ride cost.

Morning bookings have a similar average, while evening and night bookings have somewhat lower averages.

The differences between booking periods are relatively small. Therefore, time of booking does not show as clear a descriptive relationship with cost as expected ride duration or vehicle type

## Historical Ride Cost by Customer Loyalty Status

Regular customers have the highest average historical ride cost, followed by Gold and Silver customers.

However, the differences between loyalty groups are small.

The results do not demonstrate that loyalty status causes higher or lower ride costs. Differences may be related to the types of rides booked by customers in each group

## Expected Ride Duration and Historical Ride Cost

The scatterplot between expected ride duration and historical ride cost shows a clear positive descriptive association.

Longer expected rides generally have higher historical costs.

Both economy and premium rides follow this upward pattern. At similar ride durations, premium observations generally appear above economy observations.

This indicates that expected ride duration and vehicle type are the two variables with the clearest descriptive relationships with historical ride cost in this part of the analysis

## Duration Groups and Vehicle Type

Expected ride duration was divided into three groups:

- Short: 60 minutes or less
- Medium: more than 60 and up to 120 minutes
- Long: more than 120 minutes

The average historical ride costs were:

| Duration group | Economy | Premium |
|---|---:|---:|
| Short | 118.42 | 170.61 |
| Medium | 314.02 | 357.77 |
| Long | 532.79 | 571.95 |

Observations:

- Average historical cost increases substantially from short to medium and long rides

- Premium rides also have higher average costs than economy rides within every duration group

- This comparison supports the descriptive finding that both ride duration and vehicle type are associated with historical ride cost

## Number of Past Rides and Historical Ride Cost

The scatterplot between the number of past rides and historical ride cost does not show a clear standalone pattern.

Customers with both low and high numbers of past rides appear across a wide range of historical ride costs.

Therefore, the number of past rides does not appear to be a strong direct pricing factor when examined by itself.

It may still provide useful information when considered together with other variables in a predictive model.

## Average Ratings and Historical Ride Cost

The scatterplot between average customer ratings and historical ride cost does not show a clear standalone relationship.

Low and high historical ride costs occur across the available rating range.

Average ratings therefore do not appear to be a strong direct pricing factor in this descriptive analysis.

The variable may still contribute information when combined with other variables during modelling

## Main Findings

The main findings from the exploratory analysis are:

- Historical ride cost has a mean of approximately 372.50 and a median of approximately 362.02
- Expected ride duration shows the clearest positive descriptive relationship with historical ride cost
- Longer rides generally have higher historical costs
- Premium rides have higher average historical costs than economy rides
- The premium–economy difference remains visible within short, medium, and long duration groups
- Vehicle type shows the largest observed difference among the categorical comparisons
- Rural rides have a slightly higher average cost than suburban and urban rides
- Afternoon and morning bookings have slightly higher average costs than evening and night bookings
- Customer loyalty groups show relatively small cost differences
- Number of past rides and average ratings do not show clear standalone relationships with historical ride cost
- The findings represent descriptive associations and should not be interpreted as proof of causation

## Dataset Limitations

The analysis is affected by several dataset limitations

### Missing Ride Identifiers

The dataset does not contain a unique ride or customer identifier. Individual rides and repeated customer observations cannot be tracked

### No Exact Dates or Timestamps

`Time_of_Booking` contains only broad periods such as Morning, Afternoon, Evening, and Night.

It is therefore not possible to study daily, wekly, seasonal, or event-related pricing patterns

### No Distance or Route Information

The dataset includes expected ride duration but does not include ride distance, origin, destination, or route characteristics.

Ride cost differences cannot be fully separated into duration, distance, and route effects

### Broad Location Categories

Location is represented only by Urban, Suburban, and Rural categories.

These broad categories may combine locations with very different ride conditions

### Unspecified Currency

The currency used for `Historical_Cost_of_Ride` is not provided. The analysis therefore compares relative ride costs rather than interpreting the values in a specific currency

### No Observed Surge-Pricing Variable

The dataset does not contain an observed surge multiplier or an official surge-pricing indicator.

Surge conditions cannot be directly confirmed from the variables available in this EDA

### Demand and Supply Coverage

All observations contain more riders than drivers.

The dataset therefore does not allow comparison with balanced-market or driver-surplus situations

### Observational Analysis

The EDA identifies patterns and associations within the available dataset.

The results do not demonstrate that any individual variable causes ride cost to increase or decrease

## Conclusion

The exploratory analysis indicates that expected ride duration and vehicle type have the clearest descriptive relationships with historical ride cost.

Longer rides are generally more expensive, and premium rides have higher average costs than economy rides. The premium–economy difference remains visible across short, medium, and long ride-duration groups.

Location category, booking time, and loyalty status show smaller differences. Number of past rides and average ratings do not show clear standalone relationships with historical ride cost.

The two demand-and-supply variables were prepared and saved for the separate demand-and-supply analysis