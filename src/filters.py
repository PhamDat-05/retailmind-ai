import pandas as pd


def apply_filters(
    df,
    selected_cities,
    selected_branches,
    selected_product_lines,
    selected_customer_types,
    selected_payment_methods,
    selected_date_range
):
    """
    Apply user-selected filters to the cleaned sales dataset.
    """

    filtered_df = df.copy()

    if selected_cities:
        filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]

    if selected_branches:
        filtered_df = filtered_df[filtered_df["branch"].isin(selected_branches)]

    if selected_product_lines:
        filtered_df = filtered_df[
            filtered_df["product_line"].isin(selected_product_lines)
        ]

    if selected_customer_types:
        filtered_df = filtered_df[
            filtered_df["customer_type"].isin(selected_customer_types)
        ]

    if selected_payment_methods:
        filtered_df = filtered_df[
            filtered_df["payment"].isin(selected_payment_methods)
        ]

    if selected_date_range and len(selected_date_range) == 2:
        start_date = pd.to_datetime(selected_date_range[0])
        end_date = pd.to_datetime(selected_date_range[1])

        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) &
            (filtered_df["date"] <= end_date)
        ]

    return filtered_df