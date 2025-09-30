import requests

url = "https://datathon-api-o5cep.ondigitalocean.app/vagas/"
response = requests.get(url)
print(response.json())