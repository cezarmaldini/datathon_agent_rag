import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Models
    dense_model_name: str = ("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    dense_model_max_tokens: int = 768
    bm25_model_name: str = "Qdrant/bm25"
    late_interaction_model_name: str = "colbert-ir/colbertv2.0"
