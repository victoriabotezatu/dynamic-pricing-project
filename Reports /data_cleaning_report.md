# Data Cleaning Report

## Project Overview

This report summarizes the data cleaning process for the dynamic pricing ride-sharing dataset. The goal of this step was to check the dataset for common data quality issues before starting exploratory data analysis.

## Dataset Information

The dataset contains information about:

* ride-sharing demand
* driver supply
* customer details
* ride duration
* historical ride cost

The dataset contains:

* 1000 rows
* 10 columns

The columns are:

* Number_of_Riders
* Number_of_Drivers
* Location_Category
* Customer_Loyalty_Status
* Number_of_Past_Rides
* Average_Ratings
* Time_of_Booking
* Vehicle_Type
* Expected_Ride_Duration
* Historical_Cost_of_Ride

## Cleaning Checks Performed

The following checks were completed:

* Checked the dataset shape.
* Reviewed column names and data types.
* Checked for missing values.
* Checked for duplicate rows.
* Checked categorical columns for inconsistent labels.
* Checked numerical columns for impossible values.
* Saved the cleaned dataset in the Data/Cleaned folder.

## Missing Values

No missing values were found in the dataset. Therefore, no rows or columns had to be removed or filled because of missing data.

## Duplicate Records

No duplicate rows were found in the dataset. Therefore, no duplicate records had to be removed.

## Column Names

Column names were checked and cleaned to remove possible extra spaces. No major column name issues were found.

## Categorical Variables

The categorical variables contained consistent labels:

* Location_Category: Urban, Suburban, Rural
* Customer_Loyalty_Status: Silver, Regular, Gold
* Time_of_Booking: Night, Evening, Afternoon, Morning
* Vehicle_Type: Premium, Economy

No spelling mistakes or inconsistent category labels were found.

## Numerical Variables

The numerical columns were checked for impossible values.

The checks showed:

* Number_of_Riders values are positive.
* Number_of_Drivers values are positive.
* Expected_Ride_Duration values are positive.
* Historical_Cost_of_Ride values are positive.
* Average_Ratings ranges from 3.5 to 5.0. Since ratings were assumed to use a 0 to 5 scale, no invalid rating values were found.

No impossible numerical values were found.

## Dataset Limitations

The dataset does not include some real-time ride-sharing information such as customer coordinates, driver coordinates, waiting time, or driver arrival time.

Because these columns are not available, the analysis is limited to the variables included in the dataset, such as rider demand, driver supply, booking time, location category, vehicle type, ride duration, and historical ride cost.

## Cleaned Dataset

Since no major data quality problems were found, the cleaned dataset was saved without removing any rows.

The cleaned dataset was saved as:

Data/Cleaned/cleaned_dynamic_pricing.csv

## Cleaning Summary

| Check          | Result |
| -------------- | -----: |
| Rows           |   1000 |
| Columns        |     10 |
| Missing Values |      0 |
| Duplicate Rows |      0 |

## Conclusion

The dataset was already in good condition. No missing values, duplicate rows, inconsistent categories, or impossible numerical values were found. No rows or columns had to be removed during the cleaning process. The cleaned dataset was saved and is ready for exploratory data analysis.