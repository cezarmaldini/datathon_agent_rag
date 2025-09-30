import requests

query = 'Desenvolvedor Junior'
url = 'http://localhost:8001/search'

search_data = {
    "query": query,
    "limit": 10,
    "vacancy": "Desenvolvedor Frontend - Júnior - Presencial - CLT"
}

response = requests.post(url, json=search_data)

print(response.status_code)
print(response.json())  # debug

if response.status_code == 200 and "results" in response.json():
    resultados = response.json()["results"]
    print(resultados)
else:
    print("Erro na busca:", response.json())
