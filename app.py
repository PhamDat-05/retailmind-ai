from io import BytesIO

import streamlit as st
import pandas as pd

from src.data_loader import load_csv
from src.data_cleaning import clean_sales_data
from src.filters import apply_filters
from src.schema_mapper import (
    SCHEMA_FIELDS,
    get_mapping_options,
    validate_mapping,
    detect_duplicate_mappings,
    validate_selected_mapping_data_types,
    get_smart_mapping_suggestions,
    get_default_mapping_from_suggestions,
    create_detection_confidence_summary,
    get_low_confidence_required_fields,
    build_standard_schema,
    create_mapping_summary,
    create_field_availability,
    create_field_availability_summary,
    is_field_available
)
from src.kpi_calculator import (
    calculate_overall_kpis,
    calculate_top_performers,
    calculate_segment_summaries
)
from src.ai_context_builder import build_ai_context
from src.report_generator import (
    generate_markdown_report,
    get_report_file_name,
    get_chat_history_file_name
)
from src.chat_manager import (
    add_user_message,
    add_assistant_message,
    clear_chat_history,
    format_chat_history_for_prompt,
    format_chat_history_for_markdown
)
from src.visualizations import (
    plot_revenue_by_date,
    plot_revenue_by_product_line,
    plot_revenue_by_city,
    plot_revenue_by_branch,
    plot_revenue_by_customer_type,
    plot_revenue_by_payment,
    plot_rating_by_product_line
)
from src.ai_insight_generator import (
    generate_ai_insights,
    generate_ai_recommendations,
    generate_chatbot_response
)


# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="RetailMind AI",
    page_icon="🛒",
    layout="wide"
)


# =========================
# Session State Defaults
# =========================
if "ai_insights" not in st.session_state:
    st.session_state["ai_insights"] = None

if "ai_recommendations" not in st.session_state:
    st.session_state["ai_recommendations"] = None

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "last_uploaded_file_name" not in st.session_state:
    st.session_state["last_uploaded_file_name"] = None


# =========================
# Cached Data Loading
# =========================
@st.cache_data(show_spinner=False)
def load_uploaded_csv(file_bytes):
    """
    Load uploaded CSV file from bytes.
    """
    uploaded_buffer = BytesIO(file_bytes)
    df, error_message = load_csv(uploaded_buffer)

    return df, error_message


# =========================
# Helper UI Functions
# =========================
def show_unavailable_message(title, reason):
    """
    Display a consistent unavailable-data message.
    """
    st.info(f"**{title}** is not available for this dataset. {reason}")


def format_metric_value(value, prefix="", suffix="", decimals=2):
    """
    Format metric values safely.
    """
    if value is None or pd.isna(value):
        return "N/A"

    if isinstance(value, int):
        return f"{prefix}{value:,}{suffix}"

    return f"{prefix}{value:,.{decimals}f}{suffix}"


def safe_ai_markdown(text):
    """
    Safely render AI-generated Markdown in Streamlit.

    Streamlit may interpret dollar signs as LaTeX math delimiters.
    This function escapes dollar signs to prevent broken text rendering,
    such as words being joined together or shown in italic math style.
    """
    if text is None:
        return ""

    return str(text).replace("$", "\\$")


# =========================
# Header
# =========================
st.title("🛒 RetailMind AI")
st.subheader("AI-Powered Flexible Sales Insight Generator")

st.markdown("""
Upload a retail or sales CSV dataset, review smart schema detection,
map your columns to business fields, and generate dynamic KPI dashboards,
AI-powered insights, strategic recommendations, conversational business Q&A,
and downloadable AI business reports.
""")


# =========================
# File Upload
# =========================
uploaded_file = st.file_uploader(
    "Upload your sales CSV file",
    type=["csv"]
)


# =========================
# Main App Logic
# =========================
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()

    if st.session_state["last_uploaded_file_name"] != uploaded_file.name:
        st.session_state["ai_insights"] = None
        st.session_state["ai_recommendations"] = None
        st.session_state["chat_history"] = []
        st.session_state["last_uploaded_file_name"] = uploaded_file.name

    raw_df, error_message = load_uploaded_csv(file_bytes)

    if error_message:
        st.error(error_message)
        st.stop()

    if raw_df is None or raw_df.empty:
        st.error("The uploaded file is empty or could not be read.")
        st.stop()

    st.success("CSV file uploaded successfully.")

    st.caption(
        f"Original dataset: {raw_df.shape[0]:,} rows and "
        f"{raw_df.shape[1]:,} columns."
    )

    # =========================
    # Smart Schema Detection
    # =========================
    st.subheader("🧠 Smart Schema Detection")

    st.markdown("""
RetailMind AI automatically analyzes your uploaded CSV columns and suggests how they should be mapped to business fields.
Please review the suggestions before continuing.
""")

    smart_suggestions = get_smart_mapping_suggestions(raw_df)
    detection_summary = create_detection_confidence_summary(smart_suggestions)
    default_mapping = get_default_mapping_from_suggestions(
        smart_suggestions,
        minimum_score=35
    )

    with st.expander("View Auto Detection Summary", expanded=True):
        st.dataframe(detection_summary, use_container_width=True)

    low_confidence_required_df = get_low_confidence_required_fields(
        smart_suggestions
    )

    if not low_confidence_required_df.empty:
        st.warning(
            "Some required fields have low-confidence or missing suggestions. "
            "Please review and correct the mapping manually."
        )
        st.dataframe(low_confidence_required_df, use_container_width=True)
    else:
        st.info(
            "All required fields have acceptable auto-detection confidence. "
            "Please still review the mapping before continuing."
        )

    # =========================
    # Schema Mapping
    # =========================
    st.subheader("🧩 Schema Mapping")

    st.markdown("""
Map the columns from your uploaded CSV file to the business fields required by the app.
Required fields must be selected before the dashboard and AI features can run.
""")

    column_options = get_mapping_options(raw_df.columns)

    mapping = {}

    with st.expander("Configure Schema Mapping", expanded=True):
        st.markdown("### Required Fields")

        required_fields = {
            key: value
            for key, value in SCHEMA_FIELDS.items()
            if value["required"]
        }

        optional_fields = {
            key: value
            for key, value in SCHEMA_FIELDS.items()
            if not value["required"]
        }

        for field_key, field_info in required_fields.items():
            default_column = default_mapping.get(field_key)

            if default_column in column_options:
                default_index = column_options.index(default_column)
            else:
                default_index = 0

            suggestion = smart_suggestions[field_key]

            help_text = (
                f"Suggested column: {suggestion['suggested_column'] or 'Not detected'} | "
                f"Confidence: {suggestion['confidence']} | "
                f"Score: {suggestion['score']}"
            )

            mapping[field_key] = st.selectbox(
                label=f"{field_info['label']} *",
                options=column_options,
                index=default_index,
                help=help_text,
                key=f"mapping_required_{field_key}"
            )

        st.markdown("### Optional Fields")

        optional_col1, optional_col2 = st.columns(2)

        optional_items = list(optional_fields.items())

        for index, (field_key, field_info) in enumerate(optional_items):
            default_column = default_mapping.get(field_key)

            if default_column in column_options:
                default_index = column_options.index(default_column)
            else:
                default_index = 0

            suggestion = smart_suggestions[field_key]

            help_text = (
                f"Suggested column: {suggestion['suggested_column'] or 'Not detected'} | "
                f"Confidence: {suggestion['confidence']} | "
                f"Score: {suggestion['score']}"
            )

            target_column = optional_col1 if index % 2 == 0 else optional_col2

            with target_column:
                mapping[field_key] = st.selectbox(
                    label=field_info["label"],
                    options=column_options,
                    index=default_index,
                    help=help_text,
                    key=f"mapping_optional_{field_key}"
                )

    # =========================
    # Mapping Validation
    # =========================
    is_mapping_valid, missing_required_fields = validate_mapping(mapping)

    duplicate_mappings = detect_duplicate_mappings(mapping)
    data_type_warnings = validate_selected_mapping_data_types(raw_df, mapping)

    if duplicate_mappings:
        st.warning(
            "Some CSV columns are mapped to multiple business fields. "
            "This may be valid in some cases, but please review carefully."
        )

        duplicate_rows = []

        for column, fields in duplicate_mappings.items():
            duplicate_rows.append(
                {
                    "CSV Column": column,
                    "Mapped Business Fields": ", ".join(fields)
                }
            )

        st.dataframe(pd.DataFrame(duplicate_rows), use_container_width=True)

    if data_type_warnings:
        st.warning(
            "Some selected mappings may not match the expected data type. "
            "Please review them before continuing."
        )

        for warning in data_type_warnings:
            st.write(f"- {warning}")

    if not is_mapping_valid:
        st.error("Please map all required fields before continuing.")
        st.write("Missing required fields:")
        st.write(missing_required_fields)

        with st.expander("Preview Uploaded Data"):
            st.dataframe(raw_df.head(20), use_container_width=True)

        st.stop()

    mapping_summary = create_mapping_summary(mapping)
    field_availability = create_field_availability(mapping)
    field_availability_summary = create_field_availability_summary(field_availability)

    with st.expander("View Final Mapping Summary"):
        st.dataframe(mapping_summary, use_container_width=True)

    with st.expander("View Field Availability Summary"):
        st.dataframe(field_availability_summary, use_container_width=True)

    # Build standardized dataset from mapped columns
    df_standardized = build_standard_schema(raw_df, mapping)

    if df_standardized.empty:
        st.error(
            "No valid rows remained after applying schema mapping. "
            "Please check your Date, Revenue, and Quantity mappings."
        )
        st.stop()

    # Clean and enrich standardized data
    df_cleaned = clean_sales_data(df_standardized)

    # =========================
    # Sidebar Filters
    # =========================
    st.sidebar.title("🛒 RetailMind AI")
    st.sidebar.markdown("Use filters to explore sales performance.")

    with st.sidebar.expander("Filters", expanded=True):
        if is_field_available(field_availability, "city"):
            selected_cities = st.multiselect(
                "City / Region",
                options=sorted(df_cleaned["city"].unique()),
                default=sorted(df_cleaned["city"].unique())
            )
        else:
            selected_cities = sorted(df_cleaned["city"].unique())

        if is_field_available(field_availability, "branch"):
            selected_branches = st.multiselect(
                "Branch / Store",
                options=sorted(df_cleaned["branch"].unique()),
                default=sorted(df_cleaned["branch"].unique())
            )
        else:
            selected_branches = sorted(df_cleaned["branch"].unique())

        selected_product_lines = st.multiselect(
            "Product / Category",
            options=sorted(df_cleaned["product_line"].unique()),
            default=sorted(df_cleaned["product_line"].unique())
        )

        if is_field_available(field_availability, "customer_type"):
            selected_customer_types = st.multiselect(
                "Customer Type",
                options=sorted(df_cleaned["customer_type"].unique()),
                default=sorted(df_cleaned["customer_type"].unique())
            )
        else:
            selected_customer_types = sorted(df_cleaned["customer_type"].unique())

        if is_field_available(field_availability, "payment"):
            selected_payment_methods = st.multiselect(
                "Payment Method",
                options=sorted(df_cleaned["payment"].unique()),
                default=sorted(df_cleaned["payment"].unique())
            )
        else:
            selected_payment_methods = sorted(df_cleaned["payment"].unique())

        min_date = df_cleaned["date"].min().date()
        max_date = df_cleaned["date"].max().date()

        selected_date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    df_filtered = apply_filters(
        df_cleaned,
        selected_cities,
        selected_branches,
        selected_product_lines,
        selected_customer_types,
        selected_payment_methods,
        selected_date_range
    )

    if df_filtered.empty:
        st.warning(
            "No data available for the selected filters. "
            "Please adjust your filter settings."
        )
        st.stop()

    overall_kpis = calculate_overall_kpis(df_filtered, field_availability)
    top_performers = calculate_top_performers(df_filtered, field_availability)
    segment_summaries = calculate_segment_summaries(df_filtered, field_availability)

    ai_context_text = build_ai_context(
        overall_kpis=overall_kpis,
        top_performers=top_performers,
        segment_summaries=segment_summaries,
        field_availability=field_availability
    )

    st.success("Dataset detected, mapped, cleaned, and validated successfully.")

    st.caption(
        f"Showing {df_filtered.shape[0]:,} rows after filtering "
        f"from {df_cleaned.shape[0]:,} standardized rows."
    )

    (
        dashboard_tab,
        ai_insights_tab,
        ai_recommendations_tab,
        ask_ai_tab,
        ai_report_tab,
        data_quality_tab,
        schema_tab,
        ai_context_tab,
        data_preview_tab
    ) = st.tabs(
        [
            "📊 Dashboard",
            "✨ AI Insights",
            "🎯 AI Recommendations",
            "💬 Ask AI",
            "📄 AI Report",
            "🧪 Data Quality",
            "🧩 Schema Mapping",
            "🤖 AI Context",
            "🔍 Data Preview"
        ]
    )

    # =========================
    # Dashboard Tab
    # =========================
    with dashboard_tab:
        st.subheader("Executive KPI Overview")

        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

        with kpi_col1:
            st.metric(
                "Total Revenue",
                format_metric_value(overall_kpis["total_revenue"], prefix="$")
            )

        with kpi_col2:
            if overall_kpis["has_profit"]:
                st.metric(
                    "Gross Income / Profit",
                    format_metric_value(overall_kpis["gross_income"], prefix="$")
                )
            else:
                st.metric("Gross Income / Profit", "N/A")

        with kpi_col3:
            st.metric("Total Orders", f"{overall_kpis['total_orders']:,}")

        kpi_col4, kpi_col5, kpi_col6 = st.columns(3)

        with kpi_col4:
            st.metric("Quantity Sold", f"{overall_kpis['total_quantity']:,.0f}")

        with kpi_col5:
            st.metric(
                "Average Order Value",
                format_metric_value(overall_kpis["average_order_value"], prefix="$")
            )

        with kpi_col6:
            if overall_kpis["has_rating"]:
                st.metric(
                    "Average Rating",
                    format_metric_value(overall_kpis["average_rating"])
                )
            else:
                st.metric("Average Rating", "N/A")

        if not overall_kpis["has_profit"] or not overall_kpis["has_rating"]:
            st.info(
                "Some KPIs are shown as N/A because the uploaded dataset does not contain "
                "the required mapped fields for those metrics."
            )

        st.divider()

        st.subheader("Top Business Highlights")

        highlight_col1, highlight_col2, highlight_col3 = st.columns(3)

        with highlight_col1:
            if top_performers["has_city"]:
                st.info(
                    f"Top City / Region: **{top_performers['top_city']}** "
                    f"(${top_performers['top_city_revenue']:,.2f})"
                )
            else:
                st.info("Top City / Region: N/A")

        with highlight_col2:
            if top_performers["has_product"]:
                st.info(
                    f"Top Product / Category: **{top_performers['top_product_line']}** "
                    f"(${top_performers['top_product_line_revenue']:,.2f})"
                )
            else:
                st.info("Top Product / Category: N/A")

        with highlight_col3:
            if top_performers["has_payment"]:
                st.info(
                    f"Top Payment Method: **{top_performers['top_payment_method']}** "
                    f"(${top_performers['top_payment_revenue']:,.2f})"
                )
            else:
                st.info("Top Payment Method: N/A")

        st.divider()

        st.subheader("Interactive Sales Dashboard")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            if segment_summaries["revenue_by_product_line"] is not None:
                st.plotly_chart(
                    plot_revenue_by_product_line(segment_summaries["revenue_by_product_line"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Revenue by Product / Category",
                    "Product or category data was not mapped."
                )

        with chart_col2:
            if segment_summaries["revenue_by_city"] is not None:
                st.plotly_chart(
                    plot_revenue_by_city(segment_summaries["revenue_by_city"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Revenue by City / Region",
                    "City or region data was not mapped."
                )

        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            if segment_summaries["revenue_by_branch"] is not None:
                st.plotly_chart(
                    plot_revenue_by_branch(segment_summaries["revenue_by_branch"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Revenue by Branch / Store",
                    "Branch or store data was not mapped."
                )

        with chart_col4:
            if segment_summaries["revenue_by_customer_type"] is not None:
                st.plotly_chart(
                    plot_revenue_by_customer_type(segment_summaries["revenue_by_customer_type"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Revenue by Customer Type",
                    "Customer type or segment data was not mapped."
                )

        chart_col5, chart_col6 = st.columns(2)

        with chart_col5:
            if segment_summaries["revenue_by_payment"] is not None:
                st.plotly_chart(
                    plot_revenue_by_payment(segment_summaries["revenue_by_payment"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Revenue by Payment Method",
                    "Payment method data was not mapped."
                )

        with chart_col6:
            if (
                segment_summaries["revenue_by_product_line"] is not None
                and overall_kpis["has_rating"]
                and "average_rating" in segment_summaries["revenue_by_product_line"].columns
            ):
                st.plotly_chart(
                    plot_rating_by_product_line(segment_summaries["revenue_by_product_line"]),
                    use_container_width=True
                )
            else:
                show_unavailable_message(
                    "Rating by Product / Category",
                    "Rating data was not mapped."
                )

        st.plotly_chart(
            plot_revenue_by_date(segment_summaries["revenue_by_date"]),
            use_container_width=True
        )

    # =========================
    # AI Insights Tab
    # =========================
    with ai_insights_tab:
        st.subheader("AI-Generated Business Insights")

        with st.expander("View Structured AI Context"):
            st.text(ai_context_text)

        if st.button("Generate AI Insights", type="primary"):
            with st.spinner("Generating AI-powered business insights..."):
                ai_insights, ai_error = generate_ai_insights(ai_context_text)

            if ai_error:
                st.error(ai_error)
            else:
                st.session_state["ai_insights"] = ai_insights
                st.markdown(safe_ai_markdown(ai_insights))

        elif st.session_state["ai_insights"]:
            st.markdown(safe_ai_markdown(st.session_state["ai_insights"]))

    # =========================
    # AI Recommendations Tab
    # =========================
    with ai_recommendations_tab:
        st.subheader("AI-Generated Strategic Recommendations")

        with st.expander("View Structured AI Context"):
            st.text(ai_context_text)

        if st.button("Generate AI Recommendations", type="primary"):
            with st.spinner("Generating AI-powered strategic recommendations..."):
                ai_recommendations, recommendation_error = generate_ai_recommendations(
                    ai_context_text
                )

            if recommendation_error:
                st.error(recommendation_error)
            else:
                st.session_state["ai_recommendations"] = ai_recommendations
                st.markdown(safe_ai_markdown(ai_recommendations))

        elif st.session_state["ai_recommendations"]:
            st.markdown(safe_ai_markdown(st.session_state["ai_recommendations"]))

    # =========================
    # Ask AI Tab with Chat History
    # =========================
    with ask_ai_tab:
        st.subheader("AI Business Chatbot")

        st.markdown("""
Ask follow-up business questions about the filtered sales data.  
The chatbot uses the structured AI context and recent chat history to support conversational Q&A.
""")

        with st.expander("Suggested Questions", expanded=True):
            st.markdown("""
- Which product or category generates the highest revenue?
- Which city or region performs best?
- Why is this product category performing well?
- What should management focus on first?
- Which product category needs attention?
- How can we improve customer satisfaction?
- What are the main business risks?
- Which payment method contributes the most revenue?
""")

        with st.expander("View Structured AI Context"):
            st.text(ai_context_text)

        st.divider()

        st.subheader("Conversation")

        if not st.session_state["chat_history"]:
            st.info("No chat messages yet. Ask a question to start the conversation.")

        for message in st.session_state["chat_history"]:
            role = message.get("role", "assistant")
            content = message.get("content", "")
            timestamp = message.get("timestamp", "")

            with st.chat_message(role):
                st.markdown(safe_ai_markdown(content))
                if timestamp:
                    st.caption(timestamp)

        user_question = st.chat_input(
            "Ask a business question about this dataset..."
        )

        if user_question:
            st.session_state["chat_history"] = add_user_message(
                st.session_state["chat_history"],
                user_question
            )

            chat_history_text = format_chat_history_for_prompt(
                st.session_state["chat_history"],
                max_messages=8
            )

            with st.spinner("Generating AI response..."):
                chatbot_response, chatbot_error = generate_chatbot_response(
                    user_question=user_question,
                    kpi_summary_text=ai_context_text,
                    chat_history_text=chat_history_text
                )

            if chatbot_error:
                st.error(chatbot_error)
            else:
                st.session_state["chat_history"] = add_assistant_message(
                    st.session_state["chat_history"],
                    chatbot_response
                )
                st.rerun()

        st.divider()

        chat_action_col1, chat_action_col2 = st.columns(2)

        with chat_action_col1:
            if st.button("Clear Chat History"):
                st.session_state["chat_history"] = clear_chat_history()
                st.rerun()

        with chat_action_col2:
            chat_history_markdown = format_chat_history_for_markdown(
                st.session_state["chat_history"]
            )

            st.download_button(
                label="Download Chat History",
                data=chat_history_markdown,
                file_name=get_chat_history_file_name(),
                mime="text/markdown"
            )

    # =========================
    # AI Report Tab
    # =========================
    with ai_report_tab:
        st.subheader("AI Business Report Export")

        st.markdown("""
Download a structured Markdown report containing dataset overview, field availability,
dynamic KPIs, top performers, segment summaries, AI insights, AI recommendations,
chat history, methodology notes, data limitations, and structured AI context.
""")

        st.divider()

        st.subheader("Report Readiness Check")

        report_status_col1, report_status_col2, report_status_col3 = st.columns(3)

        with report_status_col1:
            if st.session_state["ai_insights"]:
                st.success("AI Insights generated")
            else:
                st.warning("AI Insights not generated")

        with report_status_col2:
            if st.session_state["ai_recommendations"]:
                st.success("AI Recommendations generated")
            else:
                st.warning("AI Recommendations not generated")

        with report_status_col3:
            if st.session_state["chat_history"]:
                st.success(
                    f"Chat history available: {len(st.session_state['chat_history'])} messages"
                )
            else:
                st.warning("No chat history yet")

        st.divider()

        st.subheader("AI Business Chat History")

        if st.session_state["chat_history"]:
            st.markdown("""
The following conversation will be included in the downloaded AI business report.
""")

            for message in st.session_state["chat_history"]:
                role = message.get("role", "assistant")
                content = message.get("content", "")
                timestamp = message.get("timestamp", "")

                with st.chat_message(role):
                    st.markdown(safe_ai_markdown(content))
                    if timestamp:
                        st.caption(timestamp)
        else:
            st.info(
                "No chat history is available yet. "
                "Go to the Ask AI tab and ask at least one question if you want chat history to appear in the report."
            )

        st.divider()

        if not st.session_state["ai_insights"]:
            st.warning(
                "AI Insights have not been generated yet. "
                "The report will still be downloadable, but the AI Insights section will show 'not generated yet'."
            )

        if not st.session_state["ai_recommendations"]:
            st.warning(
                "AI Recommendations have not been generated yet. "
                "The report will still be downloadable, but the AI Recommendations section will show 'not generated yet'."
            )

        report_markdown = generate_markdown_report(
            raw_df=raw_df,
            df_cleaned=df_cleaned,
            df_filtered=df_filtered,
            overall_kpis=overall_kpis,
            top_performers=top_performers,
            segment_summaries=segment_summaries,
            field_availability=field_availability,
            ai_insights=st.session_state["ai_insights"],
            ai_recommendations=st.session_state["ai_recommendations"],
            ai_context_text=ai_context_text,
            chat_history=st.session_state["chat_history"]
        )

        st.download_button(
            label="Download Markdown Report",
            data=report_markdown,
            file_name=get_report_file_name(),
            mime="text/markdown",
            type="primary"
        )

        with st.expander("Preview Full Report"):
            st.markdown(safe_ai_markdown(report_markdown))

    # =========================
    # Data Quality Tab
    # =========================
    with data_quality_tab:
        st.subheader("Data Quality Overview")

        original_missing_values = int(raw_df.isnull().sum().sum())
        original_duplicate_rows = int(raw_df.duplicated().sum())

        val_col1, val_col2, val_col3, val_col4 = st.columns(4)

        with val_col1:
            st.metric("Filtered Rows", df_filtered.shape[0])

        with val_col2:
            st.metric("Original Columns", raw_df.shape[1])

        with val_col3:
            st.metric("Original Missing Values", original_missing_values)

        with val_col4:
            st.metric("Original Duplicate Rows", original_duplicate_rows)

        st.divider()

        st.subheader("Standardized Dataset Information")

        clean_col1, clean_col2, clean_col3 = st.columns(3)

        with clean_col1:
            st.metric("Filtered Start Date", df_filtered["date"].min().strftime("%Y-%m-%d"))

        with clean_col2:
            st.metric("Filtered End Date", df_filtered["date"].max().strftime("%Y-%m-%d"))

        with clean_col3:
            st.metric("Current Columns", df_filtered.shape[1])

        st.divider()

        st.subheader("Field Availability")
        st.dataframe(field_availability_summary, use_container_width=True)

        st.divider()

        st.subheader("Current Standardized Columns")
        st.write(list(df_filtered.columns))

    # =========================
    # Schema Mapping Tab
    # =========================
    with schema_tab:
        st.subheader("Schema Detection and Mapping Summary")

        st.subheader("Auto Detection Summary")
        st.dataframe(detection_summary, use_container_width=True)

        st.subheader("Final Mapping Summary")
        st.dataframe(mapping_summary, use_container_width=True)

        st.subheader("Field Availability Summary")
        st.dataframe(field_availability_summary, use_container_width=True)

        st.divider()

        st.subheader("Original Dataset Preview")
        st.dataframe(raw_df.head(20), use_container_width=True)

        st.subheader("Standardized Dataset Preview")
        st.dataframe(df_cleaned.head(20), use_container_width=True)

    # =========================
    # AI Context Tab
    # =========================
    with ai_context_tab:
        st.subheader("Structured AI Context")

        st.text(ai_context_text)

        st.divider()

        st.subheader("Segment Summary Tables")

        if segment_summaries["revenue_by_product_line"] is not None:
            with st.expander("Revenue by Product / Category", expanded=True):
                st.dataframe(
                    segment_summaries["revenue_by_product_line"],
                    use_container_width=True
                )

        if segment_summaries["revenue_by_city"] is not None:
            with st.expander("Revenue by City / Region"):
                st.dataframe(
                    segment_summaries["revenue_by_city"],
                    use_container_width=True
                )

        if segment_summaries["revenue_by_branch"] is not None:
            with st.expander("Revenue by Branch / Store"):
                st.dataframe(
                    segment_summaries["revenue_by_branch"],
                    use_container_width=True
                )

        if segment_summaries["revenue_by_customer_type"] is not None:
            with st.expander("Revenue by Customer Type"):
                st.dataframe(
                    segment_summaries["revenue_by_customer_type"],
                    use_container_width=True
                )

        if segment_summaries["revenue_by_payment"] is not None:
            with st.expander("Revenue by Payment Method"):
                st.dataframe(
                    segment_summaries["revenue_by_payment"],
                    use_container_width=True
                )

        with st.expander("Revenue by Date"):
            st.dataframe(
                segment_summaries["revenue_by_date"],
                use_container_width=True
            )

    # =========================
    # Data Preview Tab
    # =========================
    with data_preview_tab:
        st.subheader("Filtered Standardized Dataset Preview")

        st.dataframe(df_filtered.head(20), use_container_width=True)

        with st.expander("View Full Filtered Dataset"):
            st.dataframe(df_filtered, use_container_width=True)


else:
    st.info("Please upload a CSV file to begin.")