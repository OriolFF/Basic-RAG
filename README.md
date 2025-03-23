# Basic RAG System

A simple implementation of a Retrieval-Augmented Generation (RAG) system that works locally using Ollama models and ChromaDB for document storage and retrieval.

## Components

### Core Files

- **query.py**: Command-line interface for querying the RAG system
  - Uses ChromaDB to retrieve relevant documents
  - Processes queries using Ollama embeddings
  - Streams responses from the LLM

- **user_query.py**: Gradio-based chat interface
  - Provides a web UI for interacting with the RAG system
  - Maintains chat history
  - Streams responses in real-time

- **indexer.py**: Document indexing system
  - Processes and chunks documents
  - Creates embeddings using Ollama
  - Stores documents and embeddings in ChromaDB
  - Handles recursive directory processing

- **utilities.py**: Helper functions
  - File reading and processing
  - Configuration management
  - Supports multiple file types (text, HTML)
  - Recursive directory traversal

### Configuration

- **config.txt**: System configuration
  - `embedmodel`: nomic-embed-text (for embeddings)
  - `mainmodel`: mistral (for text generation)
  - `source_path`: docs_for_test/
  - `db_path`: db/

### Dependencies

```plaintext
beautifulsoup4  # HTML processing
chromadb       # Vector database
mattsollamatools # Text chunking
ollama        # LLM and embeddings
requests      # HTTP requests
gradio        # Web UI
```

## Usage

1. **Setup**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Index Documents**:
   ```bash
   python indexer.py [path_to_docs]
   ```

3. **Query via Command Line**:
   ```bash
   python query.py "your question here"
   ```

4. **Launch Chat Interface**:
   ```bash
   python user_query.py
   ```

## Features

- Document chunking by sentences with configurable overlap
- Vector similarity search for relevant context
- Real-time streaming responses
- Web-based chat interface
- Support for text and HTML documents
- Configurable models and paths
- Document source tracking in responses

## Directory Structure 