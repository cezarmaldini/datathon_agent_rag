import streamlit as st
from pipeline import ingestion

st.title("Ingestão de Documentos no Banco Vetorial")

uploaded_files = st.file_uploader(
    "Selecione os arquivos para ingestão",
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} arquivo(s) selecionado(s).")

    if st.button("🚀 Executar Ingestão"):
        st.info("Iniciando ingestão em memória...")

        # Passar UploadedFile diretamente
        ingestion.ingest_documents(files=uploaded_files)

        st.success("✅ Ingestão concluída com sucesso!")