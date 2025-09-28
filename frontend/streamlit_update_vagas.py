import requests
import streamlit as st

def streamlit_update_vagas(url: str):
    st.header("Editar Vaga Existente")
        
    try:
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            vagas = response.json()['vagas']
                
            if vagas:
                vaga_options = {v['id']: f"{v['titulo_vaga']} - {v['nivel_profissional']}" for v in vagas}
                vaga_selecionada = st.selectbox("Selecione a vaga para editar:", 
                                                options=list(vaga_options.keys()),
                                                format_func=lambda x: vaga_options[x])
                    
                if vaga_selecionada:
                    vaga = next((v for v in vagas if v['id'] == vaga_selecionada), None)
                        
                    if vaga:
                        with st.form("editar_vaga"):
                            col1, col2 = st.columns(2)
                                
                            with col1:
                                titulo_vaga = st.text_input("Título da Vaga*", value=vaga['titulo_vaga'])
                                cidade = st.text_input("Cidade*", value=vaga['cidade'])
                                estado = st.text_input("Estado*", value=vaga['estado'], max_chars=2)
                                tipo_contratacao = st.selectbox("Tipo de Contratação*", 
                                                                ["CLT", "PJ", "Freelancer", "Estágio"],
                                                                index=["CLT", "PJ", "Freelancer", "Estágio"].index(vaga['tipo_contratacao']))
                                
                            with col2:
                                nivel_profissional = st.selectbox("Nível Profissional*", 
                                                                ["Júnior", "Pleno", "Sênior"],
                                                                index=["Júnior", "Pleno", "Sênior"].index(vaga['nivel_profissional']))
                                modalidade = st.selectbox("Modalidade*", 
                                                        ["Presencial", "Híbrido", "Remoto"],
                                                        index=["Presencial", "Híbrido", "Remoto"].index(vaga['modalidade']))
                                vaga_pcd = st.checkbox("Vaga PCD", value=vaga['vaga_pcd'])
                                ativa = st.checkbox("Vaga ativa", value=vaga['ativa'])
                                
                            nivel_academico = st.selectbox("Nível Acadêmico*", 
                                                         ["Ensino Médio", "Superior", "Pós-Graduação", "Mestrado", "Doutorado"],
                                                         index=["Ensino Médio", "Superior", "Pós-Graduação", "Mestrado", "Doutorado"].index(vaga['nivel_academico']))
                            principais_atividades = st.text_area("Principais Atividades*", value=vaga['principais_atividades'], height=100)
                            areas_atuacao = st.text_area("Áreas de Atuação*", value='\n'.join(vaga['areas_atuacao']), height=80)
                            competencias_tecnicas = st.text_area("Competências Técnicas*", value='\n'.join(vaga['competencias_tecnicas']), height=80)
                            habilidades_comportamentais = st.text_area("Habilidades Comportamentais*", value='\n'.join(vaga['habilidades_comportamentais']), height=80)
                                
                            if st.form_submit_button("Atualizar Vaga", type="primary"):
                                if titulo_vaga and cidade and estado and principais_atividades:
                                    try:
                                        areas_lista = [a.strip() for a in areas_atuacao.split('\n') if a.strip()]
                                        competencias_lista = [c.strip() for c in competencias_tecnicas.split('\n') if c.strip()]
                                        habilidades_lista = [h.strip() for h in habilidades_comportamentais.split('\n') if h.strip()]
                                            
                                        update_data = {
                                            "titulo_vaga": titulo_vaga,
                                            "cidade": cidade,
                                            "estado": estado,
                                            "tipo_contratacao": tipo_contratacao,
                                            "nivel_profissional": nivel_profissional,
                                            "nivel_academico": nivel_academico,
                                            "areas_atuacao": areas_lista,
                                            "principais_atividades": principais_atividades,
                                            "competencias_tecnicas": competencias_lista,
                                            "habilidades_comportamentais": habilidades_lista,
                                            "modalidade": modalidade,
                                            "vaga_pcd": vaga_pcd,
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