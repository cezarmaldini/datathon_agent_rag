import requests

vaga_id = "ce8596ce-8522-4986-b141-0b8dcf7302af"
url = f"https://datathon-api-o5cep.ondigitalocean.app/vagas/{vaga_id}"

response = requests.delete(url)
print(f"Status: {response.status_code}")  # 204 = sucesso