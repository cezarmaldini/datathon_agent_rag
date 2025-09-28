import requests
import pandas as pd
import streamlit as st
from datetime import datetime

def streamlit_create_vagas(url: str):
    st.subheader("Cadastrar Nova Vaga")
        
    with st.form("cadastrar_vaga"):
        col1, col2 = st.columns(2)
            
        with col1:
            titulo = st.text_input("Título da Vaga*")
            localizacao = st.text_input("Localização")
            salario = st.text_input("Salário")
            tipo_contrato = st.selectbox("Tipo de Contrato*", 
                                        ["CLT", "PJ", "Freelancer", "Estágio"])
            
        with col2:
            nivel = st.selectbox("Nível de Experiência*", 
                                   ["Júnior", "Pleno", "Sênior"])
            modalidade = st.selectbox("Modalidade*", 
                                        ["Presencial", "Híbrido", "Remoto"])
            ativa = st.checkbox("Vaga ativa", value=True)
            
        descricao = st.text_area("Descrição da Vaga*", height=100)
        requisitos = st.text_area("Requisitos (um por linha)*", height=100,
                                    help="Digite cada requisito em uma linha separada")
            
        if st.form_submit_button("Cadastrar Vaga", type="primary"):
            if titulo and descricao and requisitos:
                try:
                    requisitos_lista = [r.strip() for r in requisitos.split('\n') if r.strip()]
                        
                    vaga_data = {
                        "titulo": titulo,
                        "descricao": descricao,
                        "requisitos": requisitos_lista,
                        "salario": salario,
                        "localizacao": localizacao,
                        "tipo_contrato": tipo_contrato,
                        "nivel_experiencia": nivel,
                        "modalidade": modalidade,
                        "ativa": ativa
                    }
                        
                    response = requests.post(f"{url}/", json=vaga_data)
                        
                    if response.status_code == 201:
                        st.success("Vaga cadastrada com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao cadastrar: {response.text}")
                            
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.warning("Preencha todos os campos obrigatórios (*)")