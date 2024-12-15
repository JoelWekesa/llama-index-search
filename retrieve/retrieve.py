import os
from typing import List
from llama_index.core import VectorStoreIndex, Settings
from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient, QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

class Movie(BaseModel):
    """Data model for response."""
    title: str
    genres: List[str]
    overview: str


client = QdrantClient(host=os.environ['HOST'], port=6333)
aclient = AsyncQdrantClient(host=os.environ['HOST'], port=6333)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

llm = Groq(
    model=os.environ['MODEL'],
    api_key=os.environ['GROQ_API_KEY']
)

sllm = llm.as_structured_llm(output_cls=Movie)

Settings.embed_model = embed_model
Settings.llm = sllm

vector_store = QdrantVectorStore(
    "movies-recommend",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    batch_size=20,
)



index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)


query_engine = index.as_retriever(
    similarity_top_k=5, 
    sparse_top_k=12, 
    vector_store_query_mode="hybrid"
)

