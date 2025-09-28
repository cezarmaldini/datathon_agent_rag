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
                        'ID': vaga['id'],
                        'Título': vaga['titulo'],
                        'Localização': vaga['localizacao'],
                        'Nível': vaga['nivel_experiencia'],
                        'Modalidade': vaga['modalidade'],
                        'Salário': vaga['salario'],
                        'Status': 'Ativa' if vaga['ativa'] else 'Inativa',
                        'Criada em': datetime.fromisoformat(vaga['criada_em']).strftime('%d/%m/%Y')
                    })
                                     
                # Estatísticas rápidas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Vagas", len(vagas))
                with col2:
                    ativas = sum(1 for v in vagas if v['ativa'])
                    st.metric("Vagas Ativas", ativas)
                with col3:
                    st.metric("Vagas Inativas", len(vagas) - ativas)
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

            else:
                st.info("Nenhuma vaga cadastrada ainda.")
                    
    except Exception as e:
        st.error(f"Erro ao carregar vagas: {str(e)}")