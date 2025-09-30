import streamlit as st
from streamlit_option_menu import option_menu
from config.settings import Settings
from frontend import (
    streamlit_upload, streamlit_get_vagas, streamlit_create_vagas, 
    streamlit_update_vagas, streamlit_delete_vagas, streamlit_select_vagas,
    streamlit_sumary_vagas, streamlit_llm
)

# Setup
settings = Settings()

url_api_vagas = settings.api_url_vagas
url_api_llm = settings.api_url_llm

# Configuração inicial da aplicação
st.set_page_config(
    page_title='Agente IA',
    page_icon='🤖',
    layout='wide'
)

# Navegação da Aplicação
with st.sidebar:
    option = option_menu(
        menu_title="Navegação",
        options=["Vagas", "Upload", "Relatórios"],
        icons=["database-add", "folder-plus", "robot"],
        menu_icon="card-list",
        default_index=0
    )

if option == 'Vagas':
    # Header da página
    st.title('🧑‍💻 Banco de Dados de Vagas')

    tab1, tab2, tab3, tab4 = st.tabs(['📋 Vagas', '➕ Cadastrar', '✏️ Editar', '🗑️ Excluir'])

    with tab1:
        streamlit_get_vagas.streamlit_get_vagas(url=url_api_vagas)
    
    with tab2:
        streamlit_create_vagas.streamlit_create_vagas(url=url_api_vagas)

    with tab3:
        streamlit_update_vagas.streamlit_update_vagas(url=url_api_vagas)
    
    with tab4:
        streamlit_delete_vagas.streamlit_delete_vagas(url=url_api_vagas)

elif option == 'Upload':
    # Header da página
    st.title("📄 Upload de Currículos")
    st.markdown("---")

     # Introdução e instruções
    with st.expander("ℹ️ Como usar esta ferramenta", expanded=False):
        st.markdown("""
        **Bem-vindo ao sistema de upload de currículos!**
        
        Esta ferramenta permite:
        - Fazer upload de múltiplos currículos simultaneamente
        - Associar os currículos a vagas específicas
        - Processar automaticamente os documentos para análise com IA
        
        **Formato suportado:** PDF, DOCX
        """)
    
    streamlit_upload.streamlit_upload(url=url_api_vagas)

elif option == 'Relatórios':
    # Header da página
    st.title("📊 Relatórios | Análise de Candidatos")
    st.markdown("---")

    vaga_selecionada = streamlit_select_vagas.streamlit_select_vagas(url=url_api_vagas)
    resumo_vaga = streamlit_sumary_vagas.streamlit_sumary_vagas(url=url_api_vagas, vaga_selecionada=vaga_selecionada)

    with st.expander("📃 Resumo da Vaga", expanded=False):
        st.markdown(resumo_vaga)

    query = f"""
    Busque os candidatos mais adequados para esta vaga, considerando:
    
    {resumo_vaga}
    
    """
    streamlit_llm.streamlit_llm(url=url_api_llm, query=query, collection_name=vaga_selecionada)