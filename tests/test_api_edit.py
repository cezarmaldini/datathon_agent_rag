import requests

vaga_id = "ce8596ce-8522-4986-b141-0b8dcf7302af"
url = f"https://datathon-api-o5cep.ondigitalocean.app/vagas/{vaga_id}"

update_data = {
    "titulo_vaga": "Desenvolvedor Python Pleno",
    "nivel_profissional": "Pleno"
}

response = requests.put(url, json=update_data)
print(response.json())