import requests

query = """
Analista de Dados - Júnior
Dados Gerais
Tipo de Contratação: PJ
PCD: Não
Local: Palmas/TO - Brasil
Modalidade: Presencial

Requisitos da Vaga
Nível Acadêmico: Superior
Competências Técnicas: SQL, Python, Power BI, Excel, Banco de Dados, ETL, Clouds
Habilidades Comportamentais: Comunicação, Trabalho em equipe, Proatividade, Organização, Raciocíonio lógico
Áreas de Atuação: TI, Dados, Análise de Dados, BI
"""

# Dados mais simples para teste
llm_data = {
    "query": query,
    "limit": 3,
    "collection_name": "Analista de Dados - Júnior - Presencial - PJ"
}

response = requests.post(
    url='https://datathon-api-ljhdg.ondigitalocean.app/llm',
    json=llm_data
)

print("Status:", response.status_code)
print("Response:", response.json()['answer'])