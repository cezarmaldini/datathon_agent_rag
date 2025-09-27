import streamlit as st
from llama_cloud_services import LlamaParse
from config.settings import Settings
import io
import asyncio

async def parse_document(files, settings: Settings):
    parser = LlamaParse(
        api_key=settings.llama_cloud_api_key,
        result_type="markdown",
        language=settings.llama_cloud_language,
    )
    tasks = []
    for f in files:
        f.seek(0)
        tasks.append(parser.aparse(f, extra_info={"file_name": f.name}))
    return await asyncio.gather(*tasks)

st.title("🔍 Teste de LlamaParse em Memória")

uploaded_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)

if uploaded_files and st.button("🚀 Executar Parse"):
    settings = Settings()
    in_memory_files = []
    for f in uploaded_files:
        bio = io.BytesIO(f.read())
        bio.name = f.name
        in_memory_files.append(bio)

    results = asyncio.run(parse_document(in_memory_files, settings))

    for i, result in enumerate(results, 1):
        st.subheader(f"📄 Documento {i}")
        md_docs = result.get_markdown_documents(split_by_page=False)
        for doc in md_docs:
            st.markdown(doc.text[:1000])  # mostra primeiros 1000 caracteres