import pandas as pd
import numpy as np


# =========================
# Helper Functions
# =========================
def is_available(field_availability, field_key):
    """
    Check whether a business field is truly available from the uploaded dataset.
    """
    if not field_availability:
        return True

    return field_availability.get(field_key, {}).get("available", False)


def safe_sum(df, column):
    """
    Safely calculate sum for a numeric column.
    """
    if column not in df.columns:
        return 0

    return pd.to_numeric(df[column], errors="coerce").fillna(0).sum()


def safe_mean(df, column):
    """
    Safely calculate mean for a numeric column.
    """
    if column not in df.columns:
        return None

    value = pd.to_numeric(df[column], errors="coerce").mean()

    if pd.isna(value):
        return None

    return value


def get_top_group(df, group_col, value_col="total"):
    """
    Return top group and its revenue by a grouping column.
    """
    if group_col not in df.columns or value_col not in df.columns:
        return None, None

    grouped = (
        df.groupby(group_col, dropna=False)[value_col]
        .sum()
        .sort_values(ascending=False)
    )

    if grouped.empty:
        return None, None

    return grouped.index[0], grouped.iloc[0]


def get_lowest_group(df, group_col, value_col="total"):
    """
    Return lowest group and its revenue by a grouping column.
    """
    if group_col not in df.columns or value_col not in df.columns:
        return None, None

    grouped = (
        df.groupby(group_col, dropna=False)[value_col]
        .sum()
        .sort_values(ascending=True)
    )

    if grouped.empty:
        return None, None

    return grouped.index[0], grouped.iloc[0]


def get_best_rating_group(df, group_col, rating_col="rating"):
    """
    Return group with best average rating.
    """
    if group_col not in df.columns or rating_col not in df.columns:
        return None, None

    rating_df = df.dropna(subset=[rating_col])

    if rating_df.empty:
        return None, None

    grouped = (
        rating_df.groupby(group_col, dropna=False)[rating_col]
        .mean()
        .sort_values(ascending=False)
    )

    if grouped.empty:
        return None, None

    return grouped.index[0], grouped.iloc[0]


def get_worst_rating_group(df, group_col, rating_col="rating"):
    """
    Return group with worst average rating.
    """
    if group_col not in df.columns or rating_col not in df.columns:
        return None, None

    rating_df = df.dropna(subset=[rating_col])

    if rating_df.empty:
        return None, None

    grouped = (
        rating_df.groupby(group_col, dropna=False)[rating_col]
        .mean()
        .sort_values(ascending=True)
    )

    if grouped.empty:
        return None, None

    return grouped.index[0], grouped.iloc[0]


def format_currency(value):
    """
    Format a numeric value as currency text.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return f"${value:,.2f}"


def format_number(value, decimals=2):
    """
    Format numeric values safely.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return f"{value:,.{decimals}f}"


def format_plain(value):
    """
    Format plain values safely.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return str(value)


# =========================
# Overall KPI Calculation
# =========================
def calculate_overall_kpis(df, field_availability=None):
    """
    Calculate dynamic overall KPIs based on available fields.
    """
    total_revenue = safe_sum(df, "total")
    total_orders = len(df)
    total_quantity = safe_sum(df, "quantity")

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    has_profit = is_available(field_availability, "profit")
    has_rating = is_available(field_availability, "rating")

    gross_income = safe_sum(df, "gross_income") if has_profit else None

    profit_margin = None
    if has_profit and total_revenue > 0:
        profit_margin = gross_income / total_revenue * 100

    average_rating = safe_mean(df, "rating") if has_rating else None

    return {
        "total_revenue": total_revenue,
        "gross_income": gross_income,
        "profit_margin": profit_margin,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "average_order_value": average_order_value,
        "average_rating": average_rating,
        "has_profit": has_profit,
        "has_rating": has_rating
    }


# =========================
# Top Performer Calculation
# =========================
def calculate_top_performers(df, field_availability=None):
    """
    Calculate dynamic top-performing segments based on available fields.
    """
    has_city = is_available(field_availability, "city")
    has_branch = is_available(field_availability, "branch")
    has_product = is_available(field_availability, "product")
    has_payment = is_available(field_availability, "payment")
    has_customer_type = is_available(field_availability, "customer_type")
    has_rating = is_available(field_availability, "rating")

    top_city, top_city_revenue = (
        get_top_group(df, "city")
        if has_city
        else (None, None)
    )

    top_branch, top_branch_revenue = (
        get_top_group(df, "branch")
        if has_branch
        else (None, None)
    )

    top_product_line, top_product_line_revenue = (
        get_top_group(df, "product_line")
        if has_product
        else (None, None)
    )

    lowest_product_line, lowest_product_line_revenue = (
        get_lowest_group(df, "product_line")
        if has_product
        else (None, None)
    )

    top_payment_method, top_payment_revenue = (
        get_top_group(df, "payment")
        if has_payment
        else (None, None)
    )

    top_customer_type, top_customer_type_revenue = (
        get_top_group(df, "customer_type")
        if has_customer_type
        else (None, None)
    )

    best_rated_product_line, best_rating = (
        get_best_rating_group(df, "product_line")
        if has_product and has_rating
        else (None, None)
    )

    worst_rated_product_line, worst_rating = (
        get_worst_rating_group(df, "product_line")
        if has_product and has_rating
        else (None, None)
    )

    return {
        "top_city": top_city,
        "top_city_revenue": top_city_revenue,
        "top_branch": top_branch,
        "top_branch_revenue": top_branch_revenue,
        "top_product_line": top_product_line,
        "top_product_line_revenue": top_product_line_revenue,
        "lowest_product_line": lowest_product_line,
        "lowest_product_line_revenue": lowest_product_line_revenue,
        "top_payment_method": top_payment_method,
        "top_payment_revenue": top_payment_revenue,
        "top_customer_type": top_customer_type,
        "top_customer_type_revenue": top_customer_type_revenue,
        "best_rated_product_line": best_rated_product_line,
        "best_rating": best_rating,
        "worst_rated_product_line": worst_rated_product_line,
        "worst_rating": worst_rating,
        "has_city": has_city,
        "has_branch": has_branch,
        "has_product": has_product,
        "has_payment": has_payment,
        "has_customer_type": has_customer_type,
        "has_rating": has_rating
    }


# =========================
# Segment Summary Calculation
# =========================
def calculate_segment_summaries(df, field_availability=None):
    """
    Calculate segment summaries only for available fields.
    """
    summaries = {}

    has_product = is_available(field_availability, "product")
    has_city = is_available(field_availability, "city")
    has_branch = is_available(field_availability, "branch")
    has_customer_type = is_available(field_availability, "customer_type")
    has_payment = is_available(field_availability, "payment")
    has_rating = is_available(field_availability, "rating")

    if has_product:
        aggregations = {
            "total": "sum",
            "quantity": "sum",
            "invoice_id": "count"
        }

        if has_rating:
            aggregations["rating"] = "mean"

        revenue_by_product_line = (
            df.groupby("product_line", dropna=False)
            .agg(aggregations)
            .reset_index()
            .rename(
                columns={
                    "total": "revenue",
                    "quantity": "quantity_sold",
                    "invoice_id": "order_count",
                    "rating": "average_rating"
                }
            )
            .sort_values(by="revenue", ascending=False)
        )

        summaries["revenue_by_product_line"] = revenue_by_product_line
    else:
        summaries["revenue_by_product_line"] = None

    if has_city:
        summaries["revenue_by_city"] = (
            df.groupby("city", dropna=False)
            .agg(
                revenue=("total", "sum"),
                quantity_sold=("quantity", "sum"),
                order_count=("invoice_id", "count")
            )
            .reset_index()
            .sort_values(by="revenue", ascending=False)
        )
    else:
        summaries["revenue_by_city"] = None

    if has_branch:
        summaries["revenue_by_branch"] = (
            df.groupby("branch", dropna=False)
            .agg(
                revenue=("total", "sum"),
                quantity_sold=("quantity", "sum"),
                order_count=("invoice_id", "count")
            )
            .reset_index()
            .sort_values(by="revenue", ascending=False)
        )
    else:
        summaries["revenue_by_branch"] = None

    if has_customer_type:
        summaries["revenue_by_customer_type"] = (
            df.groupby("customer_type", dropna=False)
            .agg(
                revenue=("total", "sum"),
                quantity_sold=("quantity", "sum"),
                order_count=("invoice_id", "count")
            )
            .reset_index()
            .sort_values(by="revenue", ascending=False)
        )
    else:
        summaries["revenue_by_customer_type"] = None

    if has_payment:
        summaries["revenue_by_payment"] = (
            df.groupby("payment", dropna=False)
            .agg(
                revenue=("total", "sum"),
                quantity_sold=("quantity", "sum"),
                order_count=("invoice_id", "count")
            )
            .reset_index()
            .sort_values(by="revenue", ascending=False)
        )
    else:
        summaries["revenue_by_payment"] = None

    summaries["revenue_by_date"] = (
        df.groupby("date", dropna=False)
        .agg(
            revenue=("total", "sum"),
            quantity_sold=("quantity", "sum"),
            order_count=("invoice_id", "count")
        )
        .reset_index()
        .sort_values(by="date", ascending=True)
    )

    return summaries


# =========================
# AI KPI Context Builder
# =========================
def create_kpi_summary_text(
    overall_kpis,
    top_performers,
    field_availability=None
):
    """
    Create a dynamic KPI summary text for the AI model.
    This function avoids presenting unavailable fields as real zero values.
    """
    available_fields = []
    unavailable_fields = []

    if field_availability:
        for _, info in field_availability.items():
            if info["available"]:
                available_fields.append(info["label"])
            else:
                unavailable_fields.append(info["label"])

    summary_lines = []

    summary_lines.append("DATA AVAILABILITY")
    summary_lines.append("-----------------")

    if available_fields:
        summary_lines.append("Available business fields:")
        for field_name in available_fields:
            summary_lines.append(f"- {field_name}")

    if unavailable_fields:
        summary_lines.append("")
        summary_lines.append("Unavailable business fields:")
        for field_name in unavailable_fields:
            summary_lines.append(f"- {field_name}")

    summary_lines.append("")
    summary_lines.append("OVERALL KPIS")
    summary_lines.append("------------")
    summary_lines.append(f"Total Revenue: {format_currency(overall_kpis['total_revenue'])}")
    summary_lines.append(f"Total Orders: {overall_kpis['total_orders']:,}")
    summary_lines.append(f"Total Quantity Sold: {overall_kpis['total_quantity']:,.0f}")
    summary_lines.append(
        f"Average Order Value: {format_currency(overall_kpis['average_order_value'])}"
    )

    if overall_kpis["has_profit"]:
        summary_lines.append(f"Gross Income / Profit: {format_currency(overall_kpis['gross_income'])}")
        summary_lines.append(f"Profit Margin: {format_number(overall_kpis['profit_margin'])}%")
    else:
        summary_lines.append("Gross Income / Profit: Not available in uploaded dataset")
        summary_lines.append("Profit Margin: Not available in uploaded dataset")

    if overall_kpis["has_rating"]:
        summary_lines.append(f"Average Rating: {format_number(overall_kpis['average_rating'])}")
    else:
        summary_lines.append("Average Rating: Not available in uploaded dataset")

    summary_lines.append("")
    summary_lines.append("TOP PERFORMERS")
    summary_lines.append("--------------")

    if top_performers["has_city"]:
        summary_lines.append(
            f"Top City / Region: {format_plain(top_performers['top_city'])} "
            f"with revenue of {format_currency(top_performers['top_city_revenue'])}"
        )
    else:
        summary_lines.append("Top City / Region: Not available in uploaded dataset")

    if top_performers["has_branch"]:
        summary_lines.append(
            f"Top Branch / Store: {format_plain(top_performers['top_branch'])} "
            f"with revenue of {format_currency(top_performers['top_branch_revenue'])}"
        )
    else:
        summary_lines.append("Top Branch / Store: Not available in uploaded dataset")

    if top_performers["has_product"]:
        summary_lines.append(
            f"Top Product / Category: {format_plain(top_performers['top_product_line'])} "
            f"with revenue of {format_currency(top_performers['top_product_line_revenue'])}"
        )
        summary_lines.append(
            f"Lowest Revenue Product / Category: {format_plain(top_performers['lowest_product_line'])} "
            f"with revenue of {format_currency(top_performers['lowest_product_line_revenue'])}"
        )
    else:
        summary_lines.append("Product / Category performance: Not available in uploaded dataset")

    if top_performers["has_payment"]:
        summary_lines.append(
            f"Top Payment Method: {format_plain(top_performers['top_payment_method'])} "
            f"with revenue of {format_currency(top_performers['top_payment_revenue'])}"
        )
    else:
        summary_lines.append("Payment Method performance: Not available in uploaded dataset")

    if top_performers["has_customer_type"]:
        summary_lines.append(
            f"Top Customer Type / Segment: {format_plain(top_performers['top_customer_type'])} "
            f"with revenue of {format_currency(top_performers['top_customer_type_revenue'])}"
        )
    else:
        summary_lines.append("Customer Type / Segment performance: Not available in uploaded dataset")

    if top_performers["has_rating"] and top_performers["has_product"]:
        summary_lines.append(
            f"Best Rated Product / Category: {format_plain(top_performers['best_rated_product_line'])} "
            f"with average rating of {format_number(top_performers['best_rating'])}"
        )
        summary_lines.append(
            f"Worst Rated Product / Category: {format_plain(top_performers['worst_rated_product_line'])} "
            f"with average rating of {format_number(top_performers['worst_rating'])}"
        )
    else:
        summary_lines.append("Product rating performance: Not available in uploaded dataset")

    summary_lines.append("")
    summary_lines.append("IMPORTANT AI INSTRUCTIONS")
    summary_lines.append("-------------------------")
    summary_lines.append("- Use only the available metrics listed above.")
    summary_lines.append("- Do not infer unavailable fields as zero or poor performance.")
    summary_lines.append("- If profit, rating, payment, branch, city, or customer data is unavailable, clearly say it is not available.")
    summary_lines.append("- Do not invent numbers or unsupported business facts.")

    return "\n".join(summary_lines)