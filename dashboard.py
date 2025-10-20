import pandas as pd
import streamlit as st
import pytz
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="📊 WhatsApp Tracker", layout="wide")
st_autorefresh(interval=10000, limit=None, key="refresh")

URL = "http://localhost:5000/dataframe"  # Ganti dengan Railway URL jika sudah deploy

try:
    response = requests.get(URL)
    data = response.json()
    df = pd.DataFrame(data)

    jakarta_tz = pytz.timezone('Asia/Jakarta')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert(jakarta_tz)
    df['tanggal'] = df['datetime'].dt.date
    df['jam'] = df['datetime'].dt.strftime('%H:%M:%S')

    st.title("📥 WhatsApp Message Dashboard")
    group = st.sidebar.selectbox("Pilih Grup", df['group_name'].dropna().unique())
    author = st.sidebar.selectbox("Pilih Pengirim", df[df['group_name'] == group]['author_name'].dropna().unique())

    filtered = df[(df['group_name'] == group) & (df['author_name'] == author)]

    st.metric("Jumlah Pesan", len(filtered))
    st.dataframe(filtered[['tanggal', 'jam', 'body']], use_container_width=True)
    st.bar_chart(filtered['tanggal'].value_counts().sort_index())
    st.caption(f"Terakhir update: {datetime.now(jakarta_tz).strftime('%Y-%m-%d %H:%M:%S WIB')}")

except Exception as e:
    st.error(f"Gagal ambil data: {e}")