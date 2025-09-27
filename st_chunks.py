import streamlit as st
from llama_cloud_services import LlamaParse
from config.settings import Settings
from llama_index.core.node_parser import SentenceSplitter
from transformers import AutoTokenizer
import io
import asyncio

# --- Parse
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

# --- Chunks
def create_chunks(documents, settings: Settings):
    max_tokens = settings.dense_model_max_tokens
    model_name = settings.dense_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    node_parser = SentenceSplitter(
        chunk_size=max_tokens,
        chunk_overlap=50,
        tokenizer=tokenizer,
    )

    nodes = node_parser.get_nodes_from_documents(documents=documents)
    return nodes

# --- Streamlit UI
st.title("🔍 Teste de LlamaParse + Chunks em Memória")

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

        # Mostrar preview do texto
        for doc in md_docs:
            st.markdown(doc.text[:500])  # preview texto bruto

            # Criar chunks
            chunks = create_chunks([doc], settings)
            st.write(f"🔹 {len(chunks)} chunks gerados. Primeiros 3:")
            for c in chunks[:3]:
                st.code(c.text[:300])  # mostra 300 chars de cada chunk