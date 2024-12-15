import json
import os
from pathlib import Path
from llama_index.core import Document, StorageContext, VectorStoreIndex, Settings
from tqdm import tqdm
from qdrant_client import AsyncQdrantClient, QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

current_folder = Path(__file__).parent.resolve()

parent_folder = current_folder.parent.resolve()

movies_file = parent_folder / "library" / "movies.json"

with open(movies_file, "r") as f:
    movie_data = json.load(f)
    
    
documents = []  
for movie in tqdm(movie_data):
    content = f"Title: {movie['title']}\nGenres: {movie['genres']}\nOverview: {movie['overview']}"
    
    id = str(movie['id'])
    
    doc = Document(text=content, id_=id) # type: ignore
    
    documents.append(doc)


client = QdrantClient(host=os.environ['HOST'], port=6333)
aclient = AsyncQdrantClient(host=os.environ['HOST'], port=6333)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

llm = Groq(
    model=os.environ['MODEL'],
    api_key=os.environ['GROQ_API_KEY']
)

Settings.embed_model = embed_model
Settings.llm = llm

vector_store = QdrantVectorStore(
    "movies-recommend",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    batch_size=20,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents=documents,
    storage_context=storage_context,
    show_progress=True
)
