import requests
import streamlit as st

def st_llm(url: str, query: str, collection_name: str):
    if st.button("🧠 Gerar Análise com IA", type="primary"):
        with st.spinner("Analisando candidatos com IA..."):
            try:
                llm_data = {
                    "query": query,
                    "limit": 10,
                    "collection_name": collection_name
                }

                response = requests.post(url, json=llm_data)
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    st.success("✅ Análise concluída!")
                    
                    # Exibir análise da LLM
                    st.markdown(resultado['answer'])
                    
                    # Exibir candidatos fonte
                    with st.expander("👥 Candidatos Analisados", expanded=False):
                        st.write(f"Total de candidatos considerados: {len(resultado['source_documents'])}")
                        
                        for i, candidato in enumerate(resultado['source_documents'], 1):
                            with st.expander(f"Candidato #{i}"):
                                st.write(candidato['page_content'])
                                if candidato['metadata']:
                                    st.caption("Metadados:")
                                    st.json(candidato['metadata'])
                else:
                    st.error(f"Erro na análise: {response.text}")
                    
            except Exception as e:
                st.error(f"Erro ao analisar candidatos: {str(e)}")