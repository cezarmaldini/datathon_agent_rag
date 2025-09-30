import streamlit as st
from streamlit_option_menu import option_menu
from frontend import st_crud, st_select, st_upload, st_summary, st_llm

url_api_vagas: str = st.secrets.get('API_URL_VAGAS')
url_api_llm: str = st.secrets.get('API_URL_LLM')

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
        st_crud.st_get_vagas(url=url_api_vagas)
    
    with tab2:
        st_crud.st_create_vagas(url=url_api_vagas)

    with tab3:
        st_crud.st_update_vagas(url=url_api_vagas)
    
    with tab4:
        st_crud.st_delete_vagas(url=url_api_vagas)

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
    
    st_upload.st_upload(url=url_api_vagas)

elif option == 'Relatórios':
    # Header da página
    st.title("📊 Relatórios | Análise de Candidatos")
    st.markdown("---")

    vaga_selecionada = st_select.st_select(url=url_api_vagas)
    resumo_vaga = st_summary.st_summary(url=url_api_vagas, vaga_selecionada=vaga_selecionada)

    with st.expander("📃 Resumo da Vaga", expanded=False):
        st.markdown(resumo_vaga)

    query = f"""
    Busque os candidatos mais adequados para esta vaga, considerando:
    
    {resumo_vaga}
    
    """
    st_llm.st_llm(url=url_api_llm, query=query, collection_name=vaga_selecionada)