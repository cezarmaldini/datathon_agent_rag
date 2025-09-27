import requests

# Use o ID retornado na criação
vaga_id = "id-da-vaga-criada"  
url = f"http://localhost:8000/vagas/{vaga_id}"
response = requests.get(url)
print(response.json())