
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

# MENGGUNAKAN CARA LOKAL (Jauh lebih aman dan cepat untuk Streamlit)
@st.cache_data 
def load_data():
    try:
        # Pastikan file hour.csv ada di folder yang sama dengan app.py
        df_hour = pd.read_csv("hour.csv")
        df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
        return df_hour
    except FileNotFoundError:
        st.error("File 'hour.csv' tidak ditemukan. Pastikan file sudah di-upload ke folder yang sama dengan app.py!")
        st.stop()

df_hour = load_data()
st.write("Data `df_hour` berhasil dimuat. Berikut 5 baris pertama:")
st.dataframe(df_hour.head())


# --- Visualisasi & Analisis Eksplanatori ---
st.header('2. Visualisasi & Analisis Eksplanatori')

# --- Pertanyaan 1 ---
st.subheader('2.1. Pertanyaan 1: Perbandingan Pola Penyewaan (Casual vs Registered) pada Hari Kerja/Libur')

df_question_1 = df_hour[['casual', 'registered', 'workingday', 'holiday']].copy()

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

ax1.set_title('Jumlah Penyewaan Pengguna Berdasarkan Jenis Hari pada Tahun 2011-2012')
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
- Jumlah penyewaan terbesar terjadi pada hari kerja (`Working Day`), didominasi oleh pengguna `registered`.
- Pengguna `registered` menunjukkan pola penyewaan yang sangat tinggi di hari kerja (lebih dari 1.9 juta) dibandingkan hari libur atau non-working day.
- Pengguna `casual` memiliki jumlah penyewaan yang relatif lebih merata di semua jenis hari, namun puncaknya tetap di hari kerja, diikuti oleh non-working day.
- Ini menyiratkan bahwa strategi bisnis dapat difokuskan pada peningkatan layanan untuk pengguna `registered` selama hari kerja, dan mungkin promosi untuk pengguna `casual` di hari non-kerja.
""")

# --- Pertanyaan 2 ---
st.subheader('2.2. Pertanyaan 2: Pengaruh Kelembapan (hum) dan Suhu (temp) terhadap Jumlah Penyewaan (cnt) di Hari Kerja')

df_question_2 = df_hour[df_hour['workingday'] == 1].copy()

# Plot 1: Suhu vs Jumlah Sewa
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=df_question_2,
    x='temp',
    y='cnt',
    scatter_kws={'alpha': 0.6, 'color': 'dodgerblue'},
    line_kws={'color': 'red', 'linewidth': 2},
    order=2,
    ax=ax2
)
ax2.set_title('Hubungan Suhu (temp) dan Jumlah Penyewaan (cnt) di Hari Kerja')
ax2.set_xlabel('Suhu Udara (temp) (Normalized)')
ax2.set_ylabel('Total Penyewaan (cnt)')
plt.tight_layout()
st.pyplot(fig2)

st.markdown("""
**Insight (Suhu vs. Penyewaan):**
- Terdapat korelasi positif antara suhu udara dan jumlah penyewaan; semakin tinggi suhu, semakin banyak penyewaan.
""")

# Plot 2: Kelembapan vs Jumlah Sewa
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=df_question_2,
    x='hum',
    y='cnt',
    scatter_kws={'alpha': 0.6, 'color': 'dodgerblue'},
    line_kws={'color': 'red', 'linewidth': 2},
    order=2,
    ax=ax3
)
ax3.set_title('Hubungan Kelembapan (hum) dan Jumlah Penyewaan (cnt) di Hari Kerja')
ax3.set_xlabel('Kelembapan Udara (hum) (Normalized)')
ax3.set_ylabel('Total Penyewaan (cnt)')
plt.tight_layout()
st.pyplot(fig3)

st.markdown("""
**Insight (Kelembapan vs. Penyewaan):**
- Terdapat korelasi negatif antara kelembapan udara dan jumlah penyewaan; semakin tinggi kelembapan, semakin sedikit penyewaan.
""")

# Plot 3: Suhu, Kelembapan, dan Jumlah Sewa
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
ax4.set_title('Pengaruh Suhu dan Kelembapan terhadap Penyewaan Sepeda di Hari Kerja')
ax4.set_xlabel('Suhu Udara (temp) (Normalized)')
ax4.set_ylabel('Total Penyewaan (cnt)')
ax4.legend(title='Kelembapan (hum)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig4)

st.markdown("""
**Insight (Suhu, Kelembapan, dan Penyewaan):**
- Jumlah penyewaan tertinggi (>800) terjadi saat suhu berada di rentang 0.5-0.8 (hangat) dan kelembapan rendah (warna biru/ungu pada plot).
- Saat suhu ekstrem (sangat rendah atau sangat tinggi) atau kelembapan tinggi (warna kuning), jumlah penyewaan cenderung menurun.
- Ini menunjukkan preferensi penyewa terhadap cuaca hangat dengan kelembapan rendah untuk aktivitas bersepeda.
""")

st.header('3. Kesimpulan')
st.markdown("""
- **Kesimpulan untuk Pertanyaan 1:** Perusahaan rental sepeda harus memaksimalkan operasional pada hari kerja, terutama untuk pengguna terdaftar (*registered*), karena hari kerja menyumbang sebagian besar penyewaan. Potensi diskon bisa diterapkan pada hari libur untuk menarik lebih banyak pengguna kasual.
- **Kesimpulan untuk Pertanyaan 2:** Cuaca hangat dengan kelembapan rendah adalah kondisi ideal untuk penyewaan sepeda. Perusahaan dapat melakukan efisiensi operasional (misalnya, pemeliharaan sepeda) saat prakiraan cuaca menunjukkan suhu ekstrem atau kelembapan tinggi yang cenderung menurunkan permintaan.
""")
