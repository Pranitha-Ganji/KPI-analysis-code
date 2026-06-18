import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Sales KPI Dashboard",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS (LIGHT THEME)
# --------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #F8FAFC;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.kpi-title {
    font-size: 16px;
    color: #64748B;
}

.kpi-value {
    font-size: 32px;
    font-weight: bold;
    color: #2563EB;
}

.section-title {
    color: #1E293B;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("📊 Sales KPI Dashboard")
st.markdown("### Business Performance Overview")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # --------------------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------------------
    st.sidebar.header("🔍 Filters")

    regions = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

    categories = st.sidebar.multiselect(
        "Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories))
    ]

    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = len(filtered_df)

    avg_order_value = (
        total_sales / total_orders
        if total_orders > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Total Sales</div>
            <div class='kpi-value'>${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Total Profit</div>
            <div class='kpi-value' style='color:#16A34A'>
            ${total_profit:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Total Orders</div>
            <div class='kpi-value' style='color:#F59E0B'>
            {total_orders}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>Average Order Value</div>
            <div class='kpi-value' style='color:#8B5CF6'>
            ${avg_order_value:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------
    # SALES TREND
    # --------------------------------------------------
    st.markdown(
        "<h3 class='section-title'>📈 Sales Trend</h3>",
        unsafe_allow_html=True
    )

    sales_trend = (
        filtered_df.groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        sales_trend,
        x="Order Date",
        y="Sales",
        markers=True,
        color_discrete_sequence=["#3B82F6"],
        template="plotly_white"
    )

    fig_trend.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # --------------------------------------------------
    # CHARTS
    # --------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:

        region_sales = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            color="Region",
            text_auto=".2s",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig_region.update_layout(
            title="Sales by Region",
            showlegend=False
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    with col2:

        category_sales = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig_pie.update_layout(
            title="Sales Contribution by Category"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    # --------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------
    st.markdown(
        "<h3 class='section-title'>🏆 Top Products</h3>",
        unsafe_allow_html=True
    )

    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        template="plotly_white",
        color="Sales",
        color_continuous_scale="Blues"
    )

    fig_products.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # --------------------------------------------------
    # DATA TABLE
    # --------------------------------------------------
    st.markdown(
        "<h3 class='section-title'>📋 Sales Data</h3>",
        unsafe_allow_html=True
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=350
    )

else:
    st.info("📂 Upload a CSV file to begin analysis.")