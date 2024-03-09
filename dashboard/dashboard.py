#Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#Menampilkan Judul
st.title("Air Quality Analysis")
st.title("(Analisis Kualitas Udara)")
st.subheader("oleh: M. Abdan Syakura")

# Menampilkan data
all_df = pd.read_csv("all_data.csv")

# Menampilkan Deskripsi
st.write("""Udara merupakan salah satu komponen penting yang menopang kehidupan makhluk hidup.
Udara mengandung berbagai partikel dan senyawa yang tidak terlihat oleh mata manusia.
Seiring dengan perkembangan industri, kualitas udara yang ada saat ini mulai mengalami polusi udara oleh berbagai polutan yang dapat membahayakan manusia.
Berikut merupakan analisis sederhana yang dilakukan untuk menunjukkan sudah seberapa tercemar udara yang ada di suatu wilayah berdasarkan dataset yang didapatkan.
Setelah membaca tulisan ini, pembaca diharapkan dapat menjawab beberapa pertanyaan berikut.
- Pertanyaan 1
    Bagaimana tren pencemaran udara yang terjadi dalam beberapa tahun terakhir?
- Pertanyaan 2
    Daerah mana yang memiliki tingkat polusi tertinggi?
- Pertanyaan 3
    Adakah faktor yang memengaruhi kenaikan temperatur secara signifikan?
""")
st.subheader("Data yang digunakan dalam analisis kualitas udara sebagai berikut.")
st.dataframe(all_df)

#Membagi bentuk polusi
particle_pollution = all_df[['PM2.5', 'PM10']].sum(axis=1)
gas_pollution = all_df[['NO2', 'CO', 'SO2', 'O3']].sum(axis=1)

all_df.insert(loc=12, column='particle_pollution', value=particle_pollution)
all_df.insert(loc=12, column='gas_pollution', value=gas_pollution)

# Menampilkan pilihan kolom untuk visualisasi pertanyaan bisnis
pembahasan = ["Tren Pencemaran Udara", "Daerah dengan Polusi Tertinggi", "Faktor yang Mempengaruhi Temperatur", "Conclusion"]
selected_column = st.selectbox("Pilih yang anda ingin bahas terlebih dahulu:", pembahasan)
if selected_column == "Tren Pencemaran Udara":
    pollution_df = all_df.groupby(by="year").agg({
    "particle_pollution" : "mean",
    "gas_pollution" : "mean"
    })

    st.subheader("Tren Pencemaran Udara per Tahun")
    #Menampilkan chart pada ax[0]
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    ax[0].plot(pollution_df.index, pollution_df["particle_pollution"], marker='o', linestyle='-', label='Polusi Partikel')
    ax[0].set_title('Grafik Polusi Partikel')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Rerata Polusi Partikel')
    ax[0].legend()

    #Menampilkan chart pada ax[1]
    ax[1].plot(pollution_df.index, pollution_df["gas_pollution"], marker='o', linestyle='-', label='Polusi Gas')
    ax[1].set_title('Grafik Polusi Gas')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Rerata Polusi Gas')
    ax[1].legend()

    # Menampilkan grafik
    plt.tight_layout()  # Menjaga jarak antar subplot agar rapi
    plt.show()
    st.pyplot(fig)
    st.write("""Berdasarkan dari grafik di atas, polusi partikel berbahaya melonjak dengan begitu tinggi pada periode tahun 2016 - 2017 dari sebelumnya turun secara signifikan dari tahun 2014 - 2016.
    Sedangkan, polusi gas berbahaya sangat melonjak di tahun 2017 melebihi tahun-tahun sebelumnya.""")

elif selected_column == "Daerah dengan Polusi Tertinggi":
    bystation_df = all_df.groupby(by="station").agg({
    "particle_pollution" : "mean",
    "gas_pollution" : "mean"
    })

    st.subheader("Daerah dengan Polusi Tertinggi (Particle Pollution)")
    fig, ax = plt.subplots(figsize=(14, 5))
    colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="particle_pollution", 
        y=bystation_df.index,
        data=bystation_df,
        hue=colors_,
        legend=False
    )
    ax.set_title("Tingkat polusi partikel (PM2.5, PM10) berdasarkan stasiun", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    plt.show()
    st.pyplot(fig)
    st.write("""Dari visual data di atas terlihat bahwa kota Gucheng merupakan kota dengan rata-rata polusi partikel tertinggi dibandingkan kota lainnya.""")

    bystation_df = all_df.groupby(by="station").agg({
    "particle_pollution" : "mean",
    "gas_pollution" : "mean"
    })

    st.subheader("Daerah dengan Polusi Tertinggi (Gas Pollution)")
    fig, ax = plt.subplots(figsize=(14, 5))
    colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
    sns.barplot(
        x="gas_pollution", 
        y=bystation_df.index,
        data=bystation_df,
        hue=colors_,
        legend=False
    )
    ax.set_title("Tingkat polusi gas (SO2, NO2, CO, O3) berdasarkan stasiun", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    plt.show()
    st.pyplot(fig)
    st.write("""Dari visual data di atas terlihat bahwa kota Wanshouxigong merupakan kota dengan rata-rata polusi gas tertinggi dibandingkan kota lainnya.""")

elif selected_column == "Faktor yang Mempengaruhi Temperatur":
    # Buat visualisasi untuk menentukan korelasi temperature dengan parameter lainnya
    st.subheader("Faktor yang Mempengaruhi Temperatur")
    correlation_matrix = all_df[["TEMP", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
    ax.set_title('Korelasi antara Temperature dengan Parameter Kualitas Udara')
    plt.show()
    st.pyplot(fig)
    st.write("""Berdasarkan visualisasi tersebut, temperature dipengaruhi secara signifikan oleh kandungan O3 dengan korelasi positif.""")

elif selected_column == "Conclusion":
    st.write("""- Conclusion pertanyaan 1: Tren pencemaran udara dalam beberapa tahun terakhir menunjukkan terjadinya lonjakan yang begitu besar baik dari polusi partikel maupun gas, terutama lonjakan polusi gas di tahun 2017 yang memecahkan rekor tertinggi dari tahun-tahun sebelumnya.
- Conclution pertanyaan 2:
Berdasarkan hasil di atas, dapat dilihat bahwa produksi polusi partikel berbahaya paling banyak berada di kota Gucheng disusul oleh kota Wanshouxigong dan Dongsi. Sedangkan, kota dengan penghasil polusi gas terbanyak yaitu kota Wanshouxigong. Data ini dapat dipakai dalam menentukan kebijakan kota untuk mengurangi produksi polusi.
- Conclusion pertanyaan 3: Kenaikan temperatur yang terjadi dipengaruhi oleh kandungan O3 dengan korelasi positif sebesar 59%. Sedangkan, kandungan parameter lainnya justru berkorelasi negatif dan tidak berpengaruh secara signifikan.
""")

