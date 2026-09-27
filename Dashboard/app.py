

from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px



st.set_page_config(
    page_title="E-Commerce Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f8fa;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* KPI card */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e8eaed;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-height: 130px;
    }

    .kpi-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 27px;
        font-weight: 700;
        color: #111827;
    }

    .kpi-subtitle {
        font-size: 12px;
        color: #6b7280;
        margin-top: 6px;
    }

    /* Observation box */
    .observation {
        background-color: #eef6ff;
        border-left: 5px solid #2563eb;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .observation-title {
        font-weight: 700;
        color: #1d4ed8;
        margin-bottom: 5px;
    }

    .observation-text {
        color: #374151;
        line-height: 1.6;
    }

    /* Business implication */
    .business-box {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .business-title {
        font-weight: 700;
        color: #15803d;
        margin-bottom: 5px;
    }

    .business-text {
        color: #374151;
        line-height: 1.6;
    }

    /* Section title */
    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #6b7280;
        margin-bottom: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        padding-top: 40px;
        padding-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# 3. HELPER FUNCTIONS
def format_rupiah(value):
    """Format angka menjadi Rupiah."""
    if pd.isna(value):
        return "Rp0"

    return f"Rp{value:,.0f}".replace(",", ".")

def format_number(value):
    """Format angka dengan separator ribuan."""
    if pd.isna(value):
        return "0"

    return f"{value:,.0f}".replace(",", ".")


def observation_box(title, text):
    """Menampilkan observation."""
    st.markdown(
        f"""
        <div class="observation">
            <div class="observation-title">{title}</div>
            <div class="observation-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def business_box(title, text):
    """Menampilkan business implication."""
    st.markdown(
        f"""
        <div class="business-box">
            <div class="business-title">{title}</div>
            <div class="business-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title, subtitle=None):
    """Menampilkan judul section."""
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )
    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


# ============================================================
# 4. LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Dataset" / "data_fetures.csv"


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)

    # Convert date
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    if "delivery_date" in df.columns:
        df["delivery_date"] = pd.to_datetime(
            df["delivery_date"],
            errors="coerce"
        )

    return df


try:
    df = load_data(DATA_PATH)

except FileNotFoundError:
    st.error(
        f"""
        Dataset tidak ditemukan.

        Pastikan struktur folder seperti berikut:

        ecommerce-data-analytics/
        ├── Dataset/
        │   └── data_fetures.csv
        └── app/
            └── app.py
        """
    )

    st.stop()


# 5. DATA PREPARATION

# Remove rows without order date
df = df.dropna(subset=["order_date"]).copy()

# Create year if not available
df["year"] = df["order_date"].dt.year

# Create month period
df["month_period"] = df["order_date"].dt.to_period("M")

# Create month label
df["month_label"] = df["order_date"].dt.strftime("%b %Y")


# 6. SIDEBAR FILTER


st.sidebar.title("Dashboard Filter")
st.sidebar.markdown(
    "Gunakan filter berikut untuk mengeksplorasi data."
)



# Year

years = sorted(df["year"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Tahun",
    options=years,
    default=years
)


# -----------------------------
# Date Range
# -----------------------------

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Handle date selection
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

else:

    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date)


# -----------------------------
# Category
# -----------------------------

categories = sorted(
    df["category"]
    .dropna()
    .unique()
)

selected_categories = st.sidebar.multiselect(
    "Kategori",
    options=categories,
    default=categories
)


# -----------------------------
# Gender
# -----------------------------

genders = sorted(
    df["customer_gender"]
    .dropna()
    .unique()
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    options=genders,
    default=genders
)



# Province
provinces = sorted(
    df["customer_province"]
    .dropna()
    .unique()
)

selected_provinces = st.sidebar.multiselect(
    "Provinsi",
    options=provinces,
    default=provinces
)

# Payment
payments = sorted(
    df["payment_method"]
    .dropna()
    .unique()
)

selected_payments = st.sidebar.multiselect(
    "Metode Pembayaran",
    options=payments,
    default=payments
)


# 7. APPLY FILTER
filtered_df = df[
    (df["year"].isin(selected_years))
    &
    (df["order_date"] >= start_date)
    &
    (df["order_date"] <= end_date)
    &
    (df["category"].isin(selected_categories))
    &
    (df["customer_gender"].isin(selected_genders))
    &
    (df["customer_province"].isin(selected_provinces))
    &
    (df["payment_method"].isin(selected_payments))
].copy()



# 8. EMPTY DATA HANDLING
if filtered_df.empty:

    st.warning(
        """
        Tidak ada data yang sesuai dengan filter saat ini.

        Silakan ubah kombinasi filter pada sidebar.
        """
    )

    st.stop()


# 9. HEADER
st.title("E-Commerce Sales & Customer Analytics")
st.markdown(
    """
    Dashboard interaktif untuk menganalisis **penjualan, pelanggan,
    produk, transaksi, pembayaran, dan performa geografis**.
    """
)

st.caption(
    f"Periode data: {start_date.strftime('%d %b %Y')} "
    f"— {end_date.strftime('%d %b %Y')}"
)



# 10. EXECUTIVE SUMMARY
section_title(
    "Executive Summary",
    "Ringkasan kondisi bisnis berdasarkan filter yang dipilih."
)


# Main metrics
total_sales = filtered_df["total_amount"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()
total_quantity = filtered_df["quantity"].sum()

aov = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

# Completion rate
status_order = (
    filtered_df
    .groupby("order_status")["order_id"]
    .nunique()
)

completed_orders = status_order.get("Selesai", 0)

completion_rate = (
    completed_orders / total_orders * 100
    if total_orders > 0
    else 0
)


# KPI
col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Sales</div>
            <div class="kpi-value">{format_rupiah(total_sales)}</div>
            <div class="kpi-subtitle">Nilai penjualan</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{format_number(total_orders)}</div>
            <div class="kpi-subtitle">Unique orders</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Customers</div>
            <div class="kpi-value">{format_number(total_customers)}</div>
            <div class="kpi-subtitle">Unique customers</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Quantity</div>
            <div class="kpi-value">{format_number(total_quantity)}</div>
            <div class="kpi-subtitle">Units sold</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Order Value</div>
            <div class="kpi-value">{format_rupiah(aov)}</div>
            <div class="kpi-subtitle">Sales / unique order</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# 11. EXECUTIVE OBSERVATION
top_category_sales = (
    filtered_df
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_category = top_category_sales.index[0]

top_category_value = top_category_sales.iloc[0]

category_share = (
    top_category_value / total_sales * 100
    if total_sales > 0
    else 0
)


top_province_sales = (
    filtered_df
    .groupby("customer_province")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_province = top_province_sales.index[0]

top_payment_sales = (
    filtered_df
    .groupby("payment_method")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_payment = top_payment_sales.index[0]


observation_box(
    "Executive Observation",
    f"""
    Berdasarkan filter saat ini, total penjualan mencapai
    <b>{format_rupiah(total_sales)}</b> dari
    <b>{format_number(total_orders)}</b> unique order dan
    <b>{format_number(total_customers)}</b> customer.

    Kategori dengan kontribusi penjualan terbesar adalah
    <b>{top_category}</b> dengan kontribusi sekitar
    <b>{category_share:.1f}%</b> dari total sales.

    Provinsi dengan sales terbesar adalah
    <b>{top_province}</b>, sedangkan metode pembayaran dengan
    sales terbesar adalah <b>{top_payment}</b>.
    """
)


business_box(
    "Business Implication",
    """
    Fokus analisis berikutnya sebaiknya diarahkan pada faktor yang
    membentuk sales: kategori dan produk bernilai tinggi,
    perilaku pelanggan, frekuensi pembelian, serta distribusi
    geografis. Hal ini membantu membedakan apakah revenue berasal
    dari volume transaksi atau nilai transaksi yang tinggi.
    """
)


# 12. SALES OVERVIEW
section_title(
    "Sales Overview",
    "Melihat perkembangan penjualan berdasarkan waktu."
)

monthly_sales = (
    filtered_df
    .groupby("month_period")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("month_period")
)

monthly_sales["month"] = (
    monthly_sales["month_period"]
    .dt.strftime("%b %Y")
)

fig_monthly = px.area(
    monthly_sales,
    x="month",
    y="total_amount",
    markers=True,
    title="Monthly Sales"
)

fig_monthly.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Sales",
    hovermode="x unified"
)

fig_monthly.update_yaxes(
    tickprefix="Rp",
    tickformat="~s"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# 13. MONTHLY OBSERVATION
if len(monthly_sales) >= 2:
    latest_sales = monthly_sales.iloc[-1]["total_amount"]
    previous_sales = monthly_sales.iloc[-2]["total_amount"]
    growth = (
        (latest_sales - previous_sales)
        / previous_sales
        * 100
        if previous_sales != 0
        else 0
    )

    best_month_row = monthly_sales.loc[
        monthly_sales["total_amount"].idxmax()
    ]

    best_month = best_month_row["month"]
    best_month_sales = best_month_row["total_amount"]
    trend_word = "meningkat" if growth >= 0 else "menurun"

    observation_box(
        "Monthly Sales Observation",
        f"""
        Sales pada periode terbaru sebesar
        <b>{format_rupiah(latest_sales)}</b>.

        Dibandingkan periode sebelumnya, sales
        <b>{trend_word}</b> sebesar <b>{abs(growth):.2f}%</b>.

        Periode dengan sales tertinggi dalam filter saat ini adalah
        <b>{best_month}</b> dengan nilai
        <b>{format_rupiah(best_month_sales)}</b>.
        """
    )

else:

    observation_box(
        "Monthly Sales Observation",
        "Filter saat ini hanya mencakup satu periode sehingga perbandingan growth belum dapat dilakukan."
    )


# 14. CATEGORY ANALYSIS

section_title(
    "Category Performance",
    "Membandingkan kontribusi sales antar kategori."
)


category_sales = (
    filtered_df
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)


fig_category = px.bar(
    category_sales,
    x="total_amount",
    y="category",
    orientation="h",
    text_auto=".2s",
    title="Sales by Category"
)

fig_category.update_layout(
    xaxis_title="Sales",
    yaxis_title="Category"
)

fig_category.update_xaxes(
    tickprefix="Rp",
    tickformat="~s"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# Category observation
top_category_row = category_sales.iloc[-1]

top_category_name = top_category_row["category"]

top_category_sales_value = top_category_row["total_amount"]

top_category_percentage = (
    top_category_sales_value / total_sales * 100
)


observation_box(
    "Category Observation",
    f"""
    <b>{top_category_name}</b> merupakan kategori dengan
    sales terbesar yaitu <b>{format_rupiah(top_category_sales_value)}</b>,
    atau sekitar <b>{top_category_percentage:.1f}%</b> dari total sales.

    Perhatikan bahwa kategori dengan quantity tertinggi belum tentu
    menjadi kategori dengan sales tertinggi karena nilai produk
    per unit berbeda.
    """
)


# 15. ORDER STATUS

section_title(
    "Order Status",
    "Distribusi unique order berdasarkan status transaksi."
)


status_data = (
    filtered_df
    .groupby("order_status")["order_id"]
    .nunique()
    .reset_index(name="orders")
)


fig_status = px.pie(
    status_data,
    names="order_status",
    values="orders",
    hole=0.55,
    title="Order Status Distribution"
)

fig_status.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)


completed = status_data.loc[
    status_data["order_status"] == "Selesai",
    "orders"
].sum()

cancelled = status_data.loc[
    status_data["order_status"] == "Dibatalkan",
    "orders"
].sum()

returned = status_data.loc[
    status_data["order_status"] == "Dikembalikan",
    "orders"
].sum()


completion_rate = (
    completed / total_orders * 100
    if total_orders > 0
    else 0
)

cancel_rate = (
    cancelled / total_orders * 100
    if total_orders > 0
    else 0
)

return_rate = (
    returned / total_orders * 100
    if total_orders > 0
    else 0
)


observation_box(
    "Order Status Observation",
    f"""
    Dari <b>{format_number(total_orders)}</b> unique order,
    sekitar <b>{completion_rate:.2f}%</b> berstatus selesai.

    Tingkat pembatalan berada di sekitar
    <b>{cancel_rate:.2f}%</b>, sedangkan tingkat pengembalian
    sekitar <b>{return_rate:.2f}%</b>.
    """
)


# ============================================================
# 16. PAYMENT METHOD
# ============================================================

section_title(
    "Payment Performance",
    "Melihat kontribusi sales berdasarkan metode pembayaran."
)


payment_sales = (
    filtered_df
    .groupby("payment_method")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)


fig_payment = px.bar(
    payment_sales,
    x="payment_method",
    y="total_amount",
    text_auto=".2s",
    title="Sales by Payment Method"
)

fig_payment.update_layout(
    xaxis_title="Payment Method",
    yaxis_title="Sales"
)

fig_payment.update_yaxes(
    tickprefix="Rp",
    tickformat="~s"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)


payment_top = payment_sales.iloc[0]
payment_top_name = payment_top["payment_method"]
payment_top_value = payment_top["total_amount"]
payment_share = (
    payment_top_value / total_sales * 100
)


observation_box(
    "Payment Observation",
    f"""
    <b>{payment_top_name}</b> menjadi metode pembayaran dengan
    kontribusi sales terbesar yaitu
    <b>{format_rupiah(payment_top_value)}</b>
    atau sekitar <b>{payment_share:.1f}%</b> dari total sales.
    """
)


# 17. PRODUCT ANALYSIS
section_title(
    "Product Performance",
    "Membandingkan produk berdasarkan sales dan quantity."
)


col1, col2 = st.columns(2)


# Top Products by Sales
with col1:

    product_sales = (
        filtered_df
        .groupby("product_name")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_product_sales = px.bar(
        product_sales,
        x="total_amount",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Sales",
        text_auto=".2s"
    )

    fig_product_sales.update_layout(
        xaxis_title="Sales",
        yaxis_title="Product"
    )

    fig_product_sales.update_xaxes(
        tickprefix="Rp",
        tickformat="~s"
    )

    st.plotly_chart(
        fig_product_sales,
        use_container_width=True
    )


# -----------------------------
# Top Products by Quantity
# -----------------------------

with col2:

    product_quantity = (
        filtered_df
        .groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_product_quantity = px.bar(
        product_quantity,
        x="quantity",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Quantity",
        text_auto=True
    )

    fig_product_quantity.update_layout(
        xaxis_title="Quantity",
        yaxis_title="Product"
    )

    st.plotly_chart(
        fig_product_quantity,
        use_container_width=True
    )


# Product observation

top_sales_product = product_sales.iloc[-1]

top_quantity_product = product_quantity.iloc[-1]


observation_box(
    "Product Observation",
    f"""
    Produk dengan sales tertinggi adalah
    <b>{top_sales_product['product_name']}</b>
    dengan sales sebesar
    <b>{format_rupiah(top_sales_product['total_amount'])}</b>.

    Sementara itu, produk dengan quantity tertinggi adalah
    <b>{top_quantity_product['product_name']}</b>
    dengan total <b>{format_number(top_quantity_product['quantity'])}</b>
    unit.

    Perbedaan ini menunjukkan bahwa produk dengan volume penjualan
    tinggi belum tentu menghasilkan revenue terbesar.
    """
)

# 18. CUSTOMER ANALYSIS
section_title(
    "Customer Analysis",
    "Memahami perilaku pembelian customer."
)


customer_summary = (
    filtered_df
    .groupby("customer_id")
    .agg(
        orders=("order_id", "nunique"),
        sales=("total_amount", "sum")
    )
    .reset_index()
)


customer_summary["customer_type"] = customer_summary[
    "orders"
].apply(
    lambda x: "Repeat Customer"
    if x > 1
    else "One-time Customer"
)


repeat_customers = (
    customer_summary["customer_type"]
    == "Repeat Customer"
).sum()

one_time_customers = (
    customer_summary["customer_type"]
    == "One-time Customer"
).sum()


repeat_rate = (
    repeat_customers / len(customer_summary) * 100
    if len(customer_summary) > 0
    else 0
)


col1, col2 = st.columns(2)


with col1:

    frequency_data = (
        customer_summary["orders"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    frequency_data.columns = [
        "orders_per_customer",
        "customers"
    ]

    fig_frequency = px.bar(
        frequency_data,
        x="orders_per_customer",
        y="customers",
        title="Customer Purchase Frequency"
    )

    fig_frequency.update_layout(
        xaxis_title="Jumlah Order per Customer",
        yaxis_title="Jumlah Customer"
    )

    st.plotly_chart(
        fig_frequency,
        use_container_width=True
    )


with col2:

    customer_type_data = pd.DataFrame(
        {
            "customer_type": [
                "Repeat Customer",
                "One-time Customer"
            ],
            "customers": [
                repeat_customers,
                one_time_customers
            ]
        }
    )

    fig_customer_type = px.pie(
        customer_type_data,
        names="customer_type",
        values="customers",
        hole=0.55,
        title="Customer Type"
    )

    fig_customer_type.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_customer_type,
        use_container_width=True
    )


observation_box(
    "Customer Observation",
    f"""
    Dari total <b>{format_number(len(customer_summary))}</b> customer
    pada filter saat ini, sekitar <b>{repeat_rate:.2f}%</b>
    merupakan repeat customer.

    Repeat customer didefinisikan secara deskriptif sebagai customer
    yang memiliki lebih dari satu unique order dalam data yang sedang
    dianalisis.
    """
)


business_box(
    "Business Implication",
    """
    Customer dengan frekuensi pembelian tinggi dapat dianalisis lebih
    lanjut berdasarkan monetary value dan recency untuk memahami
    customer mana yang memberikan kontribusi terbesar dan mana yang
    mulai kehilangan aktivitas pembelian.
    """
)



# 19. TOP CUSTOMERS
section_title(
    "Top Customers",
    "Customer dengan kontribusi sales terbesar."
)


top_customers = (
    customer_summary
    .sort_values("sales", ascending=False)
    .head(10)
)


fig_top_customers = px.bar(
    top_customers.sort_values("sales"),
    x="sales",
    y="customer_id",
    orientation="h",
    title="Top 10 Customers by Sales",
    text_auto=".2s"
)

fig_top_customers.update_layout(
    xaxis_title="Sales",
    yaxis_title="Customer ID"
)

fig_top_customers.update_xaxes(
    tickprefix="Rp",
    tickformat="~s"
)

st.plotly_chart(
    fig_top_customers,
    use_container_width=True
)



# 20. RFM ANALYSIS
section_title(
    "RFM Customer Segmentation",
    """
    Segmentasi customer berdasarkan Recency, Frequency, dan Monetary.
    Perhitungan dilakukan berdasarkan filter yang sedang aktif.
    """
)


# Reference date
reference_date = (
    filtered_df["order_date"].max()
    + pd.Timedelta(days=1)
)


rfm = (
    filtered_df
    .groupby("customer_id")
    .agg(
        recency=(
            "order_date",
            lambda x: (
                reference_date - x.max()
            ).days
        ),
        frequency=(
            "order_id",
            "nunique"
        ),
        monetary=(
            "total_amount",
            "sum"
        )
    )
    .reset_index()
)


# ------------------------------------------------------------
# RFM Scoring
# ------------------------------------------------------------

# Rank terlebih dahulu agar qcut lebih aman
rfm["r_rank"] = rfm["recency"].rank(
    method="first"
)

rfm["f_rank"] = rfm["frequency"].rank(
    method="first"
)

rfm["m_rank"] = rfm["monetary"].rank(
    method="first"
)


if len(rfm) >= 5:

    rfm["r_score"] = pd.qcut(
        rfm["r_rank"],
        q=5,
        labels=[5, 4, 3, 2, 1]
    ).astype(int)

    rfm["f_score"] = pd.qcut(
        rfm["f_rank"],
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    rfm["m_score"] = pd.qcut(
        rfm["m_rank"],
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

else:

    # Fallback jika customer terlalu sedikit
    rfm["r_score"] = 3
    rfm["f_score"] = 3
    rfm["m_score"] = 3


# ------------------------------------------------------------
# RFM Segment
# ------------------------------------------------------------

def rfm_segment(row):

    r = row["r_score"]
    f = row["f_score"]
    m = row["m_score"]

    if r >= 4 and f >= 4 and m >= 4:

        return "Champions"

    elif f >= 4 and m >= 3:

        return "Loyal Customers"

    elif r >= 4 and f <= 3:

        return "Potential Loyalists"

    elif r <= 2 and f >= 3 and m >= 3:

        return "At Risk"

    elif r == 3 and f >= 2 and m >= 2:

        return "Need Attention"

    else:

        return "Low Engagement"


rfm["segment"] = rfm.apply(
    rfm_segment,
    axis=1
)


# ------------------------------------------------------------
# RFM Visualization
# ------------------------------------------------------------

rfm_segment_data = (
    rfm
    .groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        sales=("monetary", "sum")
    )
    .reset_index()
)


rfm_segment_data = rfm_segment_data.sort_values(
    "customers",
    ascending=False
)


col1, col2 = st.columns(2)


with col1:

    fig_rfm_count = px.bar(
        rfm_segment_data,
        x="segment",
        y="customers",
        title="Customers by RFM Segment",
        text_auto=True
    )

    fig_rfm_count.update_layout(
        xaxis_title="RFM Segment",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig_rfm_count,
        use_container_width=True
    )


with col2:

    fig_rfm_sales = px.bar(
        rfm_segment_data.sort_values("sales"),
        x="sales",
        y="segment",
        orientation="h",
        title="Sales by RFM Segment",
        text_auto=".2s"
    )

    fig_rfm_sales.update_layout(
        xaxis_title="Sales",
        yaxis_title="RFM Segment"
    )

    fig_rfm_sales.update_xaxes(
        tickprefix="Rp",
        tickformat="~s"
    )

    st.plotly_chart(
        fig_rfm_sales,
        use_container_width=True
    )


# ------------------------------------------------------------
# RFM Observation
# ------------------------------------------------------------

top_rfm_sales = rfm_segment_data.loc[
    rfm_segment_data["sales"].idxmax()
]

top_rfm_segment = top_rfm_sales["segment"]
top_rfm_sales_value = top_rfm_sales["sales"]
top_rfm_customer_count = top_rfm_sales["customers"]


observation_box(
    "RFM Observation",
    f"""
    Segment <b>{top_rfm_segment}</b> memberikan kontribusi sales
    terbesar yaitu <b>{format_rupiah(top_rfm_sales_value)}</b>
    dari <b>{format_number(top_rfm_customer_count)}</b> customer.

    Segmentasi ini bersifat <b>project-specific</b> berdasarkan
    aturan scoring RFM yang digunakan pada dashboard, sehingga label
    seperti Champions atau At Risk bukan kategori universal.
    """
)


business_box(
    "Business Implication",
    """
    RFM dapat digunakan sebagai dasar untuk membedakan pendekatan
    customer engagement. Customer dengan recency dan frequency tinggi
    dapat dianalisis untuk retention, sedangkan customer dengan
    historical monetary value tinggi tetapi recency rendah dapat
    dianalisis lebih lanjut sebagai kelompok yang perlu diperhatikan.
    """
)


# ============================================================
# 21. GEOGRAPHIC ANALYSIS
# ============================================================

section_title(
    "Geographic Analysis",
    "Melihat distribusi sales berdasarkan provinsi."
)


province_sales = (
    filtered_df
    .groupby("customer_province")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values(ascending=True)
    .reset_index()
)


fig_province = px.bar(
    province_sales,
    x="total_amount",
    y="customer_province",
    orientation="h",
    title="Top 10 Provinces by Sales",
    text_auto=".2s"
)

fig_province.update_layout(
    xaxis_title="Sales",
    yaxis_title="Province"
)

fig_province.update_xaxes(
    tickprefix="Rp",
    tickformat="~s"
)

st.plotly_chart(
    fig_province,
    use_container_width=True
)


top_province_row = province_sales.iloc[-1]

top_province_name = top_province_row[
    "customer_province"
]

top_province_value = top_province_row[
    "total_amount"
]


province_share = (
    top_province_value / total_sales * 100
)


observation_box(
    "Geographic Observation",
    f"""
    Provinsi dengan sales terbesar adalah
    <b>{top_province_name}</b> dengan kontribusi
    <b>{format_rupiah(top_province_value)}</b>,
    sekitar <b>{province_share:.1f}%</b> dari total sales.
    """
)


# ============================================================
# 22. FILTERED DATA
# ============================================================

section_title(
    "Filtered Data",
    "Data transaksi berdasarkan filter yang sedang aktif."
)


with st.expander("Lihat Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )


# ============================================================
# 23. DOWNLOAD DATA
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇Download Filtered Data",
    data=csv_data,
    file_name="filtered_ecommerce_data.csv",
    mime="text/csv"
)


# ============================================================
# 24. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        E-Commerce Sales & Customer Analytics Dashboard
        <br>
        Built with Python, Pandas, Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)