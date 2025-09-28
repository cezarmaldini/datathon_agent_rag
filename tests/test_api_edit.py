import requests

vaga_id = "eea2111f-ee7e-4f78-b99a-a35a5fe22c36"
url = f"http://localhost:8001/vagas/{vaga_id}"

update_data = {
    "titulo_vaga": "Desenvolvedor Python Pleno",
    "nivel_profissional": "Pleno"
}

response = requests.put(url, json=update_data)
print(response.json())