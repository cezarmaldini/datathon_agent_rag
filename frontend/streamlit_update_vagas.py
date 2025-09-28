import requests
import pandas as pd
import streamlit as st

def streamlit_update_vagas(url: str):
    st.header("Editar Vaga Existente")
        
    try:
        # Carregar vagas para seleção
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            vagas = response.json()['vagas']
                
            if vagas:
                vaga_options = {v['id']: f"{v['titulo']} - {v['nivel_experiencia']}" for v in vagas}
                vaga_selecionada = st.selectbox("Selecione a vaga para editar:", 
                                                options=list(vaga_options.keys()),
                                                format_func=lambda x: vaga_options[x])
                    
                if vaga_selecionada:
                    vaga = next((v for v in vagas if v['id'] == vaga_selecionada), None)
                        
                    if vaga:
                        with st.form("editar_vaga"):
                            col1, col2 = st.columns(2)
                                
                            with col1:
                                titulo = st.text_input("Título*", value=vaga['titulo'])
                                localizacao = st.text_input("Localização", value=vaga['localizacao'] or "")
                                salario = st.text_input("Salário", value=vaga['salario'] or "")
                                tipo_contrato = st.selectbox("Tipo de Contrato*", 
                                                            ["CLT", "PJ", "Freelancer", "Estágio"],
                                                            index=["CLT", "PJ", "Freelancer", "Estágio"].index(vaga['tipo_contrato']))
                                
                            with col2:
                                nivel = st.selectbox("Nível*", 
                                                    ["Júnior", "Pleno", "Sênior"],
                                                    index=["Júnior", "Pleno", "Sênior"].index(vaga['nivel_experiencia']))
                                modalidade = st.selectbox("Modalidade*", 
                                                            ["Presencial", "Híbrido", "Remoto"],
                                                            index=["Presencial", "Híbrido", "Remoto"].index(vaga['modalidade']))
                                ativa = st.checkbox("Vaga ativa", value=vaga['ativa'])
                                
                            descricao = st.text_area("Descrição*", value=vaga['descricao'], height=100)
                            requisitos = st.text_area("Requisitos*", 
                                                        value='\n'.join(vaga['requisitos']), 
                                                        height=100)
                                
                            if st.form_submit_button("Atualizar Vaga", type="primary"):
                                if titulo and descricao and requisitos:
                                    try:
                                        requisitos_lista = [r.strip() for r in requisitos.split('\n') if r.strip()]
                                            
                                        update_data = {
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
                                            
                                        response = requests.put(f"{url}/{vaga_selecionada}", json=update_data)
                                            
                                        if response.status_code == 200:
                                            st.success("Vaga atualizada com sucesso!")
                                            st.rerun()
                                        else:
                                            st.error(f"Erro ao atualizar: {response.text}")
                                                
                                    except Exception as e:
                                        st.error(f"Erro: {str(e)}")
                                else:
                                    st.warning("Preencha todos os campos obrigatórios (*)")
            else:
                st.info("Nenhuma vaga cadastrada para editar.")
                    
    except Exception as e:
        st.error(f"Erro ao carregar vagas: {str(e)}")