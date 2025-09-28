import requests
import pandas as pd
import streamlit as st

def streamlit_delete_vagas(url: str):
    st.header("Excluir Vaga")
        
    try:
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            vagas = response.json()['vagas']
                
            if vagas:
                vaga_options = {v['id']: f"{v['titulo']} - {v['nivel_experiencia']} ({'Ativa' if v['ativa'] else 'Inativa'})" 
                                for v in vagas}
                vaga_selecionada = st.selectbox("Selecione a vaga para excluir:", 
                                                options=list(vaga_options.keys()),
                                                format_func=lambda x: vaga_options[x])
                    
                if vaga_selecionada:
                    vaga = next((v for v in vagas if v['id'] == vaga_selecionada), None)
                        
                    if vaga:
                        st.warning("⚠️ **Atenção:** Esta ação não pode ser desfeita!")
                            
                        with st.expander("Detalhes da Vaga"):
                            st.write(f"**Título:** {vaga['titulo']}")
                            st.write(f"**Descrição:** {vaga['descricao']}")
                            st.write(f"**Nível:** {vaga['nivel_experiencia']}")
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