import os
from dotenv import load_dotenv
from typing import Optional
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    api_title: str = 'Datathon'
    api_description: str = 'Datathon'
    api_version: str = '0.1.0'

    # Qdrant Settings
    qdrant_url: str = os.getenv('QDRANT_URL')
    qdrant_api_key: str = os.getenv('QDRANT_API_KEY')
    qdrant_collection_name: str = os.getenv('QDRANT_COLLECTION_NAME')
    qdrant_timeout: float = 60.0
    qdrant_prefetch_limit: int = 25

    # LLamaCloud Settings
    llama_cloud_api_key: str = os.getenv('LLAMA_CLOUD_API_KEY')
    llama_cloud_language: str = 'pt'

    # Model Settings
    dense_model_name: str = (
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    bm25_model_name: str = "Qdrant/bm25"
    late_interaction_model_name: str = "colbert-ir/colbertv2.0"
