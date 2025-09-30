import streamlit as st
from qdrant_client import QdrantClient

# Client Qdrant
def new_qdrant_client():
    url: str = st.secrets.get('QDRANT_URL')
    api_key: str = st.secrets.get('QDRANT_API_KEY')

    qdrant = QdrantClient(url=url, api_key=api_key)

    return qdrant