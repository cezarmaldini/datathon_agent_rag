import streamlit as st
from config.settings import Settings
from qdrant_client import QdrantClient
from openai import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Client Qdrant
def new_qdrant_client():
    url: str = st.secrets.get('QDRANT_URL')
    api_key: str = st.secrets.get('QDRANT_URL')

    qdrant = QdrantClient(url=url, api_key=api_key)

    return qdrant