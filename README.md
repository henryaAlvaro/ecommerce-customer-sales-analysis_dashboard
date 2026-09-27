# E-Commerce Sales & Customer Analytics

End-to-end data analytics project untuk menganalisis **penjualan, perilaku pelanggan, performa produk, transaksi, metode pembayaran, dan distribusi geografis** pada data e-commerce.

Project ini dibangun menggunakan **Python, Pandas, Plotly, dan Streamlit**, mulai dari proses data understanding, data cleaning, feature engineering, Exploratory Data Analysis (EDA), business analysis, hingga interactive dashboard.

---

## Project Overview

Dalam bisnis e-commerce, data transaksi dapat digunakan untuk memahami:

* Bagaimana perkembangan penjualan dari waktu ke waktu?
* Kategori produk mana yang memberikan kontribusi revenue terbesar?
* Produk mana yang paling banyak terjual?
* Apakah produk dengan quantity tinggi juga menghasilkan revenue tinggi?
* Bagaimana karakteristik customer?
* Berapa banyak customer yang melakukan pembelian berulang?
* Metode pembayaran apa yang paling banyak digunakan?
* Bagaimana distribusi penjualan berdasarkan wilayah?
* Customer mana yang memiliki kontribusi terbesar?
* Bagaimana segmentasi customer berdasarkan Recency, Frequency, dan Monetary (RFM)?

Project ini bertujuan mengubah data transaksi mentah menjadi **insight yang dapat digunakan untuk memahami kondisi bisnis dan mendukung pengambilan keputusan berbasis data.**

---

# Objectives

Project ini memiliki beberapa tujuan utama:

1. Memahami struktur dan karakteristik data e-commerce.
2. Membersihkan data dari masalah kualitas data.
3. Membuat fitur baru yang relevan untuk analisis.
4. Melakukan Exploratory Data Analysis (EDA).
5. Menganalisis performa penjualan.
6. Menganalisis performa produk dan kategori.
7. Menganalisis perilaku customer.
8. Mengidentifikasi repeat customer.
9. Melakukan customer segmentation menggunakan RFM.
10. Menganalisis performa berdasarkan metode pembayaran.
11. Menganalisis distribusi penjualan berdasarkan wilayah.
12. Membuat interactive dashboard menggunakan Streamlit.
13. Menyediakan filtered data yang dapat di-download.

---

# Technologies

Project ini menggunakan beberapa teknologi berikut:

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Bahasa pemrograman utama     |
| Pandas           | Data manipulation & analysis |
| NumPy            | Numerical computation        |
| Matplotlib       | Exploratory visualization    |
| Seaborn          | Statistical visualization    |
| Plotly           | Interactive visualization    |
| Streamlit        | Interactive dashboard        |
| Jupyter Notebook | Data exploration & analysis  |
| Git & GitHub     | Version control & portfolio  |

---

# Project Structure

```text
ecommerce-data-analytics/
│
├── Dataset/
│   └── data_fetures.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda.ipynb
│   └── 05_business_analysis.ipynb
│
├── app/
│   └── app.py
│
├── requirements.txt
│
└── README.md
```

---

# Project Workflow

Workflow project:

```text
Raw Data
   │
   ▼
Data Understanding
   │
   ▼
Data Cleaning
   │
   ▼
Feature Engineering
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Business Analysis
   │
   ▼
Customer Segmentation
   │
   ▼
Interactive Dashboard

```

---

# Data Understanding

Tahap pertama dilakukan untuk memahami struktur dataset sebelum melakukan analisis.

Beberapa hal yang diperiksa:

* Jumlah baris dan kolom
* Tipe data
* Missing values
* Duplicate values
* Distribusi data
* Unique values
* Nilai minimum dan maksimum
* Konsistensi kategori
* Validitas data

Contoh informasi dataset:

```text
order_id
order_date
customer_id
customer_name
customer_gender
customer_age
customer_city
customer_province
product_id
product_name
category
sub_category
unit_price
quantity
discount_percent
shipping_cost
total_amount
payment_method
order_status
delivery_date
rating
```

---

# Data Cleaning

Data cleaning dilakukan untuk memastikan dataset dapat digunakan untuk analisis.

Beberapa proses yang dilakukan:

### Missing Values

Memeriksa jumlah missing value pada setiap kolom.

```python
df.isna().sum()
```

Persentase missing value:

```python
df.isna().mean() * 100
```

### Duplicate

Memeriksa duplicate rows:

```python
df.duplicated().sum()
```

### Invalid Values

Memeriksa nilai yang tidak valid, seperti:

* Quantity negatif
* Harga negatif
* Discount tidak valid
* Rating di luar range
* Tanggal tidak valid

### Data Type

Memastikan kolom tanggal memiliki tipe datetime:

```python
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)
```

---

# Feature Engineering

Feature engineering dilakukan untuk menghasilkan fitur yang lebih informatif untuk analisis.

Beberapa fitur yang digunakan dalam project:

### Order Month

```python
df["order_month"] = df["order_date"].dt.month
```

### Order Year

```python
df["order_year"] = df["order_date"].dt.year
```

### Month Name

```python
df["order_month_name"] = df["order_date"].dt.strftime("%B")
```

### Gross Amount

```python
df["gross_amount"] = (
    df["unit_price"] * df["quantity"]
)
```

### Discount Amount

```python
df["discount_amount"] = (
    df["gross_amount"]
    * df["discount_percent"]
    / 100
)
```

### Delivery Days

```python
df["delivery_days"] = (
    df["delivery_date"]
    - df["order_date"]
).dt.days
```

### Customer Age Group

Customer dikelompokkan berdasarkan usia:

```text
<20
20-29
30-39
40-49
50-59
60+
```

---

# Exploratory Data Analysis

EDA dilakukan untuk menemukan pola, distribusi, hubungan antarvariabel, dan potensi insight bisnis.

EDA dibagi menjadi beberapa bagian.

---

## 4.1 Numerical Analysis

Kolom numerik yang dianalisis antara lain:

* customer_age
* unit_price
* quantity
* discount_percent
* shipping_cost
* total_amount
* rating
* delivery_days

Analisis meliputi:

* Mean
* Median
* Minimum
* Maximum
* Standard deviation
* Distribution
* Outlier

---

# 4.2 Categorical Analysis

Kolom categorical yang dianalisis:

* customer_gender
* customer_city
* customer_province
* category
* sub_category
* payment_method
* order_status
* customer_age_group

Analisis dilakukan menggunakan:

```python
value_counts()
```

Contoh:

```python
df["payment_method"].value_counts()
```

Tujuannya untuk memahami distribusi masing-masing kategori.

---

# 4.3 Categorical × Numerical

Analisis digunakan untuk mengetahui bagaimana kategori tertentu berhubungan dengan nilai numerik.

Contoh:

```text
Category × Sales
Gender × Sales
Age Group × Sales
Payment Method × Sales
Province × Sales
```

Contoh:

```python
df.groupby("category")["total_amount"].sum()
```

---

# 4.4 Numerical × Numerical

Digunakan untuk melihat hubungan antarvariabel numerik.

Contoh:

```text
Quantity × Total Amount
Unit Price × Total Amount
Discount × Total Amount
Age × Total Amount
```

Correlation dapat digunakan untuk melihat hubungan linear:

```python
df.corr(numeric_only=True)
```

---

# 4.5 Categorical × Categorical

Digunakan untuk memahami hubungan antarvariabel kategorikal.

Contoh:

```text
Gender × Payment Method
Gender × Order Status
Age Group × Category
Category × Order Status
```

Contoh:

```python
pd.crosstab(
    df["customer_gender"],
    df["payment_method"]
)
```

---

# Business Analysis

Setelah EDA selesai, analisis diarahkan pada pertanyaan bisnis.

---

# Category Performance

Hasil analisis menunjukkan bahwa kategori dengan sales terbesar adalah:

**Elektronik**

dengan total sales sekitar:

```text
Rp79,3 Miliar
```

Kategori lainnya memiliki kontribusi yang lebih kecil.

Namun, terdapat perbedaan antara quantity dan sales.

Kategori **Fashion Wanita** memiliki quantity tertinggi, tetapi bukan merupakan kategori dengan sales tertinggi.

### Insight

Hal ini menunjukkan bahwa:

> Produk dengan volume penjualan tinggi belum tentu menghasilkan revenue terbesar.

Nilai produk per unit menjadi faktor penting dalam menentukan revenue.

---

# Customer Gender Analysis

Distribusi sales berdasarkan gender relatif berimbang.

### Perempuan

```text
Sales       : Rp60,57 Miliar
Quantity    : 44.792
Customers   : 4.827
Orders      : 24.386
```

### Laki-laki

```text
Sales       : Rp59,92 Miliar
Quantity    : 46.929
Customers   : 4.834
Orders      : 25.614
```

### Insight

Perbedaan kontribusi sales antara customer laki-laki dan perempuan relatif kecil.

Artinya, berdasarkan dataset ini, sales tidak terkonsentrasi secara ekstrem pada salah satu kelompok gender.

---

# Customer Age Analysis

Kelompok usia yang dianalisis:

```text
<20
20-29
30-39
40-49
50-59
60+
```

Kelompok usia **30-39** memberikan total sales sekitar:

```text
Rp29,20 Miliar
```

Sedangkan kelompok **20-29** memiliki sales sekitar:

```text
Rp29,18 Miliar
```

### Insight

Kelompok usia produktif menjadi salah satu kontributor utama dalam transaksi e-commerce pada dataset ini.

Namun, karena dataset hanya merepresentasikan periode tertentu, hasil ini tidak otomatis dapat digeneralisasikan ke seluruh populasi konsumen.

---

# Product Performance

Analisis produk dilakukan menggunakan dua perspektif:

### Top Products by Sales

Produk dengan sales tertinggi antara lain:

```text
Aksesoris HP Sunt Pro
Aksesoris HP Cupiditate Basic
Audio Quos Plus
Laptop Eius Lite
Aksesoris HP Magnam Pro
```

### Top Products by Quantity

Beberapa produk memiliki quantity tinggi tetapi nilai sales relatif lebih kecil.

Contoh:

```text
Perlengkapan Kantor Labore Premium
Minuman Instan Ullam Lite
Sepeda Necessitatibus Edisi Spesial
```

### Insight

Analisis produk tidak cukup hanya menggunakan quantity.

Diperlukan minimal dua perspektif:

```text
Sales
+
Quantity
```

Dengan demikian dapat dibedakan antara:

* High volume product
* High value product

---

# Payment Method Analysis

Metode pembayaran yang dianalisis:

```text
E-Wallet
Transfer Bank
COD
Kartu Kredit
QRIS
```

E-Wallet memiliki kontribusi sales terbesar:

```text
± Rp38,59 Miliar
```

Sedangkan Kartu Kredit memiliki nilai sales per order yang relatif tinggi dibanding beberapa metode pembayaran lainnya.

### Insight

Perbedaan kontribusi metode pembayaran dapat dipengaruhi oleh:

* Jumlah order
* Nilai order
* Preferensi customer
* Karakteristik transaksi

Karena itu, jumlah transaksi dan nilai transaksi perlu dianalisis secara bersamaan.

---

# Order Status Analysis

Status order:

```text
Selesai
Dibatalkan
Diproses
Dikembalikan
```

Berdasarkan unique order:

```text
Selesai       : 39.038
Dibatalkan    : 3.980
Diproses      : 3.980
Dikembalikan  : 3.002
```

Persentase order selesai sekitar:

```text
77,?%
```

### Insight

Status order membantu memahami kondisi transaksi.

Namun:

```text
Diproses ≠ Gagal
```

Order yang masih diproses sebaiknya tidak langsung dianggap sebagai transaksi gagal.

---

# 1️⃣1️⃣ Geographic Analysis

Analisis geografis dilakukan berdasarkan:

```text
Province
City
```

Provinsi dengan sales terbesar:

```text
Banten
```

dengan sales sekitar:

```text
Rp8,69 Miliar
```

Beberapa wilayah lain dengan kontribusi tinggi antara lain:

```text
Bali
Jawa Tengah
DKI Jakarta
Jawa Timur
Lampung
Kalimantan Timur
Yogyakarta
NTB
Sumatera Barat
```

### Insight

Distribusi geografis dapat digunakan untuk memahami wilayah dengan kontribusi revenue tinggi.

Analisis lebih lanjut dapat menggabungkan:

```text
Sales
Orders
Customers
Average Order Value
```

sehingga perbedaan antara volume dan value per wilayah dapat terlihat lebih jelas.

---

# Repeat Customer Analysis

Customer dikelompokkan menjadi:

```text
One-time Customer
Repeat Customer
```

Definisi repeat customer:

> Customer yang melakukan lebih dari satu unique order dalam periode dataset.

Hasil analisis:

```text
Repeat Customers : 7.768
One-time         : 1.893
```

Repeat customer menyumbang sekitar:

```text
96,12%
```

dari total sales.

### Insight

Repeat customer memberikan kontribusi sales yang jauh lebih besar dibanding customer yang hanya melakukan satu order.

Namun, istilah **repeat customer** digunakan secara deskriptif dan tidak otomatis berarti customer tersebut loyal.

---

# Customer Purchase Frequency

Customer juga dikelompokkan berdasarkan jumlah order:

```text
1 order
2-3 orders
4-6 orders
7-10 orders
>10 orders
```

Hasil analisis menunjukkan bahwa customer dengan:

```text
7+ orders
```

memberikan kontribusi sekitar:

```text
59,81%
```

dari total sales.

### Insight

Customer dengan frekuensi transaksi tinggi memberikan kontribusi besar terhadap revenue.

Hal ini membuat frequency menjadi salah satu metrik penting dalam customer analytics.

---

# RFM Analysis

RFM digunakan untuk melakukan customer segmentation berdasarkan tiga indikator:

### Recency

Seberapa lama sejak customer terakhir melakukan transaksi.

```text
Semakin kecil → semakin baru
```

### Frequency

Seberapa sering customer melakukan transaksi.

```text
Semakin tinggi → semakin sering
```

### Monetary

Berapa besar total nilai transaksi customer.

```text
Semakin tinggi → semakin besar kontribusi revenue
```

---

## RFM Segmentation

Project ini menggunakan segmentasi:

```text
Champions
Loyal Customers
Potential Loyalists
Need Attention
At Risk
Low Engagement
```

Aturan segmentasi yang digunakan:

```python
if r >= 4 and f >= 4 and m >= 4:
    "Champions"

elif f >= 4 and m >= 3:
    "Loyal Customers"

elif r >= 4 and f <= 3:
    "Potential Loyalists"

elif r <= 2 and f >= 3 and m >= 3:
    "At Risk"

elif r == 3 and f >= 2 and m >= 2:
    "Need Attention"

else:
    "Low Engagement"
```

### RFM Result

| Segment             | Customers | Sales Contribution |
| ------------------- | --------: | -----------------: |
| Champions           |     1.797 |          Rp57,01 M |
| Loyal Customers     |     1.376 |          Rp24,47 M |
| Potential Loyalists |     1.633 |          Rp12,13 M |
| Need Attention      |       703 |           Rp6,58 M |
| At Risk             |       376 |           Rp5,05 M |
| Low Engagement      |     3.776 |          Rp15,23 M |

### Insight

Segment **Champions** memberikan kontribusi sales terbesar, sekitar:

```text
Rp57,01 Miliar
```

atau sekitar:

```text
47,32%
```

dari total sales.

Segmentasi RFM dalam project ini bersifat **project-specific**, sehingga label seperti `Champions`, `At Risk`, dan `Loyal Customers` bergantung pada aturan scoring yang digunakan.

---

# Time Series Analysis

Sales dianalisis berdasarkan bulan.

Beberapa nilai monthly sales:

| Month     |     Sales |
| --------- | --------: |
| January   | Rp10,08 M |
| February  |  Rp8,93 M |
| March     |  Rp9,79 M |
| April     | Rp10,80 M |
| May       | Rp10,89 M |
| June      | Rp10,26 M |
| July      |  Rp9,80 M |
| August    |  Rp9,38 M |
| September | Rp10,58 M |
| October   | Rp10,01 M |
| November  | Rp10,15 M |
| December  |  Rp9,82 M |

Sales tertinggi terjadi pada:

```text
May
± Rp10,89 Miliar
```

Sales terendah terjadi pada:

```text
August
± Rp9,38 Miliar
```

### Important Note

Dataset ini hanya mencakup satu tahun sehingga perubahan bulanan sebaiknya disebut sebagai:

> monthly fluctuations

dan bukan langsung dianggap sebagai pola **seasonality tahunan**.

Untuk menyimpulkan seasonality dengan lebih kuat, diperlukan data dari beberapa tahun.

---

# Dashboard

Dashboard dibuat menggunakan **Streamlit**.

Dashboard menyediakan filter interaktif:

```text
Year
Date Range
Category
Gender
Province
Payment Method
```

---

## Dashboard Features

### Executive Summary

Menampilkan:

* Total Sales
* Total Orders
* Total Customers
* Total Quantity
* Average Order Value

---

### Sales Overview

Menampilkan:

* Monthly sales
* Sales trend
* Monthly growth
* Highest sales period

---

### Category Performance

Menampilkan:

* Sales by category
* Category contribution
* Category observation

---

### Order Performance

Menampilkan:

* Order status
* Completion rate
* Cancellation rate
* Return rate

---

### Payment Performance

Menampilkan:

* Sales by payment method
* Payment contribution

---

### Product Performance

Menampilkan:

* Top 10 products by sales
* Top 10 products by quantity

---

### Customer Analytics

Menampilkan:

* Purchase frequency
* Repeat customer
* One-time customer
* Top customers

---

### RFM Segmentation

Menampilkan:

* Customer segmentation
* Customer count by segment
* Sales by segment
* RFM observation

---

### Geographic Analysis

Menampilkan:

* Top provinces by sales

---

### Filtered Data

User dapat:

* Melihat data transaksi
* Mengeksplorasi hasil filter
* Download filtered dataset dalam format CSV

---

# Dashboard Preview

Tambahkan screenshot dashboard pada folder:

```text
images/dashboard.png
```

Kemudian tampilkan di README:

```markdown
![Dashboard Preview](images/dashboard.png)
```

Contoh:

![Dashboard Preview](images/dashboard.png)

---

# ▶How to Run

## 1. Clone Repository

```bash
git clone https://github.com/USERNAME/ecommerce-data-analytics.git
```

Masuk ke folder:

```bash
cd ecommerce-data-analytics
```

---

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Aktifkan:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
```

Aktifkan:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Jika belum memiliki `requirements.txt`:

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit
```

---

## 4. Run Streamlit

```bash
streamlit run app/app.py
```

Dashboard akan tersedia melalui browser.

---

# Requirements

Contoh isi `requirements.txt`:

```text
pandas
numpy
matplotlib
seaborn
plotly
streamlit
```

---

# 🧮 Important Analytical Considerations

Beberapa hal diperhatikan selama analisis agar hasil tidak misleading.

## Unique Orders

Karena satu order dapat memiliki beberapa baris produk, jumlah order dihitung menggunakan:

```python
df["order_id"].nunique()
```

bukan:

```python
len(df)
```

---

## Average Order Value

AOV dihitung menggunakan unique order:

```python
AOV = Total Sales / Unique Orders
```

Contoh:

```python
aov = total_sales / total_orders
```

---

## Order Status

Analisis status order menggunakan:

```python
groupby("order_status")["order_id"].nunique()
```

untuk menghindari penghitungan order yang sama lebih dari sekali.

---

## Repeat Customer

Repeat customer didefinisikan berdasarkan:

```text
jumlah unique order > 1
```

dalam periode dataset.

---

## RFM

RFM dihitung berdasarkan data yang sedang dianalisis dan menggunakan reference date:

```python
reference_date = (
    df["order_date"].max()
    + pd.Timedelta(days=1)
)
```

---

# Business Questions

Project ini mencoba menjawab beberapa pertanyaan bisnis:

### Sales

* Berapa total sales?
* Bagaimana perkembangan sales per bulan?
* Kapan sales tertinggi?
* Bagaimana perubahan sales antarperiode?

### Product

* Produk apa yang paling banyak menghasilkan sales?
* Produk apa yang paling banyak terjual?
* Apakah produk dengan quantity tinggi juga menghasilkan sales tinggi?

### Customer

* Berapa jumlah customer?
* Berapa banyak repeat customer?
* Bagaimana frekuensi pembelian customer?
* Customer mana yang memberikan kontribusi terbesar?

### RFM

* Siapa customer dengan recency tinggi?
* Siapa customer dengan frequency tinggi?
* Siapa customer dengan monetary value tinggi?
* Bagaimana distribusi customer berdasarkan segment?

### Transaction

* Metode pembayaran apa yang paling banyak menghasilkan sales?
* Bagaimana distribusi order status?
* Berapa cancellation rate?
* Berapa return rate?

### Geography

* Provinsi mana yang memiliki sales terbesar?
* Apakah wilayah dengan order terbanyak juga memiliki sales terbesar?

---

# Key Business Insights

Beberapa insight utama dari analisis:

### 1. Revenue didominasi kategori bernilai tinggi

Kategori Elektronik menjadi kontributor sales terbesar.

```text
± Rp79,3 Miliar
```

---

### 2. Quantity tidak selalu sama dengan revenue

Fashion Wanita memiliki quantity tinggi tetapi sales jauh lebih rendah dibanding Elektronik.

Hal ini menunjukkan pentingnya membedakan:

```text
Sales Volume
vs
Sales Value
```

---

### 3. Repeat customer memiliki kontribusi besar

Repeat customer:

```text
7.768 customers
```

berkontribusi sekitar:

```text
96,12%
```

dari total sales.

---

### 4. Customer frequency berhubungan dengan kontribusi sales

Customer dengan:

```text
7+ orders
```

berkontribusi sekitar:

```text
59,81%
```

dari total sales.

---

### 5. Champions memberikan kontribusi besar

Dalam segmentasi RFM project ini, Champions menyumbang:

```text
± Rp57,01 Miliar
```

atau:

```text
±47,32%
```

dari sales.

---

### 6. Sales bulanan mengalami fluktuasi

Sales tertinggi terjadi pada:

```text
May
```

sedangkan sales terendah:

```text
August
```

Namun data hanya mencakup satu tahun sehingga belum cukup untuk menyimpulkan seasonality tahunan.

---

# Future Improvements

Project ini masih dapat dikembangkan lebih lanjut.

## Dashboard

* [ ] Tambahkan reset filter dengan `st.session_state`
* [ ] Tambahkan KPI comparison
* [ ] Tambahkan date-over-date comparison
* [ ] Tambahkan customer lifetime analysis
* [ ] Tambahkan product profitability
* [ ] Tambahkan cohort analysis
* [ ] Tambahkan geographic map
* [ ] Tambahkan download report PDF
* [ ] Tambahkan automated business insights

---

## Machine Learning

Project dapat dikembangkan menuju predictive analytics:

### Sales Prediction

Memprediksi:

```text
Future Sales
```

menggunakan:

* Linear Regression
* Random Forest
* XGBoost
* Time Series Models

---

### Customer Churn Prediction

Memprediksi customer yang kemungkinan berhenti melakukan pembelian.

Features:

```text
Recency
Frequency
Monetary
Purchase Frequency
Average Order Value
```

---

### Customer Lifetime Value

Mengestimasi:

```text
Customer Lifetime Value
```

untuk mengetahui potensi nilai customer dalam jangka panjang.

---

### Product Recommendation

Mengembangkan:

```text
Recommendation System
```

berdasarkan:

* Purchase history
* Product similarity
* Customer behavior

---

# Skills Demonstrated

Project ini menunjukkan kemampuan dalam:

### Data Analysis

* Data Understanding
* Data Cleaning
* Exploratory Data Analysis
* Data Aggregation
* Statistical Analysis
* Business Analysis

### Python

* Pandas
* NumPy
* Functions
* Data transformation
* GroupBy
* Filtering
* Feature engineering

### Data Visualization

* Matplotlib
* Seaborn
* Plotly
* Interactive visualization

### Customer Analytics

* Customer segmentation
* Repeat customer analysis
* Purchase frequency
* RFM analysis

### Dashboard

* Streamlit
* Interactive filters
* KPI
* Business insights
* Data download

### Software Engineering

* Project structure
* Modular workflow
* Virtual environment
* Git
* GitHub

---

# Limitations

Beberapa keterbatasan project:

1. Dataset merupakan data historis sehingga hasil analisis bersifat deskriptif.
2. Dataset hanya mencakup satu tahun sehingga belum cukup untuk analisis seasonality multi-year.
3. RFM menggunakan aturan segmentasi yang dibuat khusus untuk project ini.
4. Repeat customer tidak otomatis berarti loyal customer.
5. Sales tidak sama dengan profit karena dataset tidak menyediakan seluruh komponen biaya bisnis.
6. Analisis geografis menggunakan lokasi customer dan bukan lokasi operasional perusahaan.
7. Tidak semua hubungan antarvariabel dapat dianggap sebagai hubungan sebab-akibat.

---

# Conclusion

Project **E-Commerce Sales & Customer Analytics** menunjukkan bagaimana data transaksi dapat diubah menjadi informasi yang lebih mudah dipahami melalui proses:

```text
Raw Data
    ↓
Cleaning
    ↓
Feature Engineering
    ↓
EDA
    ↓
Business Analysis
    ↓
Customer Segmentation
    ↓
Interactive Dashboard
```

Hasil analisis menunjukkan bahwa:

* Elektronik menjadi kontributor sales terbesar.
* Quantity tinggi tidak selalu menghasilkan revenue tinggi.
* Repeat customer memberikan kontribusi sales yang besar.
* Customer dengan frekuensi pembelian tinggi berkontribusi signifikan terhadap revenue.
* RFM dapat digunakan untuk memahami karakteristik customer.
* Sales mengalami fluktuasi antarbulan.
* Distribusi geografis memberikan perspektif tambahan mengenai pasar.

Project ini menjadi implementasi end-to-end dari proses **Data Analytics** menggunakan Python hingga dashboard interaktif.

---

### Skills

```text
Python
Pandas
NumPy
SQL
Data Analysis
Data Visualization
Machine Learning
Streamlit
Git & GitHub
```

---

# ⭐ Project Goal

Project ini dikembangkan sebagai bagian dari portfolio untuk menunjukkan kemampuan dalam:

> **Mengubah raw data menjadi insight bisnis yang dapat dipahami melalui proses analisis data yang sistematis dan dashboard interaktif.**

Jika project ini bermanfaat, jangan lupa memberikan ⭐ pada repository.

---
