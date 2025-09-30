import requests

query = 'Desenvolvedor Junior'
url = 'https://datathon-api-o5cep.ondigitalocean.app/search'

search_data = {
    "query": query,
    "limit": 10,
    "collection_name": "Desenvolvedor Frontend - Júnior - Presencial - CLT"
}

response = requests.post(url, json=search_data)

print(response.status_code)
print(response.json())  # debug

if response.status_code == 200 and "results" in response.json():
    resultados = response.json()["results"]
    print(resultados)
else:
    print("Erro na busca:", response.json())
