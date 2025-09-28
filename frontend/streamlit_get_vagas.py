import requests
import pandas as pd
import streamlit as st
from datetime import datetime

def streamlit_get_vagas(url: str):
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