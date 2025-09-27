from config import clients
from config.settings import Settings
from qdrant_client import models
from qdrant_client.http.models import VectorParams, Distance

def create_collections(settings: Settings):
    # Setup
    qdrant_client = clients.new_qdrant_client(settings=settings)
    collection_name = settings.qdrant_collection_name

    collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if collection_name in collection_names:
        print(f'Collection {collection_name} já existe.')
    
    else:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={
                # Vetor denso (semântico)
                "dense": VectorParams(size=768, distance=Distance.COSINE),
                # Vetor de interação tardia (ColBERT)
                "colbertv2.0": VectorParams(
                    size=128,
                    distance=Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM,
                    ),
                ),
            },
            sparse_vectors_config={
                # Vetor esparso (BM25)
                "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF),
            },
        )

        print(f"Collection '{collection_name}' criada com sucesso!")