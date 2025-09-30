import requests
import pandas as pd
import streamlit as st
from datetime import datetime, date

# Interface para Listar Vagas
def st_get_vagas(url: str):
    st.subheader("Vagas Cadastradas")
        
    try:
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            data = response.json()
            vagas = data['vagas']
                
            if vagas:
                # Preparar dados para tabela
                df_data = []
                for vaga in vagas:
                    df_data.append({
                        'Título': vaga['titulo_vaga'],
                        'Cidade': vaga['cidade'],
                        'Estado': vaga['estado'],
                        'Nível': vaga['nivel_profissional'],
                        'Modalidade': vaga['modalidade'],
                        'Tipo': vaga['tipo_contratacao'],
                        'PCD': 'Sim' if vaga['vaga_pcd'] else 'Não',
                        'Status': 'Ativa' if vaga['ativa'] else 'Inativa',
                        'Data': datetime.fromisoformat(vaga['data_requisicao']).strftime('%d/%m/%Y')
                    })
                                     
                # Estatísticas rápidas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Vagas", len(vagas))
                with col2:
                    ativas = sum(1 for v in vagas if v['ativa'])
                    st.metric("Vagas Ativas", ativas)
                with col3:
                    pcd = sum(1 for v in vagas if v['vaga_pcd'])
                    st.metric("Vagas PCD", pcd)
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

            else:
                st.info("Nenhuma vaga cadastrada ainda.")
                    
    except Exception as e:
        st.error(f"Erro ao carregar vagas: {str(e)}")

# Interface para Cadastrar Vagas
def st_create_vagas(url: str):
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

# Interface para edição de vagas
def st_update_vagas(url: str):
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

# Interface para exclusão de vagas
def st_delete_vagas(url: str):
    st.subheader("Excluir Vaga")
        
    try:
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            vagas = response.json()['vagas']
                
            if vagas:
                vaga_options = {v['id']: f"{v['titulo_vaga']} - {v['nivel_profissional']} ({'Ativa' if v['ativa'] else 'Inativa'})" 
                                for v in vagas}
                vaga_selecionada = st.selectbox("Selecione a vaga para excluir:", 
                                                options=list(vaga_options.keys()),
                                                format_func=lambda x: vaga_options[x])
                    
                if vaga_selecionada:
                    vaga = next((v for v in vagas if v['id'] == vaga_selecionada), None)
                        
                    if vaga:
                        st.warning("⚠️ **Atenção:** Esta ação não pode ser desfeita!")
                            
                        with st.expander("Detalhes da Vaga"):
                            st.write(f"**Título:** {vaga['titulo_vaga']}")
                            st.write(f"**Cidade/Estado:** {vaga['cidade']}/{vaga['estado']}")
                            st.write(f"**Nível:** {vaga['nivel_profissional']}")
                            st.write(f"**Modalidade:** {vaga['modalidade']}")
                            st.write(f"**Status:** {'Ativa' if vaga['ativa'] else 'Inativa'}")
                            
                        if st.button("🗑️ Excluir Vaga Permanentemente", type="primary"):
                            try:
                                response = requests.delete(f"{url}/{vaga_selecionada}")
                                    
                                if response.status_code == 204:
                                    st.success("Vaga excluída com sucesso!")
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao excluir: {response.text}")
                                        
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")
            else:
                st.info("Nenhuma vaga cadastrada para excluir.")
                    
    except Exception as e:
        st.error(f"Erro ao carregar vagas: {str(e)}")