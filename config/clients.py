from config.settings import Settings
from qdrant_client import QdrantClient
from supabase import Client, create_client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

# Client Postgres Supabase
def get_database_url(settings: Settings) -> str:
    """Constrói a URL de conexão com o banco PostgreSQL no Supabase"""
    return f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"

settings = Settings()
SQLALCHEMY_DATABASE_URL = get_database_url(settings)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()