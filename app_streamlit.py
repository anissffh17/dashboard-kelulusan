import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Monitoring Risiko Kelulusan", layout="wide")
st.title("Dashboard Monitoring Risiko Keterlambatan Kelulusan")

# Load Data CSV
df = pd.read_csv('hasil_prediksi_kelulusan.csv')

# Debug: Tampilkan semua kolom CSV (biar kamu bisa lihat apa yang terbaca)
st.write("Kolom di CSV:", df.columns.tolist())

# Sidebar Filter (Opsional, Hanya kalau kolom ada)
if 'Asal Universitas' in df.columns:
    universitas = st.sidebar.multiselect("Pilih Universitas", df['Asal Universitas'].unique(), default=df['Asal Universitas'].unique())
    df = df[df['Asal Universitas'].isin(universitas)]

# Tampilkan Dataframe (dengan kolom yang ada saja)
target_cols = ['Nama Lengkap', 'NIM', 'Prediksi Kelulusan', 'Risiko (%)', 'Faktor Risiko']
display_cols = [col for col in target_cols if col in df.columns]

st.subheader("Data Mahasiswa + Prediksi Risiko")
st.dataframe(df[display_cols])

# Pie Chart: Tepat Waktu vs Terlambat (kalau kolom 'Prediksi Kelulusan' ada)
if 'Prediksi Kelulusan' in df.columns:
    st.subheader("Rasio Tepat Waktu vs Terlambat")
    rasio = df['Prediksi Kelulusan'].value_counts().reset_index()
    rasio.columns = ['Prediksi', 'Jumlah']
    fig_pie = px.pie(rasio, names='Prediksi', values='Jumlah', color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart Faktor Risiko (kalau kolom 'Faktor Risiko' ada)
if 'Faktor Risiko' in df.columns:
    st.subheader("Top Faktor Risiko")
    faktor_df = df['Faktor Risiko'].value_counts().reset_index()
    faktor_df.columns = ['Faktor', 'Jumlah']
    fig_bar = px.bar(faktor_df, x='Jumlah', y='Faktor', orientation='h', color='Jumlah', color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)
