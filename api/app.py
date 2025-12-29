from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import io

app = Flask(__name__)
CORS(app)

# Globals
model = LinearRegression()
df = None
trained = False


def train_model():
    global df, trained

    df = pd.read_csv('Table data.csv')
    df = df[df['Video title'] != 'Total']

    X = df[['Duration']]
    y = df['Views']

    model.fit(X, y)
    trained = True


# 🔹 Auto-train on startup
train_model()


@app.route('/predict', methods=['POST'])
def predict():
    if not trained:
        return jsonify({"error": "Model not trained"}), 400

    data = request.get_json()
    duration = data.get('duration')

    if duration is None:
        return jsonify({"error": "duration required"}), 400

    prediction = model.predict(
        pd.DataFrame([[duration]], columns=['Duration'])
    )

    return jsonify({
        "duration": duration,
        "predicted_views": int(prediction[0])
    })


@app.route('/plot', methods=['GET'])
def plot():
    if not trained:
        return jsonify({"error": "Model not trained"}), 400

    X = df[['Duration']]
    y = df['Views']

    x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_trend = model.predict(pd.DataFrame(x_range, columns=['Duration']))

    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df, x='Duration', y='Views', alpha=0.5)
    plt.plot(x_range, y_trend, color='red', linewidth=2)

    plt.title('How the AI Sees Your YouTube Data')
    plt.xlabel('Video Length (seconds)')
    plt.ylabel('Total Views')
    plt.grid(True, linestyle='--', alpha=0.6)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return send_file(img, mimetype='image/png')


@app.route('/')
def health():
    return jsonify({"status": "API running"})


if __name__ == '__main__':
    app.run(debug=True)
