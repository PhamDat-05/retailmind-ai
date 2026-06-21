import pandas as pd
import numpy as np


# =========================
# Schema Definitions
# =========================
SCHEMA_FIELDS = {
    "transaction_id": {
        "label": "Transaction ID / Order ID",
        "internal_column": "invoice_id",
        "required": False,
        "default": None,
        "expected_type": "id",
        "keywords": [
            "invoice id", "invoice", "order id", "order_id", "transaction id",
            "transaction_id", "id", "receipt id", "bill id", "sales id"
        ]
    },
    "date": {
        "label": "Date",
        "internal_column": "date",
        "required": True,
        "default": None,
        "expected_type": "date",
        "keywords": [
            "date", "order date", "transaction date", "purchase date",
            "invoice date", "created date", "sale date", "sales date"
        ]
    },
    "time": {
        "label": "Time",
        "internal_column": "time",
        "required": False,
        "default": "00:00",
        "expected_type": "time",
        "keywords": [
            "time", "order time", "transaction time", "purchase time",
            "sale time", "sales time"
        ]
    },
    "branch": {
        "label": "Branch / Store",
        "internal_column": "branch",
        "required": False,
        "default": "Unknown",
        "expected_type": "categorical",
        "keywords": [
            "branch", "store", "store id", "store name", "shop",
            "outlet", "warehouse", "location code"
        ]
    },
    "city": {
        "label": "City / Region",
        "internal_column": "city",
        "required": False,
        "default": "Unknown",
        "expected_type": "categorical",
        "keywords": [
            "city", "region", "area", "state", "province", "market",
            "location", "country", "district", "territory"
        ]
    },
    "customer_type": {
        "label": "Customer Type / Segment",
        "internal_column": "customer_type",
        "required": False,
        "default": "Unknown",
        "expected_type": "categorical",
        "keywords": [
            "customer type", "customer_type", "segment", "customer segment",
            "membership", "member type", "customer group", "client type"
        ]
    },
    "gender": {
        "label": "Gender",
        "internal_column": "gender",
        "required": False,
        "default": "Unknown",
        "expected_type": "categorical",
        "keywords": [
            "gender", "sex"
        ]
    },
    "product": {
        "label": "Product / Product Category",
        "internal_column": "product_line",
        "required": True,
        "default": None,
        "expected_type": "categorical",
        "keywords": [
            "product line", "product_line", "product", "category",
            "product category", "item", "item category", "department",
            "sku category", "goods", "product name"
        ]
    },
    "unit_price": {
        "label": "Unit Price",
        "internal_column": "unit_price",
        "required": False,
        "default": 0,
        "expected_type": "numeric",
        "keywords": [
            "unit price", "unit_price", "price", "selling price", "item price",
            "sales price", "unit cost"
        ]
    },
    "quantity": {
        "label": "Quantity",
        "internal_column": "quantity",
        "required": True,
        "default": None,
        "expected_type": "numeric",
        "keywords": [
            "quantity", "qty", "units", "units sold", "number of items",
            "items sold", "sales quantity", "order quantity"
        ]
    },
    "tax": {
        "label": "Tax",
        "internal_column": "tax_5percent",
        "required": False,
        "default": 0,
        "expected_type": "numeric",
        "keywords": [
            "tax", "tax 5%", "tax_5", "tax amount", "vat", "gst"
        ]
    },
    "revenue": {
        "label": "Revenue / Total Sales",
        "internal_column": "total",
        "required": True,
        "default": None,
        "expected_type": "numeric",
        "keywords": [
            "total", "sales", "revenue", "amount", "total amount",
            "sales amount", "net sales", "gross sales", "total sales",
            "order value", "transaction amount", "invoice amount"
        ]
    },
    "payment": {
        "label": "Payment Method",
        "internal_column": "payment",
        "required": False,
        "default": "Unknown",
        "expected_type": "categorical",
        "keywords": [
            "payment", "payment method", "payment_method", "method",
            "payment type", "pay method", "pay type"
        ]
    },
    "cogs": {
        "label": "Cost / COGS",
        "internal_column": "cogs",
        "required": False,
        "default": 0,
        "expected_type": "numeric",
        "keywords": [
            "cogs", "cost", "cost of goods", "cost of goods sold",
            "total cost", "purchase cost"
        ]
    },
    "gross_margin_percentage": {
        "label": "Gross Margin Percentage",
        "internal_column": "gross_margin_percentage",
        "required": False,
        "default": 0,
        "expected_type": "numeric",
        "keywords": [
            "gross margin percentage", "gross margin %", "margin percentage",
            "margin %", "gross_margin_percentage", "profit margin"
        ]
    },
    "profit": {
        "label": "Profit / Gross Income",
        "internal_column": "gross_income",
        "required": False,
        "default": 0,
        "expected_type": "numeric",
        "keywords": [
            "gross income", "gross_income", "profit", "gross profit",
            "margin", "income", "net profit", "profit amount"
        ]
    },
    "rating": {
        "label": "Rating / Satisfaction Score",
        "internal_column": "rating",
        "required": False,
        "default": np.nan,
        "expected_type": "numeric",
        "keywords": [
            "rating", "customer rating", "satisfaction", "score",
            "review score", "satisfaction score", "customer score"
        ]
    }
}


REQUIRED_FIELDS = [
    field_key
    for field_key, field_info in SCHEMA_FIELDS.items()
    if field_info["required"]
]


# =========================
# Text Normalization
# =========================
def normalize_text(text):
    """
    Normalize text for column-name matching.
    """
    return (
        str(text)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
        .replace("/", " ")
        .replace(".", " ")
    )


# =========================
# Data Type Profiling
# =========================
def get_column_profile(df, column_name):
    """
    Profile a column to support schema auto-detection.
    """
    series = df[column_name]
    non_null_series = series.dropna()

    if len(non_null_series) == 0:
        return {
            "numeric_ratio": 0,
            "date_ratio": 0,
            "unique_ratio": 0,
            "sample_values": []
        }

    numeric_series = pd.to_numeric(non_null_series, errors="coerce")
    numeric_ratio = numeric_series.notna().mean()

    date_series = pd.to_datetime(non_null_series, errors="coerce")
    date_ratio = date_series.notna().mean()

    unique_ratio = non_null_series.nunique() / len(non_null_series)

    sample_values = (
        non_null_series
        .astype(str)
        .head(5)
        .tolist()
    )

    return {
        "numeric_ratio": float(numeric_ratio),
        "date_ratio": float(date_ratio),
        "unique_ratio": float(unique_ratio),
        "sample_values": sample_values
    }


def calculate_type_score(profile, expected_type):
    """
    Score how well a column's values match the expected business field type.
    """
    if expected_type == "numeric":
        if profile["numeric_ratio"] >= 0.95:
            return 30
        if profile["numeric_ratio"] >= 0.80:
            return 20
        if profile["numeric_ratio"] >= 0.50:
            return 10
        return -20

    if expected_type == "date":
        if profile["date_ratio"] >= 0.95:
            return 30
        if profile["date_ratio"] >= 0.80:
            return 20
        if profile["date_ratio"] >= 0.50:
            return 10
        return -25

    if expected_type == "categorical":
        if profile["unique_ratio"] <= 0.30:
            return 20
        if profile["unique_ratio"] <= 0.60:
            return 10
        return 0

    if expected_type == "id":
        if profile["unique_ratio"] >= 0.80:
            return 20
        return 5

    if expected_type == "time":
        return 5

    return 0


# =========================
# Smart Detection Logic
# =========================
def calculate_column_match_score(df, column_name, field_key):
    """
    Calculate a confidence score for mapping one CSV column to one business field.
    """
    field_info = SCHEMA_FIELDS[field_key]
    normalized_column = normalize_text(column_name)
    keywords = field_info["keywords"]
    expected_type = field_info["expected_type"]

    score = 0
    match_reason = []

    # 1. Exact keyword match
    for keyword in keywords:
        normalized_keyword = normalize_text(keyword)

        if normalized_column == normalized_keyword:
            score += 70
            match_reason.append("Exact name match")
            break

    # 2. Strong partial keyword match
    if score < 70:
        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            if normalized_keyword in normalized_column:
                score += 50
                match_reason.append("Strong keyword match")
                break

    # 3. Reverse partial keyword match
    if score < 50:
        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)

            if normalized_column in normalized_keyword:
                score += 35
                match_reason.append("Partial keyword match")
                break

    # 4. Token overlap score
    column_tokens = set(normalized_column.split())

    for keyword in keywords:
        keyword_tokens = set(normalize_text(keyword).split())

        if not keyword_tokens:
            continue

        overlap = column_tokens.intersection(keyword_tokens)
        overlap_ratio = len(overlap) / len(keyword_tokens)

        if overlap_ratio >= 0.75:
            score += 25
            match_reason.append("Token overlap match")
            break
        elif overlap_ratio >= 0.50:
            score += 15
            match_reason.append("Weak token overlap match")
            break

    # 5. Data type score
    profile = get_column_profile(df, column_name)
    type_score = calculate_type_score(profile, expected_type)
    score += type_score

    if type_score > 0:
        match_reason.append(f"Matches expected {expected_type} type")
    elif type_score < 0:
        match_reason.append(f"Potential {expected_type} type mismatch")

    score = max(0, min(score, 100))

    if not match_reason:
        match_reason.append("No strong signal")

    return score, "; ".join(match_reason)


def get_confidence_level(score):
    """
    Convert numeric score into confidence level.
    """
    if score >= 80:
        return "High"
    if score >= 55:
        return "Medium"
    if score >= 35:
        return "Low"
    return "Not detected"


def detect_best_column_for_field(df, field_key, minimum_score=35):
    """
    Detect the best CSV column for a business field.
    """
    best_column = None
    best_score = 0
    best_reason = "No column detected"

    for column_name in df.columns:
        score, reason = calculate_column_match_score(df, column_name, field_key)

        if score > best_score:
            best_column = column_name
            best_score = score
            best_reason = reason

    if best_score < minimum_score:
        return None, best_score, "No reliable match detected"

    return best_column, best_score, best_reason


def get_smart_mapping_suggestions(df):
    """
    Generate smart schema mapping suggestions with confidence scores.
    """
    suggestions = {}

    for field_key, field_info in SCHEMA_FIELDS.items():
        suggested_column, score, reason = detect_best_column_for_field(df, field_key)

        suggestions[field_key] = {
            "business_field": field_info["label"],
            "internal_column": field_info["internal_column"],
            "suggested_column": suggested_column,
            "score": score,
            "confidence": get_confidence_level(score),
            "required": field_info["required"],
            "reason": reason
        }

    return suggestions


def create_detection_confidence_summary(suggestions):
    """
    Create a summary table for auto-detection results.
    """
    rows = []

    for field_key, suggestion in suggestions.items():
        rows.append(
            {
                "Business Field": suggestion["business_field"],
                "Suggested CSV Column": suggestion["suggested_column"] or "Not detected",
                "Confidence": suggestion["confidence"],
                "Score": suggestion["score"],
                "Required": suggestion["required"],
                "Reason": suggestion["reason"]
            }
        )

    return pd.DataFrame(rows)


def get_default_mapping_from_suggestions(suggestions, minimum_score=35):
    """
    Convert smart suggestions into default mapping values.
    Low-confidence suggestions are kept as Not selected.
    """
    mapping = {}

    for field_key, suggestion in suggestions.items():
        if suggestion["score"] >= minimum_score and suggestion["suggested_column"]:
            mapping[field_key] = suggestion["suggested_column"]
        else:
            mapping[field_key] = None

    return mapping


# =========================
# Mapping UI Helpers
# =========================
def get_mapping_options(columns):
    """
    Return selectbox options for mapping UI.
    """
    return ["-- Not selected --"] + list(columns)


def validate_mapping(mapping):
    """
    Validate whether all required business fields have been mapped.
    """
    missing_required_fields = []

    for field_key in REQUIRED_FIELDS:
        selected_column = mapping.get(field_key)

        if not selected_column or selected_column == "-- Not selected --":
            missing_required_fields.append(SCHEMA_FIELDS[field_key]["label"])

    is_valid = len(missing_required_fields) == 0

    return is_valid, missing_required_fields


def detect_duplicate_mappings(mapping):
    """
    Detect if the same CSV column is mapped to multiple business fields.
    """
    selected_columns = {}

    for field_key, selected_column in mapping.items():
        if not selected_column or selected_column == "-- Not selected --":
            continue

        selected_columns.setdefault(selected_column, []).append(
            SCHEMA_FIELDS[field_key]["label"]
        )

    duplicates = {
        column: fields
        for column, fields in selected_columns.items()
        if len(fields) > 1
    }

    return duplicates


def validate_selected_mapping_data_types(df, mapping):
    """
    Validate whether selected mapped columns roughly match expected data types.
    """
    warnings = []

    for field_key, selected_column in mapping.items():
        if not selected_column or selected_column == "-- Not selected --":
            continue

        field_info = SCHEMA_FIELDS[field_key]
        expected_type = field_info["expected_type"]
        profile = get_column_profile(df, selected_column)

        if expected_type == "numeric" and profile["numeric_ratio"] < 0.70:
            warnings.append(
                f"{field_info['label']} is mapped to '{selected_column}', "
                f"but this column does not look numeric."
            )

        if expected_type == "date" and profile["date_ratio"] < 0.70:
            warnings.append(
                f"{field_info['label']} is mapped to '{selected_column}', "
                f"but this column does not look like a valid date column."
            )

    return warnings


def get_low_confidence_required_fields(suggestions):
    """
    Return required fields with low or missing detection confidence.
    """
    low_confidence_fields = []

    for field_key in REQUIRED_FIELDS:
        suggestion = suggestions[field_key]

        if suggestion["confidence"] in ["Low", "Not detected"]:
            low_confidence_fields.append(
                {
                    "Business Field": suggestion["business_field"],
                    "Suggested CSV Column": suggestion["suggested_column"] or "Not detected",
                    "Confidence": suggestion["confidence"],
                    "Score": suggestion["score"]
                }
            )

    return pd.DataFrame(low_confidence_fields)


# =========================
# Field Availability Metadata
# =========================
def create_field_availability(mapping):
    """
    Create metadata showing which business fields are actually available
    from the uploaded dataset.

    A field is considered available only when the user maps it to a real CSV column.
    Default values created by the app are not considered real business data.
    """
    availability = {}

    for field_key, field_info in SCHEMA_FIELDS.items():
        selected_column = mapping.get(field_key)

        is_available = bool(
            selected_column and selected_column != "-- Not selected --"
        )

        availability[field_key] = {
            "available": is_available,
            "label": field_info["label"],
            "internal_column": field_info["internal_column"],
            "mapped_column": selected_column if is_available else None,
            "required": field_info["required"]
        }

    return availability


def is_field_available(field_availability, field_key):
    """
    Check if a field is available in the uploaded dataset.
    """
    if not field_availability:
        return True

    return field_availability.get(field_key, {}).get("available", False)


def create_field_availability_summary(field_availability):
    """
    Create a readable summary of available and unavailable business fields.
    """
    rows = []

    for field_key, info in field_availability.items():
        rows.append(
            {
                "Business Field": info["label"],
                "Internal Column": info["internal_column"],
                "Mapped CSV Column": info["mapped_column"] or "Not available",
                "Available": info["available"],
                "Required": info["required"]
            }
        )

    return pd.DataFrame(rows)


def get_available_unavailable_field_names(field_availability):
    """
    Return readable lists of available and unavailable business fields.
    """
    available_fields = []
    unavailable_fields = []

    for _, info in field_availability.items():
        if info["available"]:
            available_fields.append(info["label"])
        else:
            unavailable_fields.append(info["label"])

    return available_fields, unavailable_fields


# =========================
# Standard Schema Builder
# =========================
def safe_numeric(series, default_value=0):
    """
    Convert a pandas Series to numeric safely.
    """
    numeric_series = pd.to_numeric(series, errors="coerce")
    return numeric_series.fillna(default_value)


def safe_datetime(series):
    """
    Convert a pandas Series to datetime safely.
    """
    return pd.to_datetime(series, errors="coerce")


def build_standard_schema(df, mapping):
    """
    Convert a user-uploaded dataset into the internal schema expected by the app.
    """
    standardized_df = pd.DataFrame(index=df.index)

    for field_key, field_info in SCHEMA_FIELDS.items():
        internal_column = field_info["internal_column"]
        selected_column = mapping.get(field_key)
        default_value = field_info["default"]

        if selected_column and selected_column != "-- Not selected --":
            standardized_df[internal_column] = df[selected_column]
        else:
            standardized_df[internal_column] = default_value

    # Required / important type conversions
    standardized_df["date"] = safe_datetime(standardized_df["date"])
    standardized_df["quantity"] = safe_numeric(standardized_df["quantity"], default_value=0)
    standardized_df["total"] = safe_numeric(standardized_df["total"], default_value=0)
    standardized_df["gross_income"] = safe_numeric(standardized_df["gross_income"], default_value=0)
    standardized_df["rating"] = pd.to_numeric(standardized_df["rating"], errors="coerce")
    standardized_df["unit_price"] = safe_numeric(standardized_df["unit_price"], default_value=0)
    standardized_df["tax_5percent"] = safe_numeric(standardized_df["tax_5percent"], default_value=0)
    standardized_df["cogs"] = safe_numeric(standardized_df["cogs"], default_value=0)
    standardized_df["gross_margin_percentage"] = safe_numeric(
        standardized_df["gross_margin_percentage"],
        default_value=0
    )

    # Generate transaction ID if missing
    if standardized_df["invoice_id"].isnull().all() or (
        standardized_df["invoice_id"].astype(str) == "None"
    ).all():
        standardized_df["invoice_id"] = [
            f"TXN-{i + 1:06d}" for i in range(len(standardized_df))
        ]

    # Fill optional categorical fields
    categorical_columns = [
        "branch",
        "city",
        "customer_type",
        "gender",
        "product_line",
        "payment"
    ]

    for col in categorical_columns:
        standardized_df[col] = standardized_df[col].fillna("Unknown").astype(str)

    # Time fallback
    standardized_df["time"] = standardized_df["time"].fillna("00:00").astype(str)

    # If unit price is missing, estimate from revenue / quantity
    missing_unit_price_mask = standardized_df["unit_price"] == 0
    valid_quantity_mask = standardized_df["quantity"] > 0

    standardized_df.loc[
        missing_unit_price_mask & valid_quantity_mask,
        "unit_price"
    ] = (
        standardized_df.loc[missing_unit_price_mask & valid_quantity_mask, "total"]
        / standardized_df.loc[missing_unit_price_mask & valid_quantity_mask, "quantity"]
    )

    # If COGS is missing, estimate as revenue - gross income
    missing_cogs_mask = standardized_df["cogs"] == 0

    standardized_df.loc[
        missing_cogs_mask,
        "cogs"
    ] = (
        standardized_df.loc[missing_cogs_mask, "total"]
        - standardized_df.loc[missing_cogs_mask, "gross_income"]
    )

    # If gross margin percentage is missing, calculate it
    missing_margin_mask = standardized_df["gross_margin_percentage"] == 0
    valid_total_mask = standardized_df["total"] > 0

    standardized_df.loc[
        missing_margin_mask & valid_total_mask,
        "gross_margin_percentage"
    ] = (
        standardized_df.loc[missing_margin_mask & valid_total_mask, "gross_income"]
        / standardized_df.loc[missing_margin_mask & valid_total_mask, "total"]
        * 100
    )

    # Remove rows where required fields are unusable
    standardized_df = standardized_df.dropna(subset=["date"])
    standardized_df = standardized_df[standardized_df["total"] > 0]
    standardized_df = standardized_df[standardized_df["quantity"] >= 0]

    return standardized_df.reset_index(drop=True)


def create_mapping_summary(mapping):
    """
    Create a readable mapping summary for display.
    """
    summary_rows = []

    for field_key, field_info in SCHEMA_FIELDS.items():
        selected_column = mapping.get(field_key)

        if not selected_column or selected_column == "-- Not selected --":
            selected_column = "Not selected"

        summary_rows.append(
            {
                "Business Field": field_info["label"],
                "Internal Column": field_info["internal_column"],
                "Mapped CSV Column": selected_column,
                "Required": field_info["required"]
            }
        )

    return pd.DataFrame(summary_rows)