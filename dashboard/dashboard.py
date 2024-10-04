import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur style untuk seaborn
sns.set(style='dark')

# Memuat dataset
def load_data():
    day_df = pd.read_csv('dashboard/day_df.csv')
    hour_df = pd.read_csv('dashboard/hour_df.csv')
    return day_df, hour_df

day_df, hour_df = load_data()

# Menyiapkan kolom 'dateday' untuk pengolahan data berdasarkan tanggal
def prepare_date_column(df):
    if 'dateday' in df.columns:
        df['dateday'] = pd.to_datetime(df['dateday'])
    elif {'year', 'month', 'day'}.issubset(df.columns):
        df['dateday'] = pd.to_datetime(df[['year', 'month', 'day']])
    else:
        st.error("Tidak ditemukan kolom 'dateday', atau kolom lain yang memungkinkan pembentukan tanggal.")
    return df

day_df = prepare_date_column(day_df)

with st.sidebar:
    # Menambahkan gambar di sidebar
    st.image("https://raw.githubusercontent.com/SherlyDwiPuspita/Proyek-Analisis-Data-Dicoding/main/assets/bike.jpg")

# Sidebar untuk pemilihan periode waktu
st.sidebar.title('🗓️ Pilih Periode Waktu')
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", pd.to_datetime('2011-01-01'))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime('2012-12-31'))

# Menyaring dataset berdasarkan periode waktu yang dipilih
def filter_data_by_date(df, start_date, end_date):
    filtered_df = df[(df['dateday'] >= pd.to_datetime(start_date)) & (df['dateday'] <= pd.to_datetime(end_date))]
    return filtered_df

filtered_day_df = filter_data_by_date(day_df, start_date, end_date)

# Membuat judul utama halaman
st.title('Bike Sharing Analysis 🚴')

# Mengambil informasi terkait penyewaan sepeda berdasarkan tanggal yang dipilih
def get_rent_info(df):
    total_rentals = df['count'].sum()
    total_registered = df['registered'].sum()
    total_casual = df['casual'].sum()
    return total_rentals, total_registered, total_casual

total_rentals, total_registered, total_casual = get_rent_info(filtered_day_df)

# Menyusun tampilan metrik penyewaan sepeda dalam 3 kolom
col1, col2, col3 = st.columns(3)

# Menampilkan informasi metrik untuk total penyewaan, pengguna registered, dan casual
col1.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,}")
col2.metric(label="Pengguna Registered", value=f"{total_registered:,}")
col3.metric(label="Pengguna Casual", value=f"{total_casual:,}")

# Memberikan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi penggunaan sepeda per jam
st.header('Distribusi Penggunaan Sepeda per Jam')

# Membuat visualisasi distribusi penyewaan sepeda berdasarkan jam
def plot_usage_by_hour(hour_df):
    plt.figure(figsize=(12, 6))
    sns.barplot(x='hr', y='count', data=hour_df, palette='GnBu', ci=None)
    plt.title('Distribusi Jumlah Pengguna Sepeda per Jam', fontsize=16)
    plt.xlabel('Jam (dalam 24 jam)', fontsize=14)
    plt.ylabel('Jumlah Pengguna (per jam)', fontsize=14)
    plt.ylim(0, 500)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

plot_usage_by_hour(hour_df)

# Memberikan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi perbandingan pengguna registered dan casual
st.header('Perbandingan Pengguna Casual vs Registered')

# Membuat visualisasi perbandingan jumlah pengguna casual dan registered per tahun
def plot_user_type_comparison(df):
    total_users = df.groupby(by='year').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()
    total_users = pd.melt(total_users, id_vars='year', value_vars=['registered', 'casual'], var_name='User Type', value_name='Count')

    plt.figure(figsize=(10, 6))
    sns.barplot(x='year', y='Count', hue='User Type', data=total_users, palette='GnBu')
    plt.title('Total Pengguna Registered dan Casual per Tahun', fontsize=16)
    plt.xlabel('Tahun', fontsize=14)
    plt.ylabel('Jumlah Pengguna', fontsize=14)
    plt.legend(title='Tipe Pengguna')
    plt.grid(axis='y')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout()
    st.pyplot(plt)

plot_user_type_comparison(day_df)

# Memberikan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi tren penyewaan sepeda
st.header('Trend Penyewaan Sepeda')

# Membuat visualisasi tren penyewaan sepeda berdasarkan bulan dan tahun
def plot_monthly_rentals(df):
    monthly_rentals = df.groupby(['year', 'month'])['count'].sum().reset_index()

    # Mengatur urutan bulan agar visualisasi lebih rapi
    monthly_rentals['month'] = pd.Categorical(monthly_rentals['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    plt.figure(figsize=(10, 6))

    # Membuat lineplot untuk menunjukkan tren penyewaan berdasarkan bulan dan tahun
    custom_palette = ['#66c2a5', '#91bfdb']
    sns.lineplot(x='month', y='count', hue='year', data=monthly_rentals, marker='o', palette=custom_palette)

    plt.title('Jumlah Total Sepeda yang Disewakan Berdasarkan Bulan dan Tahun', fontsize=16)
    plt.xlabel('Bulan', fontsize=14)
    plt.ylabel('Jumlah Penyewaan', fontsize=14)
    plt.grid(True)
    plt.legend(title='Tahun', loc='upper right')
    plt.tight_layout()
    st.pyplot(plt)

plot_monthly_rentals(day_df)

# Memberikan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk visualisasi penyewaan sepeda berdasarkan musim
st.header('Penyewaan Sepeda Berdasarkan Musim')

# Membuat visualisasi distribusi penyewaan sepeda berdasarkan musim
def plot_season_rentals(df):
    season_counts = pd.Series({
        'Fall': 1061129,
        'Summer': 918589,
        'Winter': 841613,
        'Spring': 471348
    }).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    palette_colors = ['#d7e7ff', '#b3d1ff', '#b3d1ff', '#b3d1ff']
    bars = sns.barplot(x=season_counts.index, y=season_counts.values, palette=palette_colors, ax=ax)

    highest_season = season_counts.idxmax()
    for i, bar in enumerate(bars.patches):
        if season_counts.index[i] == highest_season:
            bar.set_facecolor('#ff4c4c')

    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    y_ticks = ax.get_yticks().astype(int)
    ax.set_yticklabels([f'{int(y):,}' for y in y_ticks])
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

plot_season_rentals(day_df)

# Memberikan spasi tambahan antar elemen visual
st.write("")
st.write("")

# Membuat header untuk analisis RFM (Recency, Frequency, Monetary)
st.header('Analisis RFM')

# Membuat dataframe penyewaan sepeda registered per hari
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Membuat dataframe penyewaan sepeda berdasarkan musim
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

daily_registered_rent_df = create_daily_registered_rent_df(filtered_day_df)
season_rent_df = create_season_rent_df(filtered_day_df)

# Membuat dataframe untuk analisis RFM
def create_rfm_df(df):
    df['Recency'] = (df['dateday'].max() - df['dateday']).dt.days
    frequency_df = df.groupby('dateday').agg({'count': 'sum'}).reset_index()
    frequency_df.rename(columns={'count': 'Frequency'}, inplace=True)
    df['Monetary'] = df['registered'] + df['casual']
    rfm_df = df[['dateday', 'Recency', 'Monetary']].merge(frequency_df, on='dateday', how='left')
    return rfm_df

rfm_df = create_rfm_df(filtered_day_df)

# Membuat visualisasi untuk Recency, Frequency, dan Monetary
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4"] * 5

sns.barplot(y="Recency", x="dateday", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_title("Recency", loc="center", fontsize=18)
sns.barplot(y="Frequency", x="dateday", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_title("Frequency", loc="center", fontsize=18)
sns.barplot(y="Monetary", x="dateday", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_title("Monetary", loc="center", fontsize=18)

st.pyplot(fig)

# Menambahkan catatan copyright di akhir halaman
st.caption('Copyright (c) Sherly Dwi Puspita 2024')
