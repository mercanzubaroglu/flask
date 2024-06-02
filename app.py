from flask import Flask, request, jsonify
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)

# Modeli yükle
model = joblib.load('stock_price_model.pkl')

# Tahmin fonksiyonu
def make_prediction(data, days):
    # data: Pandas DataFrame formatında olmalı
    # days: kaç günlük tahmin yapılacak
    future_dates = [datetime.today() + timedelta(days=i) for i in range(1, days+1)]
    predictions = model.predict(data)  # Modelinize göre bu kısmı düzenleyin
    return dict(zip(future_dates, predictions))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Excel dosyasını al
        file = request.files['file']
        data = pd.read_excel(file)
        
        # Tahmin yapmak istediğiniz gün sayısını al
        days = int(request.form.get('days', 7))
        
        # Tahminleri yap
        predictions = make_prediction(data, days)
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
