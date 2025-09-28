import requests

vaga_id = "ac54c921-6b0c-4234-8e39-8474a26f7cdf"
url = f"http://localhost:8001/vagas/{vaga_id}"

response = requests.delete(url)
print(f"Status: {response.status_code}")  # 204 = sucesso