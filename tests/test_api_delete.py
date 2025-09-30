import requests

vaga_id = "5693ce19-37e2-4c83-b063-00bbbcae7d02"
url = f"http://localhost:8001/vagas/{vaga_id}"

response = requests.delete(url)
print(f"Status: {response.status_code}")  # 204 = sucesso