import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
# Ensure Ollama is running.
# Run `ollama pull llama3` and `ollama pull nomic-embed-text`
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.containers.internal:11434")

# Ensure PostgreSQL with pgvector is running.
# https://github.com/pgvector/pgvector
# You may need to create the vector extension in your database: CREATE EXTENSION IF NOT EXISTS vector;
CONNECTION_STRING = os.getenv("CONNECTION_STRING", "postgresql+psycopg2://rag_user:rag_password@host.containers.internal:5432/rag_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_rag_collection")

# --- 1. Setup Embeddings and Vector Store ---
print("Initializing embeddings and connecting to vector store...")
# Initialize Ollama embeddings for query embedding
embeddings = OllamaEmbeddings(
      base_url=OLLAMA_HOST,
      model=EMBEDDING_MODEL
    )

# Connect to the existing PGVector vector store
# This assumes the collection has already been created and populated.
db = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)

# --- 2. Setup Retriever ---
# The retriever fetches relevant documents from the vector store.
print("Setting up retriever...")
retriever = db.as_retriever()

# --- 3. Setup RAG Chain ---
print("Setting up RAG chain...")
# Define the prompt template
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Helpful Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# Initialize the Ollama LLM
llm = ChatOllama(
      base_url=OLLAMA_HOST,
      model=OLLAMA_MODEL
    )

# Create the RAG chain using LangChain Expression Language (LCEL)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 4. Ask a Question ---
print("Ready to answer questions.")
question = "Has CP violation been measured?"

print(f"\nQuestion: {question}")

# Invoke the chain with the question
answer = rag_chain.invoke(question)

print(f"\nAnswer: {answer}")

# --- Example of another question ---
question_2 = "What is the concept of CP violation?"
print(f"\nQuestion: {question_2}")
answer_2 = rag_chain.invoke(question_2)
print(f"\nAnswer: {answer_2}")

# --- Example of unanswerable question ---
question_2 = "What is the world formula?"
print(f"\nQuestion: {question_2}")
answer_2 = rag_chain.invoke(question_2)
print(f"\nAnswer: {answer_2}")
