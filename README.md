# 🚲 Proyek Analisis Data: Bike Sharing Dashboard

## Deskripsi Proyek
Proyek ini merupakan *dashboard* interaktif yang dibangun menggunakan **Streamlit** untuk menganalisis data penyewaan sepeda (Bike Sharing Dataset). Analisis ini berfokus pada dua pertanyaan bisnis utama:
1. Bagaimana perbandingan pola penyewaan antara pengguna *casual* dan *registered* pada hari kerja dibandingkan hari libur?
2. Bagaimana pengaruh kondisi cuaca (suhu dan kelembapan) terhadap jumlah penyewaan sepeda di hari kerja?

## Struktur File
- `app.py`: File utama yang berisi kode aplikasi Streamlit.
- `hour.csv`: Dataset mentah yang digunakan untuk analisis.
- `requirements.txt`: Daftar *library* Python beserta versinya yang dibutuhkan untuk menjalankan proyek ini.

## Setup Environment (Terminal / Command Prompt)

Sangat disarankan untuk menjalankan proyek ini di dalam *virtual environment* Python agar *library* yang diinstal tidak mengganggu proyek Anda yang lain.

```bash
# 1. Buka terminal dan arahkan ke direktori proyek Anda
cd path/to/your/project/folder

# 2. Buat virtual environment (Opsional, tapi sangat disarankan)
python -m venv env

# 3. Aktifkan virtual environment
# Untuk pengguna Windows:
.\env\Scripts\activate
# Untuk pengguna Mac/Linux:
source env/bin/activate

# 4. Install semua library yang dibutuhkan
pip install -r requirements.txt

# 5 Jika sudah, silahkan run kode di bawah ini
streamlit run dashboard.py