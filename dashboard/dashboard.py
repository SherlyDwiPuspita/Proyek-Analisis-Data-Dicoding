import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya untuk seaborn
sns.set(style='darkgrid')

# Fungsi untuk memuat dataset
def load_dataset():
    day_data = pd.read_csv('dashboard/day_df.csv')
    hour_data = pd.read_csv('dashboard/hour_df.csv')
    return day_data, hour_data

day_data, hour_data = load_dataset()

# Fungsi untuk menyiapkan kolom 'dateday' untuk pemrosesan data tanggal
def setup_date_column(dataframe):
    if 'dateday' in dataframe.columns:
        dataframe['dateday'] = pd.to_datetime(dataframe['dateday'])
    elif {'year', 'month', 'day'}.issubset(dataframe.columns):
        dataframe['dateday'] = pd.to_datetime(dataframe[['year', 'month', 'day']])
    else:
        st.error("Kolom 'dateday' atau kolom lain yang diperlukan untuk membuat tanggal tidak ditemukan.")
    return dataframe

day_data = setup_date_column(day_data)

with st.sidebar:
    # Menampilkan gambar di sidebar
    st.image("https://raw.githubusercontent.com/SherlyDwiPuspita/Proyek-Analisis-Data-Dicoding/main/assets/bike.jpg")

# Sidebar untuk memilih rentang tanggal
st.sidebar.title('🗓️ Pilih Rentang Tanggal')
start_date_input = st.sidebar.date_input("Tanggal Awal", pd.to_datetime('2011-01-01'))
end_date_input = st.sidebar.date_input("Tanggal Akhir", pd.to_datetime('2012-12-31'))

# Menyaring dataset berdasarkan rentang tanggal yang dipilih
def filter_by_date(dataframe, start_date, end_date):
    filtered_dataframe = dataframe[(dataframe['dateday'] >= pd.to_datetime(start_date)) & (dataframe['dateday'] <= pd.to_datetime(end_date))]
    return filtered_dataframe

filtered_day_data = filter_by_date(day_data, start_date_input, end_date_input)

# Judul utama halaman
st.title('Analisis Penyewaan Sepeda: Pola Penggunaan, Pengaruh Cuaca, dan Tren Musiman')

# Mendapatkan informasi penyewaan sepeda berdasarkan tanggal yang dipilih
def retrieve_rent_info(dataframe):
    total_bike_rentals = dataframe['count'].sum()
    total_registered_users = dataframe['registered'].sum()
    total_casual_users = dataframe['casual'].sum()
    return total_bike_rentals, total_registered_users, total_casual_users

total_bike_rentals, total_registered_users, total_casual_users = retrieve_rent_info(filtered_day_data)

# Mengatur tampilan metrik penyewaan sepeda dalam tiga kolom
col1, col2, col3 = st.columns(3)

# Menampilkan informasi metrik untuk total penyewaan, pengguna terdaftar, dan pengguna biasa
col1.metric(label="Total Penyewaan Sepeda", value=f"{total_bike_rentals:,}")
col2.metric(label="Pengguna Terdaftar", value=f"{total_registered_users:,}")
col3.metric(label="Pengguna Biasa", value=f"{total_casual_users:,}")

# Menambahkan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi penggunaan sepeda per jam
st.header('Pola Penyewaan Sepeda pada Hari Libur dan Hari Kerja')

# Fungsi untuk memvisualisasikan distribusi penyewaan sepeda berdasarkan jam
def visualize_usage(hour_dataframe):
    # Membuat grup berdasarkan hari libur dan hari kerja
    day_data['holiday'] = day_data['holiday'].astype('category')
    day_data['workingday'] = day_data['workingday'].astype('category')

    # Membuat plot untuk membandingkan jumlah pengguna sepeda pada hari libur dan hari kerja
    plt.figure(figsize=(10,6))
    sns.set_style('whitegrid')
    sns.lineplot(x='dateday', y='count', hue='holiday', data=day_data, palette=['#000000', '#FFD700'])
    plt.title('Pola Penggunaan Sepeda pada Hari Libur dan Hari Kerja', fontsize=18)
    plt.xlabel('Tanggal', fontsize=14)
    plt.ylabel('Jumlah Pengguna Sepeda', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Hari Libur/Hari Kerja', fontsize=12)
    plt.show()
    st.pyplot(plt)

visualize_usage(hour_data)

# Menambahkan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi perbandingan pengguna terdaftar dan biasa
st.header('Penyewaan Sepeda Berdasarkan Cuaca')

# Fungsi untuk memvisualisasikan perbandingan jumlah pengguna biasa dan terdaftar per tahun
def weather_influence(dataframe):
    # Membuat grup berdasarkan cuaca
    day_data['weathersit'] = day_data['weathersit'].astype('category')

    # Menghitung rata-rata jumlah pengguna sepeda untuk setiap kategori cuaca
    weathersit_mean = day_data.groupby('weathersit')['count'].mean().reset_index()

    # Membuat plot bar chart
    plt.figure(figsize=(9, 8))
    sns.barplot(x='weathersit', y='count', data=weathersit_mean, color='#FFD700')  # Mengatur warna bar menjadi kuning
    plt.title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    plt.xlabel('Cuaca', fontsize=14)
    plt.ylabel('Jumlah Pengguna Sepeda', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
    st.pyplot(plt)

weather_influence(day_data)

# Menambahkan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi tren penyewaan sepeda
st.header('Tren Penyewaan Sepeda')

# Fungsi untuk memvisualisasikan tren penyewaan sepeda berdasarkan bulan dan tahun
def visualize_monthly_rentals_with_multiple_lines(dataframe):
    monthly_rentals_data = dataframe.groupby(['year', 'month'])['count'].sum().reset_index()
    monthly_rentals_data['month'] = pd.Categorical(monthly_rentals_data['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

    unique_years = monthly_rentals_data['year'].unique()
    total_years = len(unique_years)
    fig, axes = plt.subplots(total_years, 1, figsize=(10, 6), sharex=True)

    # Menentukan warna untuk setiap tahun
    colors = ['#FFD700', '#000000']  # Kuning dan Hitam

    for i, year in enumerate(unique_years):
        yearly_data = monthly_rentals_data[monthly_rentals_data['year'] == year]
        
        # Mengatur warna untuk setiap tahun, bergantian antara kuning dan hitam
        sns.lineplot(ax=axes[i], x='month', y='count', data=yearly_data, marker='o', color=colors[i % len(colors)])
        
        axes[i].set_title(f'Jumlah Penyewaan Sepeda di Tahun {year}', fontsize=14)
        axes[i].set_ylabel('Jumlah Penyewaan', fontsize=12)
        axes[i].grid(True)

    axes[-1].set_xlabel('Bulan', fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

visualize_monthly_rentals_with_multiple_lines(day_data)

# Menambahkan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi penyewaan sepeda berdasarkan musim
st.header('Penyewaan Sepeda Berdasarkan Musim')

# Fungsi untuk memvisualisasikan distribusi penyewaan sepeda berdasarkan musim
def visualize_seasonal_rentals(dataframe):
    # Data penyewaan sepeda berdasarkan musim
    seasonal_counts = pd.Series({
        'Musim Gugur': 1061129,
        'Musim Panas': 918589,
        'Musim Dingin': 841613,
        'Musim Semi': 471348
    }).sort_values(ascending=False)

    # Membuat figure dan axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menentukan gradasi warna kuning
    colors = ['#FFF9C4', '#FFEB3B', '#FBC02D', '#F57F20']  # Gradasi kuning dari terang ke gelap

    # Membuat pie chart
    ax.pie(seasonal_counts, labels=seasonal_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
    ax.axis('equal')  # Untuk membuat pie chart bulat
    plt.tight_layout()

    # Menampilkan plot dengan Streamlit
    st.pyplot(fig)

visualize_seasonal_rentals(day_data)

# Menambahkan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk analisis RFM (Recency, Frequency, Monetary)
st.header('Analisis RFM')

def create_rfm_df(df):
    df['Recency'] = (df['dateday'].max() - df['dateday']).dt.days
    frequency_df = df.groupby('dateday').agg({'count': 'sum'}).reset_index()
    frequency_df.rename(columns={'count': 'Frequency'}, inplace=True)
    df['Monetary'] = df['registered'] + df['casual']
    rfm_df = df[['dateday', 'Recency', 'Monetary']].merge(frequency_df, on='dateday', how='left')
    return rfm_df

rfm_df = create_rfm_df(filtered_day_data)

# Membuat visualisasi untuk Recency, Frequency, dan Monetary menggunakan line chart
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 8))  # Ukuran diperbesar
colors = ["#F57F20"]
title_fontsize = 30  # Ukuran font judul
label_fontsize = 24  # Ukuran font label sumbu

# Plot untuk Recency
sns.lineplot(x="dateday", y="Recency", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), marker='o', color=colors[0], ax=ax[0])
ax[0].set_title("Recency", fontsize=title_fontsize, loc="center")
ax[0].set_ylabel("Days", fontsize=label_fontsize)
ax[0].tick_params(labelsize=20)  # Ukuran font untuk tick
ax[0].tick_params(axis='x', rotation=45)  # Miringkan label sumbu x 45 derajat

# Plot untuk Frequency
sns.lineplot(x="dateday", y="Frequency", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), marker='o', color=colors[0], ax=ax[1])
ax[1].set_title("Frequency", fontsize=title_fontsize, loc="center")
ax[1].set_ylabel("Counts", fontsize=label_fontsize)
ax[1].tick_params(labelsize=20)  # Ukuran font untuk tick
ax[1].tick_params(axis='x', rotation=45)  # Miringkan label sumbu x 45 derajat

# Plot untuk Monetary
sns.lineplot(x="dateday", y="Monetary", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), marker='o', color=colors[0], ax=ax[2])
ax[2].set_title("Monetary", fontsize=title_fontsize, loc="center")
ax[2].set_ylabel("Total Users", fontsize=label_fontsize)
ax[2].tick_params(labelsize=20)  # Ukuran font untuk tick
ax[2].tick_params(axis='x', rotation=45)  # Miringkan label sumbu x 45 derajat

plt.tight_layout()
st.pyplot(fig)

# Mengakhiri aplikasi Streamlit
if __name__ == '__main__':
    st.write("Terima kasih telah menggunakan aplikasi ini!")

# Menambahkan catatan copyright di akhir halaman
st.caption('Copyright (c) Sherly Dwi Puspita 2024')
