from config import clients
from config.settings import Settings

from pipeline import create_collection

from llama_cloud_services import LlamaParse
from llama_index.core.node_parser import SentenceSplitter

from transformers import AutoTokenizer


def parse_document(files, settings: Settings):
    print(f"Iniciando o parse do arquivo: {files}...")
    parser = LlamaParse(
        api_key=settings.llama_cloud_api_key,
        result_type='markdown',
        language=settings.llama_cloud_language
    )

    documents = parser.load_data(files)
    print(f"Parse concluído. {len(documents)} documento(s) extraído(s).")
    
    return documents

def create_chunks(documents, settings: Settings):
    max_tokens = settings.dense_model_max_tokens
    model_name = settings.dense_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    node_parser = SentenceSplitter(
        chunk_size=max_tokens,
        chunk_overlap=50,
        tokenizer=tokenizer
    )

    print("Iniciando a criação dos chunks...")
    nodes = node_parser.get_nodes_from_documents(documents=documents)
    print(f"Criação de chunks concluída. {len(nodes)} chunks gerados.")

    return nodes

def main():
    setup = Settings()

    documents = parse_document(files='POSTECH - DTAT - Datathon - Fase 5.pdf', settings=setup)

    chunks = create_chunks(documents=documents, settings=setup)

    for i, chunk in enumerate(chunks):
        print(f'--- Chunk{i+1} ---')
        print(chunk.text)

if __name__ == '__main__':
    main()