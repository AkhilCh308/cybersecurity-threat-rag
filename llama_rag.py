from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
import os

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.groq import Groq
import chromadb
from chromadb import PersistentClient

load_dotenv()

# Constants
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "cybersecurity_updates"

# Initialize Chroma client
client = PersistentClient(path=str(VECTORSTORE_DIR))
# Create Chroma Collection
chroma_collection = client.get_or_create_collection(COLLECTION_NAME)
# Embeddings
embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

# LLM (Groq API)
llm = Groq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)

# Apply settings globally
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = CHUNK_SIZE


def scrape_urls(urls):
    """
    Fetches cybersecurity news/advisories and stores them in ChromaDB
    """
    print("Fetching web data...")
    docs = SimpleWebPageReader(html_to_text=True).load_data(urls)

    print("Parsing into nodes...")
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(docs)

    # Reset collection
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    print("Setting up vector store...")
    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection,
        embedding_function=embed_model,
        client=client
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Creating index and inserting data...")
    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=storage_context
    )

    print("Data added to ChromaDB ✅")
    return index

def generate_response(index, query):
    """
    Queries the stored data for answers.
    """
    query_engine = index.as_query_engine(
        response_mode="compact",
        similarity_top_k=3
    )
    response = query_engine.query(query)
    return str(response)

