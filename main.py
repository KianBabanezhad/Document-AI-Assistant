import chromadb
import ollama
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Initialize FastAPI
app = FastAPI()

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change "*" to your React frontend URL for security (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="company_docs")

class QueryRequest(BaseModel):
    question: str

def retrieve_documents(query):
    # Generate embedding for query
    embedder = OllamaEmbeddings(model="mxbai-embed-large")
    query_embedding = embedder.embed_query(query)

    # Retrieve top 3 relevant documents
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    return [doc["text"] for doc in results["metadatas"][0]]

@app.post("/chat/")
def chat(request: QueryRequest):
    # Retrieve relevant documents
    retrieved_texts = retrieve_documents(request.question)
    context = "\n".join(retrieved_texts)

    def generate():
        stream = ollama.chat(
            model="gpt-oss:120b-cloud",
            stream=True,
            messages=[
                {"role": "system", "content": "Answer based only on the provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {request.question}"}
            ]
        )
        for chunk in stream:
            yield chunk['message']['content']

    return StreamingResponse(generate(), media_type="text/plain")

# Run using: uvicorn main:app --reload
