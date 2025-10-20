from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

print("✅ Flask app initialized")

app = Flask(__name__)
df_global = pd.DataFrame()

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    if request.method == 'POST':
        # Simpan data dari client
        return "✅ Data diterima", 200
    else:
        # Kirim data ke dashboard
        dummy_data = [
            {
                "time": "2023-06-06T08:15:00.000Z",
                "author_name": "admin",
                "message": "Halo dari server!"
            },
            {
                "time": "2023-06-06T08:16:00.000Z",
                "author_name": "user1",
                "message": "Siap!"
            }
        ]
        return jsonify(dummy_data), 200

def receive_message():
    global df_global
    data = request.json
    df = pd.DataFrame([data])

    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['tanggal'] = df['datetime'].dt.date
    df['jam'] = df['datetime'].dt.strftime('%H:%M:%S')

    df_global = pd.concat([df_global, df], ignore_index=True)
    return "OK", 200

@app.route('/dataframe', methods=['GET'])
def get_dataframe():
    global df_global
    return jsonify(df_global.to_dict(orient='records'))

@app.route('/ping')
def ping():
    return "pong", 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)