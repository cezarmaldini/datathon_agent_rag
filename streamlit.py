import io
import asyncio
import streamlit as st
from streamlit_option_menu import option_menu
from config.settings import Settings
from frontend import streamlit_upload, streamlit_get_vagas, streamlit_create_vagas, streamlit_update_vagas, streamlit_delete_vagas

settings = Settings()

api_base_url = settings.api_url_local

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

    url_api_vagas = f'{api_base_url}/vagas'

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

    streamlit_upload.streamlit_upload()