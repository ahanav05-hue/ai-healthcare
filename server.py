from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('login.html')

# After login
@app.route('/login', methods=['POST'])
def login():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    return f"Prediction working! Data: {data}"

# IMPORTANT for Railway / deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # dynamic port
    app.run(host="0.0.0.0", port=port)