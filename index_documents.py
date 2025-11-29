import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

# Load documents
docs_path = "./documents"
docs = []
for file in os.listdir(docs_path):
    if file.endswith(".pdf"):
        docs.extend(PyPDFLoader(os.path.join(docs_path, file)).load())
    elif file.endswith(".docx"):
        docs.extend(Docx2txtLoader(os.path.join(docs_path, file)).load())

# Split text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

# Generate embeddings using Ollama
embedder = OllamaEmbeddings(model="mxbai-embed-large")
for chunk in chunks:
    text = chunk.page_content
    embedding = embedder.embed_query(text)
    collection.add(ids=[str(hash(text))], embeddings=[embedding], metadatas=[{"text": text}])

print("✅ Documents indexed successfully!")
