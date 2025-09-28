import streamlit as st
from llama_cloud_services import LlamaExtract
from config.settings import Settings, ResumeCurriculum
import io

st.title("📑 Teste de LlamaExtract em Memória")

uploaded_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)

def extract_metadata(files, settings: Settings):
    extractor = LlamaExtract(api_key=settings.llama_cloud_api_key)

    agents = extractor.list_agents()
    names = [a.name for a in agents]

    if "resume-curriculum" in names:
        agent_extract = extractor.get_agent(name="resume-curriculum")
    else:
        agent_extract = extractor.create_agent(
            name="resume-curriculum", data_schema=ResumeCurriculum
        )

    results = []
    for f in files:
        f.seek(0)
        res = agent_extract.extract(files=[f])
        results.append(res)
    return results

if uploaded_files and st.button("🚀 Executar Extração"):
    settings = Settings()

    in_memory_files = []
    for f in uploaded_files:
        bio = io.BytesIO(f.read())
        bio.name = f.name
        in_memory_files.append(bio)

    results = extract_metadata(in_memory_files, settings)

    for i, res in enumerate(results, 1):
        st.subheader(f"📄 Resultado {i}")
        st.json(res)