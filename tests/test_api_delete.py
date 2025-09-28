import requests

vaga_id = "6c8e136f-c948-47fa-beea-37cca056a778"
url = f"http://localhost:8001/vagas/{vaga_id}"

response = requests.delete(url)
print(f"Status: {response.status_code}")  # 204 = sucesso