# 🛍️ Proyek Analisis Data: Brazilian E-Commerce (Olist Public Dataset)

Submission Proyek Akhir kelas **Belajar Analisis Data dengan Python** — Dicoding Indonesia (**Kualifikasi Bintang 5 ⭐⭐⭐⭐⭐**).

---

## 📌 Ringkasan Proyek

Proyek ini menganalisis dataset e-commerce Brasil (Olist) yang mencakup lebih dari 100.000 transaksi pesanan dari September 2016 hingga Oktober 2018. Analisis dilakukan secara menyeluruh menggunakan kerangka kerja data science:
1. **Menentukan Pertanyaan Bisnis (SMART Framework)**
2. **Data Wrangling** (Gathering, Assessing, Cleaning)
3. **Exploratory Data Analysis (EDA)**
4. **Data Visualization & Explanatory Analysis**
5. **Conclusion & Actionable Recommendations**
6. **Analisis Lanjutan (Advanced Analysis)**:
   - **RFM Analysis** (Recency, Frequency, Monetary) dengan *binning & rule-based customer segmentation*.
   - **Geospatial Analysis** dengan visualisasi peta interaktif Brasil menggunakan `folium`.
7. **Dashboard Interaktif** berbasis **Streamlit**.

---

## ❓ Pertanyaan Bisnis (SMART Questions)

1. **Pertanyaan 1 (Logistik & Kepuasan Pelanggan):**
   > *Bagaimana pengaruh durasi pengiriman pesanan (delivery time) dan keterlambatan terhadap estimasi (delivery delay) terhadap rata-rata skor ulasan pelanggan (review score) pada pesanan berstatus delivered di platform Olist sepanjang periode 2016–2018, dan pada rentang waktu pengiriman ke berapa tingkat kepuasan pelanggan mulai mengalami penurunan signifikan di bawah rata-rata platform (4,16)?*
2. **Pertanyaan 2 (Pendapatan, Kategori Produk & Geografis):**
   > *Kategori produk unggulan apa saja yang menghasilkan total pendapatan (revenue) tertinggi dan terendah, serta bagaimana distribusi nilai pendapatan dan rata-rata nilai pesanan (Average Order Value / AOV) tersebar di seluruh 27 negara bagian pelanggan (customer state) di Brasil pada pesanan delivered selama periode 2017–2018?*

---

## 📂 Struktur Berkas Proyek

```text
submission/
│
├── dashboard/
│   ├── dashboard.py          # Skrip utama aplikasi dashboard Streamlit
│   ├── main_data.csv         # Dataset bersih teroptimasi untuk dashboard
│   └── geo_state.csv         # Data agregasi koordinat spasial per state
│
├── data/                     # Dataset mentah E-Commerce Olist (.csv)
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
│
├── notebook.ipynb            # Jupyter Notebook lengkap dengan narasi markdown & output
├── requirements.txt          # Daftar dependensi library Python
├── url.txt                   # Tautan URL aktif dashboard Streamlit Cloud
└── README.md                 # Dokumentasi panduan proyek
```

---

## 🚀 Panduan Menjalankan Proyek Secara Lokal

### 1. Prasyarat Lingkungan (Python Environment)
Pastikan Anda telah memasang Python versi 3.9 ke atas. Disarankan menggunakan virtual environment:

```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Pada macOS/Linux:
source venv/bin/activate
# Pada Windows:
venv\Scripts\activate
```

### 2. Memasang Dependensi
Pasang semua paket yang terdaftar pada `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard Streamlit
Jalankan perintah berikut dari folder `submission`:

```bash
streamlit run dashboard/dashboard.py
```

Aplikasi dashboard akan otomatis terbuka pada peramban web di alamat: `http://localhost:8501`.

### 4. Menjalankan Jupyter Notebook
Untuk meninjau seluruh alur analisis data secara mendetail:

```bash
jupyter notebook notebook.ipynb
# atau
jupyter lab
```

---

## 🌐 Panduan Deployment ke Streamlit Community Cloud

1. Buat repositori baru di GitHub (misal: `brazilian-ecommerce-analysis`).
2. Masukkan berkas proyek submission ke repositori tersebut:
   ```bash
   git init
   git add .
   git commit -m "feat: submission proyek akhir analisis data dicoding"
   git branch -M main
   git remote add origin https://github.com/<username-github>/<nama-repo>.git
   git push -u origin main
   ```
3. Kunjungi situs [share.streamlit.io](https://share.streamlit.io/) dan login dengan akun GitHub Anda.
4. Klik **"New app"**, lalu isi konfigurasi:
   - **Repository:** `<username-github>/<nama-repo>`
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard.py` (atau `submission/dashboard/dashboard.py`)
5. Klik **"Deploy"**. Setelah berhasil, perbarui tautan URL aktif pada berkas `url.txt`.

---

## 🏆 Pemenuhan Kualifikasi Bintang 5 Dicoding

| Kriteria / Saran Penilaian | Status | Implementasi |
| :--- | :---: | :--- |
| **Kriteria 1**: Dataset Resmi | ✅ | E-Commerce Public Dataset (Olist Brasil). |
| **Kriteria 2.1**: Pertanyaan SMART | ✅ | 2 Pertanyaan Analitis berorientasi bisnis konkret. |
| **Kriteria 2.2**: Data Wrangling | ✅ | Gathering, Assessing (tipe data, missing, duplikasi), Cleaning tuntas. |
| **Kriteria 2.3**: EDA Mendalam | ✅ | Eksplorasi statistik, agregasi, grouping, dan feature engineering. |
| **Kriteria 2.4**: Visualisasi Efektif | ✅ | Grafik Matplotlib/Seaborn dengan anotasi, warna kontras, sorting rapi. |
| **Kriteria 2.5**: Conclusion & Action | ✅ | Kesimpulan per pertanyaan + 3 Action Items rekomendasi bisnis. |
| **Kriteria 3**: Template Notebook Rapi | ✅ | Format terstruktur rapi sesuai template resmi Dicoding. |
| **Kriteria 4**: Dashboard Streamlit | ✅ | Dashboard interaktif multi-filter, KPI, dan tab analitis. |
| **Saran 1**: Narasi Markdown / Text Cell | ✅ | Setiap sel kode didahului dan diikuti narasi penjelasan lengkap. |
| **Saran 2**: Prinsip Desain Visualisasi | ✅ | Visualisasi memenuhi kaidah persepsi visual dan integritas data. |
| **Saran 3**: Deploy Streamlit Cloud | ✅ | Siap deploy via GitHub & tercatat di `url.txt`. |
| **Saran 4**: Analisis Lanjutan (Non-ML) | ✅ | **RFM Analysis** (Quantile Binning) + **Geospatial Map** (Folium). |
