# Data Cleaning Report

## Project Overview

This report summarizes the data-cleaning process applied to the dynamic-pricing ride-sharing dataset.

The main goal of this stage was to identify and address possible data-quality problems before performing exploratory data analysis and further modelling.

The cleaning process examined:

- dataset structure and data types
- column names
- missing and blank values
- textual missing-value markers
- duplicate records
- categorical labels
- invalid numerical values
- minimum, maximum, and potentially unusual numerical observations

## Dataset Information

The original dataset contained:

- 1,000 observations
- 10 variables
- 6 numerical variables
- 4 categorical variables

The variables included in the dataset are:

- `Number_of_Riders`
- `Number_of_Drivers`
- `Location_Category`
- `Customer_Loyalty_Status`
- `Number_of_Past_Rides`
- `Average_Ratings`
- `Time_of_Booking`
- `Vehicle_Type`
- `Expected_Ride_Duration`
- `Historical_Cost_of_Ride`

## Data-Cleaning Procedure

The dataset was loaded from:

`Data/Raw/dynamic_pricing(in).csv`

After loading the dataset, the following checks were performed:

### 1. Dataset Structure and Data Types

This consisted mainly in inspecting the number of rows, columns and the data type of each variable 

The conclusion was that the numerical variables were stored as integer or floating-point values, while the categorical variables were stored as text values.

But it is important to note that no incorrect data types were identified

### 2. Column Names and Text Values

This consisted mainly in checking column names for possible leading or trailing spaces.

The values in the categorical columns were also stripped of possible leading or trailing spaces:

- `Location_Category`
- `Customer_Loyalty_Status`
- `Time_of_Booking`
- `Vehicle_Type`

The conclusion is that no important inconsistencies were found after this operation.

### 3. Missing and Blank Values

This consisted mainly in checking the dataset for standard missing values in all columns.

The categorical columns were additionally checked for:

- empty strings
- `NA`
- `N/A`
- `Unknown`
- `None`
- `-`

In the end, no missing values, blank categorical values, or textual missing-value markers were found and that's why no values had to be imputed and no rows or columns had to be removed because of missing data

### 4. Duplicate Records

This consisted mainly in checking the dataset for completely identical rows.

The conclusion was that no exact duplicate rows were found and that's why no records were removed as duplicates

### 5. Categorical Values

This consisted mainly in comparing the categorical variables with the expected categories

The expected values were:

| Variable | Expected categories |
|---|---|
| `Location_Category` | Urban, Suburban, Rural |
| `Customer_Loyalty_Status` | Regular, Silver, Gold |
| `Time_of_Booking` | Morning, Afternoon, Evening, Night |
| `Vehicle_Type` | Economy, Premium |

And the conclusion is that no unexpected categories, spelling differences, or inconsistent category labels were identified

### 6. Numerical Validity Checks

This consisted mainly in checking the numerical variables using the following logical conditions:

- `Number_of_Riders` must be greater than zero
- `Number_of_Drivers` must be greater than zero
- `Number_of_Past_Rides` cannot be negative
- `Average_Ratings` must be between 1 and 5
- `Expected_Ride_Duration` must be greater than zero
- `Historical_Cost_of_Ride` must be greater than zero

The conclusion is that no invalid numerical values were found

The observed average ratings ranged from 3.5 to 5.0, which is within the expected 1-to-5 interval

### 7. Unusual High-Cost Observation

Given that the highest historical ride cost was approximately 836.12, we reviewed this observation and afterwards, associated it with a premium vehicle and an expected ride duration of 180 minutes.

In the end, because the observation represented a long premium ride and did not violate any logical data-quality condition, it was considered plausible and was not removed from the the dataset

## Cleaning Summary

| Check | Result |
|---|---:|
| Original rows | 1,000 |
| Final rows | 1,000 |
| Columns | 10 |
| Missing values | 0 |
| Blank categorical values | 0 |
| Textual missing markers | 0 |
| Duplicate rows | 0 |
| Unexpected categories | 0 |
| Invalid numerical values | 0 |
| Rows removed | 0 |
| Values imputed | 0 |

## Cleaned Dataset

After the necessary data cleaning operations/checks were performed, the validated dataset was saved as:

`Data/Cleaned/cleaned_dynamic_pricing.csv`

Because there was no need remove rows or impute values, the cleaned dataset contains the same 1,000 observations and 10 variables as the original dataset.

## Data-Cleaning Limitations

However, it is inportant to note that the dataset does not contain a unique ride identifier or an exact timestamp for each observation.

For this reason, during teh data cleaning process, duplicate detection was limited to identifying completely identical rows. Therefore, it was not possible to determine whether similar rows represented repeated records or separate rides with similar characteristics.

Additionally, the high-cost observations were assessed using the variables available in the dataset. The absence of information such as ride distance, route, exact location, and currency limits the possibility of validating ride costs using external business rules

## Conclusion

- The dataset was already in good condition

- No missing values, blank values, textual missing markers, exact duplicate rows, inconsistent categories, or impossible numerical values were identified

- The maximum historical ride cost was inspected and considered plausible because it was associated with a long premium ride

- All 1,000 observations were retained, and the cleaned dataset was saved for the exploratory data analysis stage