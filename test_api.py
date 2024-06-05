import requests
import pandas as pd

# API'nin URL'si ve port numarası
url = 'http://10.117.50.61:5000/predict'

# Dosyadan veriyi okuma
file_path = "aselsan.xlsx"
data = pd.read_excel(file_path)

# Son fiyatı al
current_price = data.iloc[-1]['Kapanış(TL)']

# Hisse adını al (dosya adından)
hisse_adi = file_path.split('/')[-1].split('.')[0]

# Test verisi
test_data = {
    "hisse_adi": hisse_adi,
    "current_price": current_price
}

# POST isteği gönderme
response = requests.post(url, json=test_data)

# Yanıtı kontrol etme
if response.status_code == 200:
    predictions = response.json()
    print(f"\n{hisse_adi} hissesi için öneriler:")
    print("7 Günlük Tahmin: ", predictions['7_days'])
    print("30 Günlük Tahmin: ", predictions['30_days'])
    print("60 Günlük Tahmin: ", predictions['60_days'])
    print("90 Günlük Tahmin: ", predictions['90_days'])
    print("\nAl-Sat Önerileri:")
    for period, recommendation in predictions.items():
        print(f"{period} için öneri: {recommendation}")
else:
    print("API'ye istek gönderilirken bir hata oluştu. Hata kodu:", response.status_code)
