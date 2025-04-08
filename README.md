# RAG Search System

A Retrieval Augmented Generation (RAG) pipeline for intelligent document comparison and analysis.

## 🎯 Overview

This project implements a RAG search system that enables sophisticated document comparison and version analysis across multiple file formats. It leverages LlamaIndex and advanced language models to provide intelligent insights about document differences, versioning, and content evolution.

## ✨ Features

- Multi-format document support (PDF, DOCX, TXT, MD)
- Intelligent document version comparison and analysis
- Semantic search capabilities across document collections
- Document version tracking and identification
- Multiple configurable model and embedding combinations
- ChromaDB vector database for persistent storage
- Modular architecture with separate components for:
  - Document loading and processing
  - Vector index management
  - Query processing
- Support for both OpenAI and Azure OpenAI services
- Command-line interface for easy execution
- Example scripts for document generation, index creation, and querying

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/MiMa6/rag-search-system
cd rag-search-system

# Install dependencies using Poetry
poetry install
```

## 🚀 Quick Start

The usage consists of three main steps:

### Step 1: Generate Test Documents (Optional)

```bash
# Generate sample document versions for testing
python example_generate_docs.py
```

### Step 2: Create Index

```bash
# Index your documents with the default configuration
python example_create_index.py --data-dir rag_pipeline/data/test_docs --collection-name example_collection
```

### Step 3: Query the Index

```bash
# Query using the interactive mode
python example_query.py --collection-name example_collection

# List available collections
python example_query.py --list-collections
```

### Web Interface

A web interface is available for querying the RAG system. The interface is built with Svelte and Express.js, providing a Simple way to interact with the system.

For setup and usage instructions, see the [Web Interface Documentation](web/README.md).

Key features:

- Real-time query responses
- Chat-like interface for question-answer interactions
- Debug logging for backend operations

To start the web interface:

```bash
# Start the backend server
cd web/backend
npm install
npm run dev

# In a new terminal, start the frontend
cd web/frontend
npm install
npm run dev
```

Then visit http://localhost:5173 in your browser.

### Running whole "Pipeline" by one command

```bash
# Use default configuration (gpt-4o + text-embedding-3-large)
poetry run python run_pipeline.py --default

# Use fast configuration (gpt-4 + text-embedding-3-small)
poetry run python run_pipeline.py --fast

# Use legacy configuration (gpt-3.5-turbo + text-embedding-3-small)
poetry run python run_pipeline.py --legacy

# Use Azure OpenAI default configuration
poetry run python run_pipeline.py --azure-default

# Use Azure OpenAI fast configuration
poetry run python run_pipeline.py --azure-fast
```

## 📁 Project Structure

```
.
├── rag_pipeline/         # Main package
│   ├── core/            # Core RAG pipeline functionality
│   ├── db/             # Database operations
│   ├── engine/         # Data loading and query processing
│   ├── config/         # Configuration management
│   ├── tools/          # Utility tools
│   ├── utils/          # General utilities
│   ├── scripts/        # Maintenance and utility scripts
│   ├── data/           # Data storage
│   │   └── chroma_db/  # ChromaDB persistent storage
│   └── tests/          # Test files
├── examples/            # Example usage scripts
│   ├── run_pipeline.py # Main pipeline script
│   └── ...
├── web/                # Web interface
├── pyproject.toml      # Project dependencies
└── .env               # Environment variables
```

## 🔧 Configuration

The RAG pipeline supports multiple configurations for different use cases:

### Model Configurations

1. **OpenAI Configurations**:

   - `default`: Uses gpt-4o with text-embedding-3-large (latest and most capable)
   - `fast`: Uses gpt-4 with text-embedding-3-small (faster processing)
   - `legacy`: Uses gpt-3.5-turbo with text-embedding-3-small (backward compatibility)

2. **Azure OpenAI Configurations**:
   - `azure_default`: Uses Azure GPT-4 with text-embedding-ada-002
   - `azure_fast`: Uses Azure GPT-3.5-turbo with text-embedding-ada-002

### File Type Configurations

- **default**: [.pdf, .txt, .docx, .md]
- **text_only**: [.txt, .md]
- **documents**: [.pdf, .docx]

### Environment Variables

Create a `.env` file in the project root with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

To use Azure OpenAI, update the endpoint URLs in the configuration:

```python
# Update in rag_pipeline/config.py
"api_base": "YOUR_AZURE_OPENAI_ENDPOINT",
```

## 💻 Programmatic Usage

### Complete Pipeline

```python
from rag_pipeline import RAGPipeline

# Initialize with preferred configuration
pipeline = RAGPipeline(
    data_dir="path/to/documents",
    model_config="default",  # or "fast", "legacy", "azure_default", "azure_fast"
    file_types="default"     # or "text_only", "documents"
)

# Load and index documents
pipeline.load_documents()

# Query the documents
response = pipeline.query("Compare all versions of Document A")
print(response)
```

### Component-based Approach

```python
from rag_pipeline.data_loader import DataLoader
from rag_pipeline.chroma_manager import ChromaDBManager
from rag_pipeline.query_engine import RAGQueryEngine

# 1. Load documents
data_loader = DataLoader(data_dir="path/to/documents")
documents = data_loader.load_documents()

# 2. Create or update index
chroma_manager = ChromaDBManager(collection_name="my_collection")
index = chroma_manager.create_index(documents)

# 3. Query the index
query_engine = RAGQueryEngine(collection_name="my_collection")
response = query_engine.query("What are the key differences between document versions?")
print(response)
```

## 🔍 Example Queries

The pipeline can answer various questions about your documents:

```
"Compare all versions of the Project Overview document. What are the key differences between versions?"
"Which version of the Technical Specification is more recent, and what major changes were made?"
"List all documents that appear to be different versions of the same content, ordered by date."
"Identify any documents that could be considered outdated and should be archived, explaining why."
```

## 📊 Inspecting the Vector Database

The project includes a dedicated tool for inspecting and managing ChromaDB collections:

```bash
# List all collections
python inspect_chroma.py --list

# View documents in a specific collection
python inspect_chroma.py --collection your_collection_name

```
