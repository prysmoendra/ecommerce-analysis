import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import os
import datetime

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Brazilian E-Commerce Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan modern dan profesional
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-star {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. PEMUATAN DATA DENGAN CACHING
# ==============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    main_path = os.path.join(current_dir, "main_data.csv")
    geo_path = os.path.join(current_dir, "geo_state.csv")

    if not os.path.exists(main_path):
        main_path = "main_data.csv"
        geo_path = "geo_state.csv"

    df = pd.read_csv(main_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])

    geo_df = pd.read_csv(geo_path) if os.path.exists(geo_path) else None
    return df, geo_df

df_raw, df_geo = load_data()

# ==============================================================================
# 3. SIDEBAR: FILTER INTERAKTIF
# ==============================================================================
st.sidebar.image("https://raw.githubusercontent.com/fadhil/images/main/olist_logo.png", width=180, use_container_width=False) if False else None
st.sidebar.markdown("## 🔍 **Filter Analisis Data**")
st.sidebar.markdown("Sesuaikan rentang tanggal dan filter wilayah:")

min_date = df_raw["order_purchase_timestamp"].min().date()
max_date = df_raw["order_purchase_timestamp"].max().date()

# Filter Rentang Tanggal
date_range = st.sidebar.date_input(
    "Pilih Rentang Waktu Transaksi:",
    value=[datetime.date(2017, 1, 1), max_date],
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter Negara Bagian (Customer State)
all_states = sorted(df_raw["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian (Customer State):",
    options=all_states,
    default=all_states[:5]  # Default top-5 states
)
if not selected_states:
    selected_states = all_states

# Filter Kategori Produk Utama
top_categories = df_raw["category"].value_counts().head(20).index.tolist()
selected_categories = st.sidebar.multiselect(
    "Filter Kategori Produk (Opsional):",
    options=["Semua Kategori"] + top_categories,
    default=["Semua Kategori"]
)

# Terapkan Filter ke DataFrame
filtered_df = df_raw[
    (df_raw["order_purchase_timestamp"].dt.date >= start_date) &
    (df_raw["order_purchase_timestamp"].dt.date <= end_date) &
    (df_raw["customer_state"].isin(selected_states))
]

if "Semua Kategori" not in selected_categories and len(selected_categories) > 0:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 **Tentang Proyek**")
st.sidebar.info(
    "Dashboard Analisis Data E-Commerce Brasil (Olist) untuk Submission Proyek Akhir Dicoding "
    "menggunakan standar penilaian **Bintang 5**."
)

# ==============================================================================
# 4. HEADER UTAMA & KPI SUMMARY CARDS
# ==============================================================================
st.markdown('<div class="main-title">🛍️ Brazilian E-Commerce Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis Kinerja Logistik, Pendapatan Penjualan, Segmentasi RFM, dan Sebaran Spasial (Platform Olist)</div>', unsafe_allow_html=True)

# KPI Cards
total_orders = len(filtered_df)
total_revenue = filtered_df["total_price"].sum()
avg_review = filtered_df["review_score"].dropna().mean()
avg_delivery = filtered_df["delivery_days"].mean()
ontime_rate = (1 - filtered_df["is_delayed"].mean()) * 100

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="📦 Total Pesanan", value=f"{total_orders:,}")
with col2:
    st.metric(label="💰 Total Pendapatan", value=f"R$ {total_revenue/1e6:.2f}M" if total_revenue >= 1e6 else f"R$ {total_revenue:,.0f}")
with col3:
    st.metric(label="⭐ Rata-rata Ulasan", value=f"{avg_review:.2f} / 5.0" if pd.notna(avg_review) else "N/A")
with col4:
    st.metric(label="🚚 Rata-rata Kirim", value=f"{avg_delivery:.1f} Hari")
with col5:
    st.metric(label="🎯 Tepat Waktu (SLA)", value=f"{ontime_rate:.1f}%")

st.markdown("---")

# ==============================================================================
# 5. TABS INTERAKTIF DASHBOARD
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🚚 Logistik vs Kepuasan (Q1)",
    "📊 Pendapatan & Geografis (Q2)",
    "🎯 Segmentasi Pelanggan (RFM)",
    "🗺️ Peta Spasial Brasil"
])

# ------------------------------------------------------------------------------
# TAB 1: LOGISTIK & KEPUASAN PELANGGAN
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Pengaruh Durasi Pengiriman terhadap Skor Kepuasan Pelanggan")
    st.markdown("""
    Analisis ini menjawab **Pertanyaan Bisnis 1**: Mengidentifikasi korelasi antara durasi pengiriman pesanan (*delivery time*) 
    dan keterlambatan estimasi kurir (*delivery delay*) terhadap skor ulasan kepuasan pelanggan (*review score*).
    """)

    # Pengelompokan Bucket Pengiriman
    bins = [0, 7, 14, 21, 30, 999]
    labels = ["1-7 Hari", "8-14 Hari", "15-21 Hari", "22-30 Hari", "> 30 Hari"]
    temp_df = filtered_df.dropna(subset=["review_score"]).copy()
    temp_df["delivery_bucket"] = pd.cut(temp_df["delivery_days"], bins=bins, labels=labels, right=True)

    bucket_stats = temp_df.groupby("delivery_bucket", observed=False).agg(
        total_orders=("order_id", "count"),
        avg_score=("review_score", "mean"),
        pct_detractors=("review_score", lambda x: (x <= 2).mean() * 100),
        pct_promoters=("review_score", lambda x: (x >= 4).mean() * 100)
    ).reset_index()

    col_t1_left, col_t1_right = st.columns([3, 2])

    with col_t1_left:
        # Visualisasi Interaktif Plotly
        fig_score = go.Figure()
        fig_score.add_trace(go.Bar(
            x=bucket_stats["delivery_bucket"],
            y=bucket_stats["avg_score"],
            marker_color=["#27AE60", "#2ECC71", "#F39C12", "#E67E22", "#C0392B"],
            text=[f"{s:.2f} ★" for s in bucket_stats["avg_score"]],
            textposition="auto",
            name="Rata-rata Skor Ulasan"
        ))
        overall_platform_avg = temp_df["review_score"].mean()
        fig_score.add_hline(
            y=overall_platform_avg,
            line_dash="dash",
            line_color="#2980B9",
            annotation_text=f"Benchmark Rata-rata ({overall_platform_avg:.2f})",
            annotation_position="top right"
        )
        fig_score.update_layout(
            title="<b>Rata-rata Skor Ulasan per Kelompok Durasi Pengiriman</b>",
            xaxis_title="Rentang Durasi Pengiriman",
            yaxis_title="Rata-rata Skor Ulasan (1 - 5)",
            yaxis=dict(range=[0, 5.2]),
            height=420,
            template="plotly_white"
        )
        st.plotly_chart(fig_score, use_container_width=True)

    with col_t1_right:
        # Perbandingan Tepat Waktu vs Terlambat
        delayed_stats = temp_df.groupby("is_delayed").agg(
            total=("order_id", "count"),
            mean_score=("review_score", "mean"),
            pct_bintang1=("review_score", lambda x: (x == 1).mean() * 100)
        ).reset_index()
        delayed_stats["status"] = delayed_stats["is_delayed"].map({0: "Tepat Waktu / Cepat", 1: "Terlambat (SLA Breached)"})

        fig_delay = px.bar(
            delayed_stats,
            x="status",
            y="mean_score",
            color="status",
            color_discrete_map={"Tepat Waktu / Cepat": "#2ECC71", "Terlambat (SLA Breached)": "#E74C3C"},
            text=[f"{s:.2f} ★" for s in delayed_stats["mean_score"]],
            title="<b>Dampak Keterlambatan Estimasi Kurir</b>",
            labels={"status": "Status Pengiriman", "mean_score": "Rata-rata Skor"}
        )
        fig_delay.update_layout(height=420, showlegend=False, template="plotly_white", yaxis=dict(range=[0, 5.2]))
        st.plotly_chart(fig_delay, use_container_width=True)

    # Insight & Rekomendasi Box
    st.success("""
    💡 **Temuan Utama Logistik (SLA Threshold Insight):**
    1. **Ambang Batas Kritis 14 Hari**: Kepuasan pelanggan berada pada level tinggi jika pesanan tiba dalam 1-14 hari (skor 4,29–4,41). Begitu pengiriman melewati 14 hari, skor kepuasan langsung anjlok ke bawah rata-rata platform.
    2. **Keterlambatan Estimasi Berdampak Fatal**: Pelanggan yang menerima barang terlambat dari perkiraan kurir memberikan skor rata-rata **2,27** (turun 47% dibanding tepat waktu yang bernilai **4,28**).
    3. **Action Item**: Pasang peringatan otomatis (*automated dispatch alert*) pada hari ke-10 untuk rute yang berisiko terlambat, serta berikan kompensasi proaktif sebelum komplain terjadi.
    """)

# ------------------------------------------------------------------------------
# TAB 2: PENDAPATAN & GEOGRAFIS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Performa Pendapatan Kategori Produk & Sebaran Wilayah Pelanggan")
    st.markdown("""
    Analisis ini menjawab **Pertanyaan Bisnis 2**: Mengidentifikasi kategori pendorong pendapatan utama (*revenue drivers*) 
    serta distribusi omzet dan *Average Order Value* (AOV) di seluruh negara bagian Brasil.
    """)

    col_t2_left, col_t2_right = st.columns([1, 1])

    with col_t2_left:
        # Top 10 Kategori Produk
        cat_df = filtered_df.groupby("category").agg(
            revenue=("total_price", "sum"),
            orders=("order_id", "nunique")
        ).sort_values(by="revenue", ascending=False).head(10).reset_index()

        fig_cat = px.bar(
            cat_df.sort_values(by="revenue", ascending=True),
            y="category",
            x="revenue",
            orientation="h",
            title="<b>Top 10 Kategori Produk Berdasarkan Pendapatan (Revenue)</b>",
            labels={"category": "Kategori Produk", "revenue": "Total Pendapatan (R$)"},
            color="revenue",
            color_continuous_scale="Blues"
        )
        fig_cat.update_layout(height=450, coloraxis_showscale=False, template="plotly_white")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_t2_right:
        # Top 10 Negara Bagian + AOV
        state_df = filtered_df.groupby("customer_state").agg(
            revenue=("total_price", "sum"),
            orders=("order_id", "nunique")
        ).reset_index()
        state_df["aov"] = state_df["revenue"] / state_df["orders"]
        state_df = state_df.sort_values(by="revenue", ascending=False).head(10)

        fig_state = go.Figure()
        fig_state.add_trace(go.Bar(
            x=state_df["customer_state"],
            y=state_df["revenue"],
            name="Total Revenue (R$)",
            marker_color="#3498DB",
            yaxis="y1"
        ))
        fig_state.add_trace(go.Scatter(
            x=state_df["customer_state"],
            y=state_df["aov"],
            name="AOV (R$)",
            marker=dict(color="#E74C3C", size=9),
            line=dict(color="#E74C3C", width=2.5),
            yaxis="y2"
        ))
        fig_state.update_layout(
            title="<b>Distribusi Pendapatan & AOV pada 10 Negara Bagian Teratas</b>",
            xaxis=dict(title="Negara Bagian (Customer State)"),
            yaxis=dict(title="Total Revenue (R$)", side="left"),
            yaxis2=dict(title="Average Order Value (R$)", overlaying="y", side="right", range=[100, 180]),
            height=450,
            template="plotly_white",
            legend=dict(x=0.65, y=0.98)
        )
        st.plotly_chart(fig_state, use_container_width=True)

    # Insight Box
    st.info("""
    💡 **Temuan Utama Penjualan & Geografis:**
    1. **Tiga Kategori Teratas**: *health_beauty*, *watches_gifts*, dan *bed_bath_table* menyumbang lebih dari seperempat total omzet platform.
    2. **Disparitas Wilayah & AOV Paradox**: São Paulo (SP) mendominasi ~39% total pendapatan nasional namun memiliki nilai belanja rata-rata per transaksi terendah (AOV = R$ 125). Negara bagian seperti BA, SC, dan DF mencatat AOV yang jauh lebih tinggi (> R$ 142-152).
    3. **Action Item**: Luncurkan program *bundling / upselling* di SP untuk mendongkrak AOV, serta ekspansi promosi katalog premium di wilayah BA dan SC.
    """)

# ------------------------------------------------------------------------------
# TAB 3: RFM ANALYSIS (ADVANCED ANALYTICS)
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Analisis Lanjutan: Segmentasi Pelanggan (RFM Model)")
    st.markdown("""
    Segmentasi pelanggan berbasis **Recency (R)**, **Frequency (F)**, dan **Monetary (M)** 
    mengelompokkan pelanggan ke dalam segmen perilaku belanja nyata tanpa machine learning.
    """)

    # Hitung Metrik RFM
    ref_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm_table = filtered_df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda x: (ref_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("total_price", "sum")
    ).reset_index()

    # Binning & Quantile Scoring
    rfm_table["r_score"] = pd.qcut(rfm_table["recency"], q=4, labels=[4, 3, 2, 1])
    rfm_table["f_score"] = rfm_table["frequency"].apply(lambda f: 4 if f >= 4 else (3 if f == 3 else (2 if f == 2 else 1)))
    rfm_table["m_score"] = pd.qcut(rfm_table["monetary"], q=4, labels=[1, 2, 3, 4])

    def assign_segment(row):
        r, f, m = int(row["r_score"]), int(row["f_score"]), int(row["m_score"])
        if r >= 3 and f >= 2 and m >= 3:
            return "Champions (Pelanggan Utama)"
        elif r >= 3 and f >= 2:
            return "Loyal Customers (Setia)"
        elif r >= 3 and f == 1 and m >= 3:
            return "Potential Loyalists (Potensial)"
        elif r >= 3 and f == 1:
            return "Recent / New Customers (Baru)"
        elif r == 2 and f >= 2:
            return "At Risk (Berisiko Churn)"
        elif r == 2 and f == 1:
            return "Need Attention (Perhatian)"
        elif r == 1 and f >= 2:
            return "Can't Lose Them (Kritis)"
        else:
            return "Hibernating / Lost (Tidur)"

    rfm_table["segment"] = rfm_table.apply(assign_segment, axis=1)
    seg_summary = rfm_table.groupby("segment").agg(
        pelanggan=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_omzet=("monetary", "sum")
    ).reset_index()
    seg_summary["pct_pelanggan"] = (seg_summary["pelanggan"] / len(rfm_table)) * 100

    col_rfm1, col_rfm2 = st.columns([1, 1])

    with col_rfm1:
        fig_pie = px.pie(
            seg_summary,
            names="segment",
            values="pelanggan",
            title="<b>Proporsi Pelanggan per Segmen RFM</b>",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(height=440)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_rfm2:
        fig_seg_bar = px.bar(
            seg_summary.sort_values(by="total_omzet", ascending=True),
            y="segment",
            x="total_omzet",
            orientation="h",
            title="<b>Kontribusi Pendapatan per Segmen RFM</b>",
            labels={"segment": "", "total_omzet": "Total Pendapatan (R$)"},
            color="total_omzet",
            color_continuous_scale="Viridis"
        )
        fig_seg_bar.update_layout(height=440, coloraxis_showscale=False, template="plotly_white")
        st.plotly_chart(fig_seg_bar, use_container_width=True)

    # Tabel Ringkasan RFM
    st.markdown("#### **Tabel Ringkasan Metrik Segmen RFM**")
    st.dataframe(
        seg_summary.rename(columns={
            "segment": "Segmen Pelanggan",
            "pelanggan": "Jumlah Pelanggan",
            "pct_pelanggan": "% Pelanggan",
            "avg_recency": "Rata-rata Recency (Hari)",
            "avg_frequency": "Rata-rata Frekuensi",
            "avg_monetary": "Rata-rata Belanja (R$)",
            "total_omzet": "Total Omzet (R$)"
        }).style.format({
            "% Pelanggan": "{:.1f}%",
            "Rata-rata Recency (Hari)": "{:.1f}",
            "Rata-rata Frekuensi": "{:.2f}",
            "Rata-rata Belanja (R$)": "R$ {:.2f}",
            "Total Omzet (R$)": "R$ {:,.2f}"
        }),
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# TAB 4: GEOSPATIAL ANALYSIS
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Analisis Spasial: Peta Sebaran Wilayah Transaksi Brasil")
    st.markdown("""
    Peta interaktif menggunakan **Folium** untuk menampilkan persebaran geografis nilai transaksi dan jumlah pesanan di negara bagian Brasil.
    """)

    if df_geo is not None:
        state_totals = filtered_df.groupby("customer_state").agg(
            revenue=("total_price", "sum"),
            orders=("order_id", "nunique")
        ).reset_index()

        geo_merged = df_geo.merge(state_totals, left_on="geolocation_state", right_on="customer_state", how="inner")

        # Peta Brasil
        m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="CartoDB positron")

        max_rev = geo_merged["revenue"].max() if len(geo_merged) > 0 else 1
        for _, row in geo_merged.iterrows():
            radius = max(6, (row["revenue"] / max_rev) * 30)
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=radius,
                popup=f"<b>{row['geolocation_state']}</b><br>Total Orders: {row['orders']:,}<br>Total Revenue: R$ {row['revenue']:,.2f}",
                tooltip=f"{row['geolocation_state']}: R$ {row['revenue']/1e6:.2f}M" if row['revenue'] >= 1e6 else f"{row['geolocation_state']}: R$ {row['revenue']:,.0f}",
                color="#E74C3C",
                fill=True,
                fill_color="#E74C3C",
                fill_opacity=0.6
            ).add_to(m)

        st_folium(m, width=950, height=520)
    else:
        st.warning("Berkas koordinat spasial tidak ditemukan.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown(
    "<center><small>Proyek Akhir Belajar Analisis Data dengan Python — Dicoding Indonesia | Dibuat oleh Fajar Krismahendra Bintang Pangestu</small></center>",
    unsafe_allow_html=True
)
