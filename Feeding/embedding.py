import os
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

# --- Configuration ---
# Ensure Ollama is running.
# Run `ollama pull nomic-embed-text`
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.containers.internal:11434")

# Ensure PostgreSQL with pgvector is running.
# https://github.com/pgvector/pgvector
# You may need to create the vector extension in your database: CREATE EXTENSION IF NOT EXISTS vector;
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg2://rag_user:rag_password@host.containers.internal:5432/rag_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_rag_collection")

# --- 1. Load Documents ---
# Using a web page as a document source.
print("Loading documents...")
loader = WebBaseLoader("https://arxiv.org/html/2503.16954v2")
docs = loader.load()
# Using a local docs directory as a document source.
# Create a "docs" directory and place your documents in it.
#loader = DirectoryLoader('docs/')
#docs = loader.load()

# --- 2. Split Documents into Chunks ---
print("Splitting documents...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# --- 3. Setup Embeddings and Vector Store ---
print("Initializing embeddings and vector store...")
# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(
      base_url=OLLAMA_HOST,
      model=EMBEDDING_MODEL
    )

# Initialize PGVector vector store
# This will create the table and add the documents if it doesn't exist.
db = PGVector.from_documents(
    embedding=embeddings,
    documents=chunks,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    use_jsonb=True
)

print("Documents have been embedded and saved to PGVector.")
