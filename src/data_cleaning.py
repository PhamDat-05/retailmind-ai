import pandas as pd


def clean_column_names(df):
    """
    Standardize column names to make them easier to use in Python.
    Example: 'Invoice ID' -> 'invoice_id'
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "percent")
    )

    return df


def clean_sales_data(df):
    """
    Clean and enrich supermarket sales data for analysis.
    """
    df = df.copy()

    # Standardize column names
    df = clean_column_names(df)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert time column and extract hour
    df["time"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce").dt.time
    df["hour"] = pd.to_datetime(df["time"].astype(str), format="%H:%M:%S", errors="coerce").dt.hour

    # Create date-related features
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()
    df["day_name"] = df["date"].dt.day_name()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    # Create business features
    df["profit_margin"] = df["gross_income"] / df["total"]
    df["revenue_per_unit"] = df["total"] / df["quantity"]

    return df