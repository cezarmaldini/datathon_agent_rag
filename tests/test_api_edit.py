import requests

vaga_id = "id-da-vaga-criada"
url = f"http://localhost:8000/vagas/{vaga_id}"

update_data = {
    "titulo": "Desenvolvedor Python Pleno",
    "salario": "R$ 6000 - R$ 8000",
    "nivel_experiencia": "Pleno"
}

response = requests.put(url, json=update_data)
print(response.json())