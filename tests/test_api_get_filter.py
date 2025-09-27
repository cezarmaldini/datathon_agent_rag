import requests

# Só vagas ativas
url = "http://localhost:8000/vagas/?ativa=true&pagina=1&por_pagina=10"
response = requests.get(url)
print(response.json())