import asyncio
import uuid
from typing import List
from tqdm.auto import tqdm

from config import clients
from config.settings import Settings, ResumeCurriculum

from llama_cloud_services import LlamaParse
from llama_cloud_services import LlamaExtract
from llama_index.core.node_parser import SentenceSplitter
from transformers import AutoTokenizer

from fastembed import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from qdrant_client.http.models import PointStruct

# Parse
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

# Chunks
def create_chunks(documents, settings: Settings):
    max_tokens = settings.dense_model_max_tokens
    model_name = settings.dense_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    node_parser = SentenceSplitter(
        chunk_size=max_tokens,
        chunk_overlap=50,
        tokenizer=tokenizer
    )

    nodes = node_parser.get_nodes_from_documents(documents=documents)
    print(f"Criação de chunks concluída. {len(nodes)} chunks gerados.")

    return nodes

# Extract Metadata
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
        data_list = [run.data for run in res]
        results.append(data_list)
    return results

# Embeddings
def initialize_embedding_models(settings: Settings):
    dense_embedding_model = TextEmbedding(settings.dense_model_name)
    bm25_embedding_model = Bm25(settings.bm25_model_name)
    colbert_embedding_model = LateInteractionTextEmbedding(settings.late_interaction_model_name)

    return dense_embedding_model, bm25_embedding_model, colbert_embedding_model

def create_embeddings(chunk_text, dense_model, bm25_model, colbert_model):
    dense_embedding = list(dense_model.passage_embed([chunk_text]))[0].tolist()
    sparse_embedding = list(bm25_model.passage_embed([chunk_text]))[0].as_object()
    colbert_embedding = list(colbert_model.passage_embed([chunk_text]))[0].tolist()

    return {
        "dense": dense_embedding,
        "sparse": sparse_embedding,
        "colbertv2.0": colbert_embedding,
    }

# Points Qdrant
def create_points(chunk, embedding_models, metadata, vacancy: str):
    
    dense_model, bm25_model, colbert_model = embedding_models

    text = chunk.text

    embeddings = create_embeddings(chunk_text=text, dense_model=dense_model, bm25_model=bm25_model, colbert_model=colbert_model)

    payload = {
        'text': text,
        'metadata': {
            **metadata,
            'vacancy': vacancy
        }
    }

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector={
            'dense': embeddings['dense'],
            'sparse': embeddings['sparse'],
            'colbertv2.0': embeddings['colbertv2.0']
        },
        payload=payload
    )

    return point

# Upload Qdrant
def upload_in_batches(settings: Settings, points: List[PointStruct], batch_size: int = 10):
    qdrant_client = clients.new_qdrant_client(settings)
    collection_name = settings.qdrant_collection_name

    n_batches = (len(points) + batch_size - 1) // batch_size

    print(f"Uploading {len(points)} points to collection '{collection_name}' in {n_batches} batches...")

    for i in tqdm(range(0, len(points), batch_size), total=n_batches):
        batch = points[i : i + batch_size]
        qdrant_client.upload_points(collection_name=collection_name, points=batch)

    print(
        f"Successfully uploaded {len(points)} points to collection '{collection_name}'"
    )