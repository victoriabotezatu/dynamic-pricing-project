import os
import pandas as pd

CATEGORICAL_COLUMNS = [
    "Location_Category",
    "Customer_Loyalty_Status",
    "Time_of_Booking",
    "Vehicle_Type"
]
EXPECTED_CATEGORIES = {
    "Location_Category": [
        "Urban",
        "Suburban",
        "Rural"
    ],
    "Customer_Loyalty_Status": [
        "Regular",
        "Silver",
        "Gold"
    ],
    "Time_of_Booking": [
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ],
    "Vehicle_Type": [
        "Economy",
        "Premium"
    ]
}
MISSING_MARKERS = [
    "NA",
    "N/A",
    "Unknown",
    "None",
    "-"
]
def clean_text_values(dataframe, categorical_columns):
    cleaned_dataframe = dataframe.copy()
    cleaned_dataframe.columns = (
        cleaned_dataframe.columns.str.strip()
    )
    for column in categorical_columns:
        cleaned_dataframe[column] = (
            cleaned_dataframe[column].str.strip()
        )

    return cleaned_dataframe


def count_unexpected_categories(dataframe):
    unexpected_category_count = 0

    for column in CATEGORICAL_COLUMNS:
        for value in dataframe[column].unique():
            if value not in EXPECTED_CATEGORIES[column]:
                unexpected_category_count += 1

    return unexpected_category_count


def count_textual_missing_values(dataframe):
    textual_missing_count = 0

    for column in CATEGORICAL_COLUMNS:
        textual_missing_count += (
            dataframe[column]
            .isin(MISSING_MARKERS)
            .sum()
        )

    return textual_missing_count

def count_invalid_numerical_values(dataframe):
    invalid_values = {
        "Number_of_Riders": (dataframe["Number_of_Riders"] <= 0).sum(),

        "Number_of_Drivers": (dataframe["Number_of_Drivers"] <= 0).sum(),

        "Number_of_Past_Rides": (dataframe["Number_of_Past_Rides"] < 0).sum(),

        "Average_Ratings": ((dataframe["Average_Ratings"] < 1)|(dataframe["Average_Ratings"] > 5)).sum(),

        "Expected_Ride_Duration": (dataframe["Expected_Ride_Duration"] <= 0).sum(),

        "Historical_Cost_of_Ride": (dataframe["Historical_Cost_of_Ride"] <= 0).sum()
    }

    return invalid_values


def clean_dataset(dataframe):
    original_row_count = len(dataframe)

    cleaned_dataframe = clean_text_values(dataframe,CATEGORICAL_COLUMNS
    )

    duplicate_count = (cleaned_dataframe.duplicated().sum()
    )

    cleaned_dataframe = (cleaned_dataframe.drop_duplicates().copy()
    )

    rows_removed = (original_row_count- len(cleaned_dataframe)
    )

    blank_categorical_values = sum((cleaned_dataframe[column] == "").sum()for column in CATEGORICAL_COLUMNS
    )

    textual_missing_count = (count_textual_missing_values(cleaned_dataframe)
    )

    unexpected_category_count = (count_unexpected_categories(cleaned_dataframe)
    )

    invalid_values = (count_invalid_numerical_values(cleaned_dataframe)
    )

    cleaning_summary = pd.DataFrame({
        "Check": [
            "Original rows",
            "Final rows",
            "Columns",
            "Missing values",
            "Blank categorical values",
            "Textual missing markers",
            "Duplicate rows found",
            "Unexpected categories",
            "Invalid numerical values",
            "Rows removed",
            "Values imputed"
        ],
        "Result": [
            original_row_count,
            len(cleaned_dataframe),
            cleaned_dataframe.shape[1],
            cleaned_dataframe.isna().sum().sum(),
            blank_categorical_values,
            textual_missing_count,
            duplicate_count,
            unexpected_category_count,
            sum(invalid_values.values()),
            rows_removed,
            0
        ]
    })

    return cleaned_dataframe, cleaning_summary


def validate_dataset(dataframe):
    blank_categorical_values = sum((dataframe[column] == "").sum()for column in CATEGORICAL_COLUMNS)

    textual_missing_count = (count_textual_missing_values(dataframe))

    unexpected_category_count = (count_unexpected_categories(dataframe))

    invalid_values = (count_invalid_numerical_values(dataframe))

    assert dataframe.isna().sum().sum() == 0
    assert dataframe.duplicated().sum() == 0
    assert blank_categorical_values == 0
    assert textual_missing_count == 0
    assert unexpected_category_count == 0
    assert sum(invalid_values.values()) == 0

    assert (dataframe["Number_of_Riders"] <= 0).sum() == 0

    assert (dataframe["Number_of_Drivers"] <= 0).sum() == 0

    assert (dataframe["Number_of_Past_Rides"] < 0).sum() == 0

    assert (dataframe["Average_Ratings"] < 1).sum() == 0

    assert (dataframe["Average_Ratings"] > 5).sum() == 0

    assert (dataframe["Expected_Ride_Duration"] <= 0).sum() == 0

    assert (dataframe["Historical_Cost_of_Ride"] <= 0).sum() == 0

    print("All final data-quality checks passed.")


def run_data_cleaning(input_file, output_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Dataset not found: {input_file}"
        )

    dataframe = pd.read_csv(input_file)

    print("Dataset loaded successfully.")
    print("Original shape:", dataframe.shape)

    cleaned_dataframe, cleaning_summary = (clean_dataset(dataframe))

    validate_dataset(cleaned_dataframe)

    output_folder = os.path.dirname(output_file)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    cleaned_dataframe.to_csv(
        output_file,
        index=False
    )

    print("\nCleaning summary:")
    print(
        cleaning_summary.to_string(
            index=False
        )
    )

    print("\nCleaned dataset saved successfully.")
    print("Output file:", output_file)
    print("Final shape:", cleaned_dataframe.shape)

    return cleaned_dataframe


if __name__ == "__main__":
    input_file = (
        "Data/Raw/"
        "dynamic_pricing(in).csv"
    )

    output_file = (
        "Data/Cleaned/"
        "cleaned_dynamic_pricing.csv"
    )
    run_data_cleaning(input_file,output_file)