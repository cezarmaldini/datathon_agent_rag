import io
import asyncio
import streamlit as st
from pipeline import test, create_collection
from config.settings import Settings

st.title("🔍 Teste em Memória")

uploaded_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)

if uploaded_files and st.button("🚀 Executar Parse"):
    settings = Settings()
    create_collection.create_collections(settings=settings)
    embedding_models = test.initialize_embedding_models(settings=settings)

    in_memory_files = []
    points = []

    for f in uploaded_files:
        bio = io.BytesIO(f.read())
        bio.name = f.name
        in_memory_files.append(bio)

    # Parse
    results = asyncio.run(test.parse_document(files=in_memory_files, settings=settings))

    # Metadata serializável (apenas campo 'data')
    metadata_list = test.extract_metadata(files=in_memory_files, settings=settings)

    # Criar pontos
    for result, meta_list in zip(results, metadata_list):
        md_docs = result.get_markdown_documents(split_by_page=False)
        for doc in md_docs:
            chunks = test.create_chunks(documents=[doc], settings=settings)
            for chunk in chunks:
                # meta_list pode ter múltiplos ExtractRun, usar o primeiro (ou ajustar se houver mais)
                point = test.create_points(chunk=chunk, embedding_models=embedding_models, metadata=meta_list[0])
                points.append(point)
    
    if points:
        test.upload_in_batches(settings=settings, points=points)
    else:
        print("Nenhum ponto gerado para upload.")