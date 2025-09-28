import requests
import streamlit as st

def streamlit_sumary_vagas(url: str, vaga_selecionada: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            vagas = response.json()['vagas']
            
            # Encontrar a vaga selecionada
            for vaga in vagas:
                vaga_str = f"{vaga['titulo_vaga']} - {vaga['nivel_profissional']} - {vaga['modalidade']} - {vaga['tipo_contratacao']}"
                if vaga_str == vaga_selecionada:
                    return f"""
## {vaga['titulo_vaga']} - {vaga['nivel_profissional']}

### Dados Gerais
**Tipo de Contratação:** {vaga['tipo_contratacao']}  
**PCD:** {'Sim' if vaga['vaga_pcd'] else 'Não'}  
**Local:** {vaga['cidade']}/{vaga['estado']} - {vaga['pais']}  
**Modalidade:** {vaga['modalidade']}

### Requisitos da Vaga
**Nível Acadêmico:** {vaga['nivel_academico']}  
**Competências Técnicas:** {', '.join(vaga['competencias_tecnicas'])}  
**Habilidades Comportamentais:** {', '.join(vaga['habilidades_comportamentais'])}  
**Áreas de Atuação:** {', '.join(vaga['areas_atuacao'])}
"""
            return "Vaga não encontrada"
        else:
            return "Erro ao carregar vagas"
    except:
        return "Erro de conexão"