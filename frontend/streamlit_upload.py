import io
import asyncio
import requests
import streamlit as st
from pipeline import ingestion, create_collection
from config.settings import Settings
from frontend.streamlit_select_vagas import streamlit_select_vagas

def streamlit_upload(url: str):  
    # Seção de seleção de vaga
    st.subheader("Seleção da Vaga")
    st.markdown("Selecione a vaga para a qual deseja cadastrar os currículos:")

    select_vacancy = streamlit_select_vagas(url)
    
    # Seção de upload
    st.subheader("Upload dos Currículos")
    st.markdown("Selecione os arquivos dos candidatos:")
    
    uploaded_files = st.file_uploader(
        "Arraste e solte ou clique para selecionar arquivos", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt'],
        help="Formatos suportados: PDF, Word (.docx), Texto (.txt)"
    )
    
    # Exibir preview dos arquivos selecionados
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} arquivo(s) selecionado(s)")
        
        with st.expander("📋 Ver arquivos selecionados", expanded=False):
            cols = st.columns(3)
            for i, file in enumerate(uploaded_files):
                col = cols[i % 3]
                with col:
                    st.caption(f"**{file.name}**")
                    st.text(f"Tamanho: {len(file.getvalue()) / 1024:.1f} KB")
    
    # Botão de upload com validação
    if uploaded_files:
        st.subheader("Processamento")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            upload_btn = st.button(
                "🚀 Iniciar Upload e Processamento", 
                type="primary",
                use_container_width=True
            )
        
        with col2:
            st.info("⚠️ **Atenção:** O processo pode levar alguns minutos dependendo da quantidade de arquivos.")
        
        if upload_btn:
            # Barra de progresso
            progress_bar = st.progress(0, text="Iniciando processamento...")
            
            try:
                st.info('📤 **Upload Iniciado...** Aguarde enquanto processamos seus arquivos.')
                
                # Configuração inicial
                settings = Settings()
                create_collection.create_collections(collection_name=select_vacancy)
                embedding_models = ingestion.initialize_embedding_models(settings=settings)
                
                progress_bar.progress(10, text="Preparando arquivos...")
                
                # Processamento dos arquivos
                in_memory_files = []
                points = []
                
                for f in uploaded_files:
                    bio = io.BytesIO(f.read())
                    bio.name = f.name
                    in_memory_files.append(bio)
                
                progress_bar.progress(30, text="Analisando documentos...")
                
                # Processamento assíncrono
                results = asyncio.run(ingestion.parse_document(files=in_memory_files, settings=settings))
                
                progress_bar.progress(50, text="Extraindo metadados...")
                
                metadata_list = ingestion.extract_metadata(files=in_memory_files, settings=settings)
                
                progress_bar.progress(70, text="Processando conteúdo...")
                
                for result, meta_list in zip(results, metadata_list):
                    md_docs = result.get_markdown_documents(split_by_page=False)
                    for doc in md_docs:
                        chunks = ingestion.create_chunks(documents=[doc], settings=settings)
                        for chunk in chunks:
                            point = ingestion.create_points(chunk=chunk, embedding_models=embedding_models, metadata=meta_list[0], vacancy=select_vacancy)
                            points.append(point)
                
                progress_bar.progress(90, text="Fazendo upload final...")
                
                if points:
                    ingestion.upload_in_batches(collection_name=select_vacancy, settings=settings, points=points)
                    progress_bar.progress(100, text="Processamento concluído!")
                    
                    # Mensagem de sucesso
                    st.success('🎉 **Upload concluído com sucesso!**', icon='✅')
                    
                    # Resumo do processamento
                    with st.expander("📊 Resumo do Processamento", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Arquivos Processados", len(uploaded_files))
                        with col2:
                            st.metric("Vaga Associada", select_vacancy)
                    
                    st.balloons()
                    
                else:
                    st.error("❌ **Nenhum ponto gerado para upload.** Verifique os arquivos e tente novamente.")
                    
            except Exception as e:
                st.error(f"❌ **Erro durante o processamento:** {str(e)}")
                progress_bar.empty()
    
    else:
        # Estado inicial - instruções visuais
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📝 Passo a Passo:**
            1. Selecione a vaga
            2. Escolha os arquivos
            3. Clique em Upload
            """)
        
        with col2:
            st.markdown("""
            **✅ Formatos Aceitos:**
            - PDF Documents
            - Word (.docx)
            """)
        
        with col3:
            st.markdown("""
            **⚡ Dicas:**
            - Arquivos até 10MB cada
            - Mantenha conexão estável
            """)