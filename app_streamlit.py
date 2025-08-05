
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Monitoring Risiko Kelulusan", layout="wide")
st.title("Dashboard Monitoring Risiko Keterlambatan Kelulusan")

# Load Data Prediksi
df = pd.read_csv('hasil_prediksi_kelulusan.csv')

# Sidebar Filters
prodi = st.sidebar.multiselect("Pilih Program Studi", df['Prodi'].unique(), default=df['Prodi'].unique())
angkatan = st.sidebar.multiselect("Pilih Angkatan", df['Angkatan'].unique(), default=df['Angkatan'].unique())

# Filter Data
filtered_df = df[(df['Prodi'].isin(prodi)) & (df['Angkatan'].isin(angkatan))]

# Tabel Mahasiswa + Prediksi Risiko
st.subheader("Data Mahasiswa + Prediksi Risiko")
st.dataframe(filtered_df[['Nama Lengkap', 'NIM', 'Prediksi Kelulusan', 'Risiko (%)', 'Faktor Risiko']])

# Pie Chart Rasio Tepat Waktu vs Terlambat
st.subheader("Rasio Tepat Waktu vs Terlambat")
rasio = filtered_df['Prediksi Kelulusan'].value_counts().reset_index()
rasio.columns = ['Prediksi', 'Jumlah']
fig_pie = px.pie(rasio, names='Prediksi', values='Jumlah', color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig_pie, use_container_width=True)

# Top Faktor Risiko (Diambil dari Data Faktor Risiko)
st.subheader("Top Faktor Risiko")
faktor_df = filtered_df['Faktor Risiko'].value_counts().reset_index()
faktor_df.columns = ['Faktor', 'Jumlah']
fig_bar = px.bar(faktor_df, x='Jumlah', y='Faktor', orientation='h', color='Jumlah', color_continuous_scale='Viridis')
st.plotly_chart(fig_bar, use_container_width=True)
