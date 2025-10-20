import pandas as pd
import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Whatsapp Tracker", layout="wide")
st.title("📲 Whatsapp Tracker Dashboard")

# Auto-refresh setiap 10 detik, maksimal 100 kali
st_autorefresh(interval=10000, limit=100, key="data_refresh")

url = "https://whatsapp-tracker-production.up.railway.app/whatsapp"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Parsing data
    jam, tanggal, author_name, message = [], [], [], []

    for i in data:
        try:
            dt = pd.to_datetime(i.get("datetime") or i.get("timestamp"), errors="coerce")
            if pd.isna(dt):
                continue
            jam.append(dt.strftime("%H:%M:%S"))
            tanggal.append(dt.strftime("%Y-%m-%d"))
            jam.append(dt.strftime("%H:%M:%S"))
            tanggal.append(dt.strftime("%Y-%m-%d"))
            author_name.append(i.get("author_name", "Unknown"))
            message.append(i.get("message", ""))
        except Exception:
            continue

    df = pd.DataFrame({
        "Jam": jam,
        "Tanggal": tanggal,
        "Author Name": author_name,
        "Message": message
    })

    # Total pesan per author
    st.subheader("📊 Total Message per Author")
    total_message = df.groupby("Author Name")["Message"].count().reset_index()
    total_message.columns = ["Author Name", "Total Message"]
    st.dataframe(total_message)

    # Filter dinamis
    st.subheader("🔍 Filtered Message")
    selected_date = st.selectbox("Pilih Tanggal", sorted(df["Tanggal"].unique(), reverse=True))
    selected_author = st.selectbox("Pilih Author", sorted(df["Author Name"].unique()))
    filtered_df = df[(df["Tanggal"] == selected_date) & (df["Author Name"] == selected_author)]
    st.dataframe(filtered_df)

except Exception as e:
    st.error(f"❌ Gagal ambil data: {e}")