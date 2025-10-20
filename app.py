from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)
df_global = pd.DataFrame()

@app.route('/whatsapp', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)