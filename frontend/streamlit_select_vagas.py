import requests
import streamlit as st

def streamlit_select_vagas(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            vagas = response.json()['vagas']
            vaga_options = [f"{vaga['titulo_vaga']} - {vaga['nivel_profissional']} - {vaga['modalidade']} - {vaga['tipo_contratacao']}" 
                        for vaga in vagas]
        else:
            vaga_options = ['Erro ao carregar vagas']
    except:
        vaga_options = ['Erro de conexão']

    select_vacancy = st.selectbox(
        'Vaga de destino:',
        vaga_options,
        help="Escolha a vaga que será associada a todos os currículos enviados"
    )

    return select_vacancy