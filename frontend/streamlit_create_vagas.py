import requests
import pandas as pd
import streamlit as st
from datetime import date

def streamlit_create_vagas(url: str):
    st.subheader("Cadastrar Nova Vaga")
        
    with st.form("cadastrar_vaga"):
        col1, col2 = st.columns(2)
            
        with col1:
            data_requisicao = st.date_input("Data da Requisição*", value=date.today())
            titulo_vaga = st.text_input("Título da Vaga*")
            cidade = st.text_input("Cidade*")
            estado = st.text_input("Estado (Sigla)*", max_chars=2)
            tipo_contratacao = st.selectbox("Tipo de Contratação*", 
                                          ["CLT", "PJ", "Freelancer", "Estágio"])
            nivel_profissional = st.selectbox("Nível Profissional*", 
                                            ["Júnior", "Pleno", "Sênior"])
            
        with col2:
            nivel_academico = st.selectbox("Nível Acadêmico*", 
                                         ["Ensino Médio", "Superior", "Pós-Graduação", "Mestrado", "Doutorado"])
            modalidade = st.selectbox("Modalidade*", 
                                    ["Presencial", "Híbrido", "Remoto"])
            vaga_pcd = st.checkbox("Vaga para PCD")
            ativa = st.checkbox("Vaga ativa", value=True)
            pais = st.text_input("País", value="Brasil")
            
        principais_atividades = st.text_area("Principais Atividades*", height=100)
        areas_atuacao = st.text_area("Áreas de Atuação (uma por linha)*", height=80,
                                   help="Digite cada área em uma linha separada")
        competencias_tecnicas = st.text_area("Competências Técnicas (uma por linha)*", height=80,
                                           help="Digite cada competência em uma linha separada")
        habilidades_comportamentais = st.text_area("Habilidades Comportamentais (uma por linha)*", height=80,
                                                 help="Digite cada habilidade em uma linha separada")
            
        if st.form_submit_button("Cadastrar Vaga", type="primary"):
            if (titulo_vaga and cidade and estado and principais_atividades and 
                areas_atuacao and competencias_tecnicas and habilidades_comportamentais):
                try:
                    areas_lista = [a.strip() for a in areas_atuacao.split('\n') if a.strip()]
                    competencias_lista = [c.strip() for c in competencias_tecnicas.split('\n') if c.strip()]
                    habilidades_lista = [h.strip() for h in habilidades_comportamentais.split('\n') if h.strip()]
                        
                    vaga_data = {
                        "data_requisicao": str(data_requisicao),
                        "titulo_vaga": titulo_vaga,
                        "tipo_contratacao": tipo_contratacao,
                        "vaga_pcd": vaga_pcd,
                        "cidade": cidade,
                        "estado": estado,
                        "pais": pais,
                        "nivel_profissional": nivel_profissional,
                        "nivel_academico": nivel_academico,
                        "areas_atuacao": areas_lista,
                        "principais_atividades": principais_atividades,
                        "competencias_tecnicas": competencias_lista,
                        "habilidades_comportamentais": habilidades_lista,
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