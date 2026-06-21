import pandas as pd


REQUIRED_COLUMNS = [
    "Invoice ID",
    "Branch",
    "City",
    "Customer type",
    "Gender",
    "Product line",
    "Unit price",
    "Quantity",
    "Tax 5%",
    "Total",
    "Date",
    "Time",
    "Payment",
    "cogs",
    "gross margin percentage",
    "gross income",
    "Rating"
]


def load_csv(uploaded_file):
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, f"Failed to load CSV file: {e}"


def validate_columns(df):
    """
    Check whether the uploaded dataset contains all required columns.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        return False, missing_columns

    return True, []


def validate_dataset(df):
    """
    Validate dataset structure and quality.
    """
    validation_results = {
        "row_count": df.shape[0],
        "column_count": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": list(df.columns)
    }

    is_valid_columns, missing_columns = validate_columns(df)

    validation_results["is_valid_columns"] = is_valid_columns
    validation_results["missing_columns"] = missing_columns

    return validation_results