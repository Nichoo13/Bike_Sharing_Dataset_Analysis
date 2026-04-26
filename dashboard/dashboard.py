import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(layout='wide', page_title='Analisis Data Bike Sharing')

st.title('Proyek Analisis Data: Bike Sharing Dataset')
st.markdown('### Oleh: Nicholas Noverhino Ama Payong')

# --- Data Loading ---
st.header('1. Gathering Data')

@st.cache_data
def load_data():
    try:
        # Membaca file lokal hour.csv
        df_hour = pd.read_csv("dashboard/hour.csv")
        df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
        return df_hour
    except FileNotFoundError:
        st.error("File 'hour.csv' tidak ditemukan. Pastikan file berada di folder yang sama dengan dashboard.py!")
        st.stop()

df_hour = load_data()
st.write("Data `df_hour` berhasil dimuat. Berikut 5 baris pertama:")
st.dataframe(df_hour.head())

# --- MEMBUAT SIDEBAR INTERAKTIF ---
st.sidebar.title("🚴‍♂️ Filter Data Rental")

min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

try:
    start_date, end_date = st.sidebar.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except ValueError:
    st.error("Pastikan Anda memilih tanggal awal dan tanggal akhir.")
    st.stop()

# --- FILTERING DATA UTAMA ---
# Sekarang kita gunakan main_df sebagai sumber data untuk SEMUA grafik di bawah
main_df = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                  (df_hour["dteday"] <= str(end_date))]

st.write(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# --- Visualisasi & Analisis Eksplanatori ---
st.header('2. Visualisasi & Analisis Eksplanatori')

# --- Pertanyaan 1: SMART Version ---
st.subheader('2.1. Pertanyaan Bisnis 1')
st.info("**Pertanyaan:** Bagaimana perbandingan pola penyewaan antara pengguna casual dan registered pada hari kerja dibandingkan hari libur selama tahun 2011-2012, untuk menentukan di hari apa perusahaan harus memfokuskan promosi keanggotaan (membership)?")

# Gunakan main_df agar grafik interaktif sesuai filter tanggal
df_question_1 = main_df[['casual', 'registered', 'workingday', 'holiday']].copy()

def jenis_hari(workingday, holiday):
    if workingday == 1 and holiday == 0:
        return 'Working Day'
    elif workingday == 0 and holiday == 1:
        return 'Holiday'
    else:
        return 'Non-Working Day'

df_question_1['jenis_hari'] = df_question_1.apply(lambda x: jenis_hari(x['workingday'], x['holiday']), axis=1)
df_question_1_grouped = df_question_1.groupby(by='jenis_hari')[['casual', 'registered']].sum()

fig1, ax1 = plt.subplots(figsize=(10, 6))
df_question_1_grouped.plot(kind='bar', ax=ax1, color=['skyblue', 'lightcoral'])

for container in ax1.containers:
    ax1.bar_label(container, fmt='%d', label_type='edge')

ax1.set_title('Jumlah Penyewaan Pengguna Berdasarkan Jenis Hari')
ax1.set_xlabel('Jenis Hari')
ax1.set_ylabel('Jumlah Penyewaan')
ax1.set_yticks([])
ax1.ticklabel_format(style='plain', axis='y')
ax1.legend(title='Jenis Pengguna')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig1)

st.markdown("""
**Insight Pertanyaan 1:**
- Berdasarkan data yang dipilih, jumlah penyewaan terbesar terjadi pada hari kerja (`Working Day`), yang sangat didominasi oleh pengguna `registered`.
- Pengguna `casual` memiliki proporsi yang cukup signifikan di hari non-kerja (akhir pekan/libur). 
- **Action Plan:** Hal ini menunjukkan bahwa akhir pekan adalah momen terbaik bagi tim pemasaran untuk menawarkan promosi keanggotaan kepada pengguna `casual`.
""")

# --- Pertanyaan 2: SMART Version ---
st.subheader('2.2. Pertanyaan Bisnis 2')
st.info("**Pertanyaan:** Bagaimana pengaruh kelembapan (hum) dan temperatur suhu (temp) terhadap jumlah penyewaan (cnt) di hari kerja selama periode 2011-2012, agar perusahaan dapat mengantisipasi lonjakan permintaan dengan menyiapkan stok maksimal?")

# Gunakan main_df agar grafik interaktif sesuai filter tanggal
df_question_2 = main_df[main_df['workingday'] == 1].copy()

# Plot: Suhu, Kelembapan, dan Jumlah Sewa (3 Variabel)
fig4, ax4 = plt.subplots(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df_question_2,
    x='temp',
    y='cnt',
    hue='hum',
    palette='viridis',
    alpha=0.8,
    edgecolor=None,
    ax=ax4
)
ax4.set_title('Pengaruh Suhu dan Kelembapan terhadap Penyewaan Sepeda (Hari Kerja)')
ax4.set_xlabel('Suhu Udara (temp) (Normalized)')
ax4.set_ylabel('Total Penyewaan (cnt)')
ax4.legend(title='Kelembapan (hum)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig4)

st.markdown("""
**Insight Pertanyaan 2:**
- Terlihat pola bahwa penyewaan mencapai puncak tertinggi saat suhu hangat (0.5 - 0.8) dan tingkat kelembapan udara yang rendah (titik berwarna biru/ungu).
- **Action Plan:** Manajer operasional harus memastikan seluruh stok sepeda tersedia 100% di stasiun saat kondisi cuaca ideal ini terdeteksi di prakiraan cuaca.
""")

st.header('3. Kesimpulan Akhir (Actionable)')
st.success("""
1. **Strategi Membership (Q1):** Perusahaan disarankan memfokuskan strategi promosi keanggotaan pada akhir pekan atau hari libur. Memberikan diskon pendaftaran *member* khusus di hari tersebut akan sangat efektif untuk menarik pengguna *casual* beralih menjadi pelanggan tetap (*registered*).
2. **Manajemen Stok (Q2):** Perusahaan harus menyiapkan stok sepeda maksimal saat suhu diprediksi hangat (0.5-0.8) dengan kelembapan rendah. Sebaliknya, saat cuaca diprediksi ekstrem atau kelembapan tinggi, perusahaan dapat menarik sebagian stok untuk jadwal pemeliharaan rutin guna efisiensi biaya.
""")
