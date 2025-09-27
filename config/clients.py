from config.settings import Settings
from qdrant_client import QdrantClient
from supabase import Client, create_client

# Client Qdrant
def new_qdrant_client(settings: Settings):
    url: str = settings.qdrant_url
    api_key: str = settings.qdrant_api_key

    qdrant = QdrantClient(url=url, api_key=api_key)

    return qdrant

# Client Supabase
def new_supabase_client(settings: Settings):
    url: str = settings.supabase_url
    api_key: str = settings.supabase_url

    supabase: Client = create_client(supabase_url=url, supabase_key=api_key)

    return supabase