import requests
import streamlit as st

def st_select(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            vagas = response.json()['vagas']
            vaga_options = [f"{vaga['titulo_vaga']} - {vaga['nivel_profissional']} - {vaga['modalidade']} - {vaga['tipo_contratacao']}" 
                        for vaga in vagas]
            
            select_vacancy = st.selectbox(
                'Vaga de destino:',
                vaga_options,
                help="Escolha a vaga que será associada a todos os currículos enviados"
            )
            
            # Retornar apenas o texto selecionado
            return select_vacancy
        else:
            return None
    except:
        return None