import requests

url = "http://localhost:8001/vagas/"
response = requests.get(url)
print(response.json())