# Document AI Assistant

A Retrieval-Augmented Generation (RAG) chatbot that enables users to query and interact with their PDF and DOCX documents using local large language models via Ollama. The system embeds document content into a ChromaDB vector store, retrieves the most relevant sections using semantic search, and generates accurate, context-aware answers through a FastAPI backend. All processing is performed locally, ensuring data privacy while delivering fast, reliable document-based question answering through a clean React interface.

## Features

- **Document Indexing**: Automatically processes and indexes PDF and DOCX files
- **Semantic Search**: Uses ChromaDB vector database for efficient document retrieval
- **Local LLM**: Powered by Ollama with the GPT-OSS 120B model
- **Real-time Streaming**: Stream AI responses as they're generated
- **Modern UI**: Clean React-based chat interface
- **Privacy-First**: All processing happens locally on your machine

## Architecture

The application consists of three main components:

1. **Document Indexer** (`index_documents.py`): Processes documents and stores embeddings in ChromaDB
2. **FastAPI Backend** (`main.py`): Handles chat requests and performs RAG
3. **React Frontend** (`my-app/`): User-friendly chat interface

## Prerequisites

- Python 3.8+
- Node.js 16+
- [Ollama](https://ollama.ai/) installed locally
- Ollama models:
  - `mxbai-embed-large` (for embeddings)
  - `gpt-oss:120b-cloud` (for chat generation, you can use every Ollama model that is already installed)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama Models

```bash
ollama pull mxbai-embed-large
ollama pull gpt-oss:120b-cloud
```

### 4. Install Frontend Dependencies

```bash
cd my-app
npm install
```

## Usage

### Step 1: Index Your Documents

1. Create a `documents` folder in the project root
2. Add your PDF and DOCX files to the folder
3. Run the indexer:

```bash
python index_documents.py
```

This will create a `chroma_db` directory with your document embeddings.

### Step 2: Start the Backend Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Step 3: Start the Frontend

In a new terminal:

```bash
cd my-app
npm start
```

The chat interface will open at `http://localhost:3000`

### Step 4: Start Chatting

Ask questions about your indexed documents, and the AI will provide answers based on the document content.

## API Endpoints

### POST `/chat/`

Send a question and receive a streaming response.

**Request Body:**
```json
{
  "question": "What is the main topic of the document?"
}
```

**Response:**
Streaming text response based on retrieved document context.

## How It Works

1. **Indexing Phase**:
   - Documents are loaded from the `documents` folder
   - Text is split into 500-character chunks with 50-character overlap
   - Each chunk is embedded using the `mxbai-embed-large` model
   - Embeddings are stored in ChromaDB

2. **Query Phase**:
   - User question is embedded using the same model
   - Top 3 most similar document chunks are retrieved
   - Retrieved context + question are sent to the LLM
   - LLM generates an answer based only on the provided context
   - Response is streamed back to the user in real-time

## Project Structure

```
.
├── main.py                 # FastAPI backend server
├── index_documents.py      # Document indexing script
├── documents/              # Place your PDF/DOCX files here
├── chroma_db/              # Vector database (auto-generated)
└── my-app/                 # React frontend
    ├── src/
    │   ├── App.js         # Main chat component
    │   └── App.css        # Styling
    └── package.json       # Frontend dependencies
```

## Configuration

### Change the LLM Model

Edit `main.py` line 45:
```python
model="gpt-oss:120b-cloud",  # Change to any Ollama model
```

### Adjust Chunk Size

Edit `index_documents.py` line 21:
```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
```

### Change Number of Retrieved Documents

Edit `main.py` line 34:
```python
results = collection.query(query_embeddings=[query_embedding], n_results=3)  # Change n_results
```

## Troubleshooting

### Ollama Connection Issues
Ensure Ollama is running:
```bash
ollama serve
```

### Port Already in Use
Change the backend port in `main.py`:
```bash
uvicorn main:app --reload --port 8001
```

Update the frontend API URL in `my-app/src/App.js` line 19:
```javascript
const response = await fetch("http://localhost:8001/chat/", {
```

### CORS Errors
If deploying to a different domain, update the CORS settings in `main.py` line 15:
```python
allow_origins=["http://your-frontend-url.com"],
```

## Performance Tips

- For faster embeddings, use a smaller embedding model
- Reduce chunk size for more precise retrieval
- Increase `n_results` for more context (may slow down generation)
- Use a smaller LLM for faster responses



## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [LangChain](https://langchain.com/) for document processing
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://react.dev/) for the frontend
