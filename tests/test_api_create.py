import requests
import json

url = "http://localhost:8001/vagas/"

vaga = {
    "titulo": "Desenvolvedor Python Júnior",
    "descricao": "Vaga para desenvolvedor Python iniciante",
    "requisitos": ["Python", "FastAPI", "PostgreSQL"],
    "salario": "R$ 3000 - R$ 5000",
    "localizacao": "Remoto",
    "tipo_contrato": "CLT",
    "nivel_experiencia": "Júnior",
    "modalidade": "Remoto"
}

response = requests.post(url, json=vaga)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))