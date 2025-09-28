import requests

query = """
    Busque os candidatos mais adequados para esta vaga, considerando:
    
    Desenvolvedor Frontend - Júnior
    Dados Gerais
    Tipo de Contratação: CLT
    PCD: Não
    Local: São Paulo/SP - Brasil
    Modalidade: Híbrido

    Requisitos da Vaga
    Nível Acadêmico: Superior
    Competências Técnicas: HTML5, CSS3, JavaScript, React, TypeScript, Git, Responsive Design
    Habilidades Comportamentais: Trabalho em equipe, Comunicação, Proatividade, Atenção as detalhes
    Áreas de Atuação: Frontend, Desenvolvimento Web, UI/UX
"""

url = 'http://localhost:8001/search'

search_data = {
        "query": query,
        "limit": 10
    }

response = requests.post(f"{url}", json=search_data)
resultados = response.json()['results']
print(resultados)