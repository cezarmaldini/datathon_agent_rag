import requests

vaga_id = "id-da-vaga-criada"
url = f"http://localhost:8000/vagas/{vaga_id}"

response = requests.delete(url)
print(f"Status: {response.status_code}")  # 204 = sucesso