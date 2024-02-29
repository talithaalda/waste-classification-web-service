import requests

# URL Flask API
url = 'http://127.0.0.1:5000/predict'

# Path ke gambar yang ingin Anda prediksi
image_path = 'E:/OneDrive - Universitas Airlangga/UNAIR/Semester 7/Skripsi/flaskApiDeploy/trash.jpg'

# Kirim permintaan POST dengan gambar
files = {'image': open(image_path, 'rb')}
response = requests.post(url, files=files)

# Tampilkan respons dari server
print(response.json())
