"""
Sales & Revenue Analysis Dashboard
-----------------------------------
Build a dashboard to analyze sales and revenue data.

Key features:
- Import data from Excel, CSV, or database
- Visualize KPIs like total sales, revenue trends, and top-performing products
- Use charts, filters, and slicers for interactive analysis

Run with:  streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sales & Revenue Analysis Dashboard",
    page_icon="📊",
    layout="wide",
)

REQUIRED_COLS = ["Date", "Product", "Category", "Region", "Quantity", "Revenue"]


# ---------------------------------------------------------------------------
# Data loading (Excel / CSV import)
# ---------------------------------------------------------------------------
@st.cache_data
def load_sample_data() -> pd.DataFrame:
    df = pd.read_csv("sample_sales_data.csv", parse_dates=["Date"])
    return df


def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Normalize column names (case/space tolerant matching against required cols)
    rename_map = {}
    for req in REQUIRED_COLS + ["Unit Price", "Order ID", "Customer ID"]:
        for col in df.columns:
            if col.strip().lower() == req.lower():
                rename_map[col] = req
    df = df.rename(columns=rename_map)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Uploaded file is missing required column(s): {', '.join(missing)}. "
            f"Expected columns roughly matching: {', '.join(REQUIRED_COLS)} "
            f"(Unit Price optional if Revenue is present)."
        )
    df["Date"] = pd.to_datetime(df["Date"])
    return df


st.sidebar.title("📊 Controls")

uploaded = st.sidebar.file_uploader("Import data (Excel or CSV)", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    try:
        raw_df = load_uploaded_file(uploaded)
        st.sidebar.caption(f"Using uploaded file: **{uploaded.name}**")
    except Exception as e:
        st.sidebar.error(str(e))
        st.stop()
else:
    raw_df = load_sample_data()
    st.sidebar.caption("Using bundled **sample dataset**. Import your own CSV or Excel file to replace it.")

# ---------------------------------------------------------------------------
# Filters / slicers
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

min_date, max_date = raw_df["Date"].min().date(), raw_df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

regions_all = sorted(raw_df["Region"].dropna().unique().tolist())
categories_all = sorted(raw_df["Category"].dropna().unique().tolist())
products_all = sorted(raw_df["Product"].dropna().unique().tolist())

sel_regions = st.sidebar.multiselect("Region", regions_all, default=regions_all)
sel_categories = st.sidebar.multiselect("Category", categories_all, default=categories_all)
sel_products = st.sidebar.multiselect("Product", products_all, default=products_all)

trend_granularity = st.sidebar.radio("Revenue trend view", ["Daily", "Weekly", "Monthly"], index=2)

# Apply filters
mask = (
    (raw_df["Date"].dt.date >= start_date)
    & (raw_df["Date"].dt.date <= end_date)
    & (raw_df["Region"].isin(sel_regions))
    & (raw_df["Category"].isin(sel_categories))
    & (raw_df["Product"].isin(sel_products))
)
df = raw_df.loc[mask].copy()

if df.empty:
    st.warning("No data matches the current filters. Try widening your date range or selections.")
    st.stop()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption(f"Showing {len(df):,} orders from {start_date} to {end_date}.")

# ---------------------------------------------------------------------------
# KPIs: total sales, revenue, top-performing products
# ---------------------------------------------------------------------------
total_revenue = df["Revenue"].sum()
total_orders = len(df)
total_units = df["Quantity"].sum()
avg_order_value = total_revenue / total_orders if total_orders else 0
top_product = df.groupby("Product")["Revenue"].sum().idxmax() if not df.empty else "N/A"

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Units Sold", f"{total_units:,}")
k4.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
k5.metric("Top Product", top_product)

st.markdown("---")

# ---------------------------------------------------------------------------
# Revenue trend chart
# ---------------------------------------------------------------------------
freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}
trend = (
    df.set_index("Date")
    .resample(freq_map[trend_granularity])["Revenue"]
    .sum()
    .reset_index()
)

st.subheader(f"Revenue Trend ({trend_granularity})")
fig_trend = px.line(trend, x="Date", y="Revenue", markers=True)
fig_trend.update_layout(margin=dict(t=10, b=10))
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# Breakdown charts
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    cat_rev = df.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
    fig_cat = px.pie(cat_rev, names="Category", values="Revenue", hole=0.45)
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.subheader("Revenue by Region")
    reg_rev = df.groupby("Region")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
    fig_reg = px.bar(reg_rev, x="Region", y="Revenue", color="Region", text_auto=".2s")
    fig_reg.update_layout(showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig_reg, use_container_width=True)

st.subheader("Top-Performing Products")
top10 = df.groupby("Product")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(10)
fig_top10 = px.bar(top10, x="Revenue", y="Product", orientation="h", text_auto=".2s")
fig_top10.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=10, b=10))
st.plotly_chart(fig_top10, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------
st.subheader("Filtered Data")
with st.expander("View filtered data table"):
    st.dataframe(df, use_container_width=True)

st.caption("Built with Streamlit, Pandas, and Plotly.")
