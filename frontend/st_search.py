import requests
import streamlit as st

# Busca semântica
def st_search(url: str, query: str, collection_name: str):
    if st.button("🔍 Buscar Candidatos", type="primary"):
        with st.spinner("Buscando candidatos..."):
            try:
                search_data = {
                    "query": query,
                    "limit": 5,
                    "collection_name": collection_name
                }

                response = requests.post(f"{url}", json=search_data)
                
                if response.status_code == 200:
                    resultados = response.json()['results']
                    
                    st.success(f"✅ {len(resultados)} candidatos encontrados")
                    
                    # Exibir resultados
                    for i, candidato in enumerate(resultados, 1):
                        with st.expander(f"Candidato #{i}"):
                            st.write(candidato['page_content'])
                            if candidato['metadata']:
                                st.caption("Metadados:")
                                st.json(candidato['metadata'])
                else:
                    st.error(f"Erro na busca: {response.text}")
                    
            except Exception as e:
                st.error(f"Erro ao buscar candidatos: {str(e)}")