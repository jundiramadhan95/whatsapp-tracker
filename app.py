from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Hello from Railway!", 200

@app.route('/ping')
def ping():
    return "pong", 200