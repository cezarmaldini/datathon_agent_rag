from config.settings import Settings
from qdrant_client import QdrantClient

# Client Qdrant
def new_qdrant_client(settings: Settings):
    url: str = settings.qdrant_url
    api_key: str = settings.qdrant_api_key

    qdrant = QdrantClient(url=url, api_key=api_key)

    return qdrant