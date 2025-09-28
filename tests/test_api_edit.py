import requests

vaga_id = "f9dc2061-3c31-4acc-be92-443950395d3c"
url = f"http://localhost:8001/vagas/{vaga_id}"

update_data = {
    "titulo": "Teste",
    "salario": "R$ 6000 - R$ 8000",
    "nivel_experiencia": "Pleno"
}

response = requests.put(url, json=update_data)
print(response.json())