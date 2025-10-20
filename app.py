from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

print("✅ Flask app initialized")

app = Flask(__name__)
df_global = pd.DataFrame(columns=["timestamp", "author_name", "message", "datetime", "tanggal", "jam"])

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    global df_global

    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validasi minimal
            if not all(k in data for k in ["timestamp", "author_name", "message"]):
                return "❌ Payload tidak lengkap", 400

            df = pd.DataFrame([data])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            df['tanggal'] = df['datetime'].dt.date
            df['jam'] = df['datetime'].dt.strftime('%H:%M:%S')

            df_global = pd.concat([df_global, df], ignore_index=True)
            return "✅ Data diterima dan disimpan", 200

        except Exception as e:
            return f"❌ Gagal parsing data: {e}", 400

    else:
        # GET: Kirim data ke dashboard
        return jsonify(df_global.to_dict(orient='records')), 200

@app.route('/dataframe', methods=['GET'])
def get_dataframe():
    global df_global
    return jsonify(df_global.to_dict(orient='records')), 200

@app.route('/ping')
def ping():
    return "pong", 200