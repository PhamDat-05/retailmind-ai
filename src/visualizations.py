import plotly.express as px


def plot_revenue_by_date(revenue_by_date):
    """
    Create a line chart showing revenue trend over time.
    """
    fig = px.line(
        revenue_by_date,
        x="date",
        y="revenue",
        markers=True,
        title="Revenue Trend by Date"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue",
        hovermode="x unified"
    )

    return fig


def plot_revenue_by_product_line(revenue_by_product_line):
    """
    Create a bar chart showing revenue by product line.
    """
    fig = px.bar(
        revenue_by_product_line,
        x="product_line",
        y="revenue",
        title="Revenue by Product Line",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Product Line",
        yaxis_title="Revenue"
    )

    return fig


def plot_revenue_by_city(revenue_by_city):
    """
    Create a bar chart showing revenue by city.
    """
    fig = px.bar(
        revenue_by_city,
        x="city",
        y="revenue",
        title="Revenue by City",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Revenue"
    )

    return fig


def plot_revenue_by_branch(revenue_by_branch):
    """
    Create a bar chart showing revenue by branch.
    """
    fig = px.bar(
        revenue_by_branch,
        x="branch",
        y="revenue",
        title="Revenue by Branch",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Branch",
        yaxis_title="Revenue"
    )

    return fig


def plot_revenue_by_customer_type(revenue_by_customer_type):
    """
    Create a bar chart showing revenue by customer type.
    """
    fig = px.bar(
        revenue_by_customer_type,
        x="customer_type",
        y="revenue",
        title="Revenue by Customer Type",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Revenue"
    )

    return fig


def plot_revenue_by_payment(revenue_by_payment):
    """
    Create a pie chart showing revenue share by payment method.
    """
    fig = px.pie(
        revenue_by_payment,
        names="payment",
        values="revenue",
        title="Revenue Share by Payment Method"
    )

    return fig


def plot_rating_by_product_line(revenue_by_product_line):
    """
    Create a bar chart showing average rating by product line.
    """
    fig = px.bar(
        revenue_by_product_line.sort_values(
            by="average_rating",
            ascending=False
        ),
        x="product_line",
        y="average_rating",
        title="Average Rating by Product Line",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Product Line",
        yaxis_title="Average Rating"
    )

    return fig