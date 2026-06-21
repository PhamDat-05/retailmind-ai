import pandas as pd


# =========================
# Formatting Helpers
# =========================
def format_currency(value):
    """
    Format numeric value as currency.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return f"${value:,.2f}"


def format_number(value, decimals=2):
    """
    Format numeric value safely.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return f"{value:,.{decimals}f}"


def format_plain(value):
    """
    Format plain text value safely.
    """
    if value is None or pd.isna(value):
        return "Not available"

    return str(value)


def is_available(field_availability, field_key):
    """
    Check whether a business field is available.
    """
    if not field_availability:
        return True

    return field_availability.get(field_key, {}).get("available", False)


# =========================
# AI Context Sections
# =========================
def build_data_availability_section(field_availability):
    """
    Build data availability section for AI context.
    """
    lines = []

    lines.append("1. DATA AVAILABILITY")
    lines.append("--------------------")

    available_fields = []
    unavailable_fields = []

    if field_availability:
        for _, info in field_availability.items():
            if info["available"]:
                mapped_column = info.get("mapped_column") or "Unknown"
                available_fields.append(
                    f"- {info['label']} | mapped from CSV column: {mapped_column}"
                )
            else:
                unavailable_fields.append(f"- {info['label']}")

    if available_fields:
        lines.append("Available business fields:")
        lines.extend(available_fields)
    else:
        lines.append("Available business fields: Not specified")

    lines.append("")

    if unavailable_fields:
        lines.append("Unavailable business fields:")
        lines.extend(unavailable_fields)
    else:
        lines.append("Unavailable business fields: None")

    return "\n".join(lines)


def build_overall_kpi_section(overall_kpis):
    """
    Build overall KPI section for AI context.
    """
    lines = []

    lines.append("2. OVERALL KPI SUMMARY")
    lines.append("----------------------")

    lines.append(
        f"Total Revenue: {format_currency(overall_kpis.get('total_revenue'))}"
    )

    lines.append(
        f"Total Orders: {overall_kpis.get('total_orders', 0):,}"
    )

    lines.append(
        f"Total Quantity Sold: {format_number(overall_kpis.get('total_quantity'), decimals=0)}"
    )

    lines.append(
        f"Average Order Value: {format_currency(overall_kpis.get('average_order_value'))}"
    )

    if overall_kpis.get("has_profit"):
        lines.append(
            f"Gross Income / Profit: {format_currency(overall_kpis.get('gross_income'))}"
        )
        lines.append(
            f"Profit Margin: {format_number(overall_kpis.get('profit_margin'))}%"
        )
    else:
        lines.append("Gross Income / Profit: Not available in uploaded dataset")
        lines.append("Profit Margin: Not available in uploaded dataset")

    if overall_kpis.get("has_rating"):
        lines.append(
            f"Average Rating: {format_number(overall_kpis.get('average_rating'))}"
        )
    else:
        lines.append("Average Rating: Not available in uploaded dataset")

    return "\n".join(lines)


def build_top_performer_section(top_performers):
    """
    Build top performer section for AI context.
    """
    lines = []

    lines.append("3. TOP PERFORMERS")
    lines.append("-----------------")

    if top_performers.get("has_city"):
        lines.append(
            f"Top City / Region: {format_plain(top_performers.get('top_city'))} "
            f"with revenue of {format_currency(top_performers.get('top_city_revenue'))}"
        )
    else:
        lines.append("Top City / Region: Not available in uploaded dataset")

    if top_performers.get("has_branch"):
        lines.append(
            f"Top Branch / Store: {format_plain(top_performers.get('top_branch'))} "
            f"with revenue of {format_currency(top_performers.get('top_branch_revenue'))}"
        )
    else:
        lines.append("Top Branch / Store: Not available in uploaded dataset")

    if top_performers.get("has_product"):
        lines.append(
            f"Top Product / Category: {format_plain(top_performers.get('top_product_line'))} "
            f"with revenue of {format_currency(top_performers.get('top_product_line_revenue'))}"
        )

        lines.append(
            f"Lowest Revenue Product / Category: {format_plain(top_performers.get('lowest_product_line'))} "
            f"with revenue of {format_currency(top_performers.get('lowest_product_line_revenue'))}"
        )
    else:
        lines.append("Product / Category performance: Not available in uploaded dataset")

    if top_performers.get("has_payment"):
        lines.append(
            f"Top Payment Method: {format_plain(top_performers.get('top_payment_method'))} "
            f"with revenue of {format_currency(top_performers.get('top_payment_revenue'))}"
        )
    else:
        lines.append("Payment Method performance: Not available in uploaded dataset")

    if top_performers.get("has_customer_type"):
        lines.append(
            f"Top Customer Type / Segment: {format_plain(top_performers.get('top_customer_type'))} "
            f"with revenue of {format_currency(top_performers.get('top_customer_type_revenue'))}"
        )
    else:
        lines.append("Customer Type / Segment performance: Not available in uploaded dataset")

    if top_performers.get("has_rating") and top_performers.get("has_product"):
        lines.append(
            f"Best Rated Product / Category: {format_plain(top_performers.get('best_rated_product_line'))} "
            f"with average rating of {format_number(top_performers.get('best_rating'))}"
        )

        lines.append(
            f"Worst Rated Product / Category: {format_plain(top_performers.get('worst_rated_product_line'))} "
            f"with average rating of {format_number(top_performers.get('worst_rating'))}"
        )
    else:
        lines.append("Product rating performance: Not available in uploaded dataset")

    return "\n".join(lines)


def summarize_segment_table(df, label_column, value_column="revenue", top_n=5):
    """
    Convert a segment dataframe into concise text lines for AI context.
    """
    if df is None or df.empty:
        return ["Not available"]

    if label_column not in df.columns or value_column not in df.columns:
        return ["Not available"]

    top_rows = df.head(top_n)

    lines = []

    for _, row in top_rows.iterrows():
        label = row[label_column]
        value = row[value_column]

        extra_parts = []

        if "quantity_sold" in df.columns:
            extra_parts.append(
                f"quantity sold: {format_number(row.get('quantity_sold'), decimals=0)}"
            )

        if "order_count" in df.columns:
            extra_parts.append(
                f"orders: {format_number(row.get('order_count'), decimals=0)}"
            )

        if "average_rating" in df.columns and not pd.isna(row.get("average_rating")):
            extra_parts.append(
                f"average rating: {format_number(row.get('average_rating'))}"
            )

        extra_text = ""
        if extra_parts:
            extra_text = " | " + " | ".join(extra_parts)

        lines.append(
            f"- {label}: {format_currency(value)}{extra_text}"
        )

    return lines


def build_segment_summary_section(segment_summaries):
    """
    Build segment performance section for AI context.
    """
    lines = []

    lines.append("4. SEGMENT PERFORMANCE SUMMARY")
    lines.append("------------------------------")

    if segment_summaries.get("revenue_by_product_line") is not None:
        lines.append("Revenue by Product / Category:")
        lines.extend(
            summarize_segment_table(
                segment_summaries["revenue_by_product_line"],
                label_column="product_line"
            )
        )
    else:
        lines.append("Revenue by Product / Category: Not available in uploaded dataset")

    lines.append("")

    if segment_summaries.get("revenue_by_city") is not None:
        lines.append("Revenue by City / Region:")
        lines.extend(
            summarize_segment_table(
                segment_summaries["revenue_by_city"],
                label_column="city"
            )
        )
    else:
        lines.append("Revenue by City / Region: Not available in uploaded dataset")

    lines.append("")

    if segment_summaries.get("revenue_by_branch") is not None:
        lines.append("Revenue by Branch / Store:")
        lines.extend(
            summarize_segment_table(
                segment_summaries["revenue_by_branch"],
                label_column="branch"
            )
        )
    else:
        lines.append("Revenue by Branch / Store: Not available in uploaded dataset")

    lines.append("")

    if segment_summaries.get("revenue_by_customer_type") is not None:
        lines.append("Revenue by Customer Type / Segment:")
        lines.extend(
            summarize_segment_table(
                segment_summaries["revenue_by_customer_type"],
                label_column="customer_type"
            )
        )
    else:
        lines.append("Revenue by Customer Type / Segment: Not available in uploaded dataset")

    lines.append("")

    if segment_summaries.get("revenue_by_payment") is not None:
        lines.append("Revenue by Payment Method:")
        lines.extend(
            summarize_segment_table(
                segment_summaries["revenue_by_payment"],
                label_column="payment"
            )
        )
    else:
        lines.append("Revenue by Payment Method: Not available in uploaded dataset")

    lines.append("")

    if segment_summaries.get("revenue_by_date") is not None:
        date_df = segment_summaries["revenue_by_date"]

        if not date_df.empty and "date" in date_df.columns and "revenue" in date_df.columns:
            first_date = date_df["date"].min()
            last_date = date_df["date"].max()
            highest_day = date_df.sort_values(by="revenue", ascending=False).iloc[0]
            lowest_day = date_df.sort_values(by="revenue", ascending=True).iloc[0]

            lines.append("Revenue Trend Summary:")
            lines.append(f"- Date range: {first_date.date()} to {last_date.date()}")
            lines.append(
                f"- Highest revenue date: {highest_day['date'].date()} "
                f"with {format_currency(highest_day['revenue'])}"
            )
            lines.append(
                f"- Lowest revenue date: {lowest_day['date'].date()} "
                f"with {format_currency(lowest_day['revenue'])}"
            )
        else:
            lines.append("Revenue Trend Summary: Not available")
    else:
        lines.append("Revenue Trend Summary: Not available")

    return "\n".join(lines)


def build_data_limitation_section(field_availability):
    """
    Build limitations section to prevent AI hallucination.
    """
    lines = []

    lines.append("5. DATA LIMITATIONS")
    lines.append("-------------------")

    limitations = []

    if not is_available(field_availability, "profit"):
        limitations.append(
            "- Profit / gross income data is not available, so do not make profit margin or profitability conclusions."
        )

    if not is_available(field_availability, "rating"):
        limitations.append(
            "- Rating data is not available, so do not discuss customer satisfaction scores or product rating performance."
        )

    if not is_available(field_availability, "payment"):
        limitations.append(
            "- Payment method data is not available, so do not discuss payment method performance."
        )

    if not is_available(field_availability, "customer_type"):
        limitations.append(
            "- Customer type / segment data is not available, so do not compare customer segments."
        )

    if not is_available(field_availability, "branch"):
        limitations.append(
            "- Branch / store data is not available, so do not compare branch-level performance."
        )

    if not is_available(field_availability, "city"):
        limitations.append(
            "- City / region data is not available, so do not compare regional performance."
        )

    if limitations:
        lines.extend(limitations)
    else:
        lines.append("- No major optional field limitations detected.")

    return "\n".join(lines)


def build_ai_instruction_section():
    """
    Build strict AI instructions.
    """
    lines = []

    lines.append("6. AI INSTRUCTIONS")
    lines.append("------------------")
    lines.append("- Use only the metrics provided in this structured context.")
    lines.append("- Do not invent numbers, percentages, segments, or business facts.")
    lines.append("- Do not infer unavailable fields as zero or poor performance.")
    lines.append("- If a field is unavailable, clearly state that the uploaded dataset does not contain that information.")
    lines.append("- Prioritize practical, manager-friendly business interpretation.")
    lines.append("- Keep recommendations tied directly to the available metrics.")
    lines.append("- Avoid overclaiming causality from descriptive sales data.")

    return "\n".join(lines)


# =========================
# Main Context Builder
# =========================
def build_ai_context(
    overall_kpis,
    top_performers,
    segment_summaries,
    field_availability
):
    """
    Build a structured, grounded AI context for Gemini.

    This context combines:
    - field availability metadata
    - overall KPI summary
    - top performers
    - segment summaries
    - data limitations
    - strict AI instructions

    The goal is to reduce hallucination and prevent unsupported AI recommendations.
    """
    sections = []

    sections.append("RETAILMIND AI STRUCTURED BUSINESS CONTEXT")
    sections.append("========================================")
    sections.append("")
    sections.append(
        "This context is generated by the Python analytics pipeline after CSV upload, "
        "schema detection, schema mapping, data cleaning, filtering, and KPI calculation."
    )
    sections.append(
        "The AI model must rely only on the information below."
    )
    sections.append("")

    sections.append(build_data_availability_section(field_availability))
    sections.append("")
    sections.append(build_overall_kpi_section(overall_kpis))
    sections.append("")
    sections.append(build_top_performer_section(top_performers))
    sections.append("")
    sections.append(build_segment_summary_section(segment_summaries))
    sections.append("")
    sections.append(build_data_limitation_section(field_availability))
    sections.append("")
    sections.append(build_ai_instruction_section())

    return "\n".join(sections)