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
- Modular architecture with:
  - Centralized configuration management
  - Dedicated ChromaDB manager
  - Efficient document loading
  - Streamlined query processing
- Support for both OpenAI and Azure OpenAI services
- Simple command-line interface
- Example scripts for index creation and querying

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/MiMa6/rag-search-system
cd rag-search-system

# Install dependencies using Poetry
poetry install
```

## 🚀 Quick Start

The usage consists of two main steps:

### Step 1: Create Index

```bash
# Create index with default settings
python examples/example_create_index.py --data-dir docs/

# Create index with specific model and collection name
python examples/example_create_index.py --data-dir docs/ --model-config default --collection-name my_docs
```

### Step 2: Query the Index

```bash
# List available collections
python examples/example_query.py --list

# Query with default settings
python examples/example_query.py

# Query with specific model and collection
python examples/example_query.py --model-config azure_fast --collection-name my_docs
```

### Running the Pipeline

```bash
# Use default configuration (gpt-4o + text-embedding-3-large)
python examples/run_pipeline.py --default

# Use Azure OpenAI configuration
python examples/run_pipeline.py --azure-default

# Interactive mode
python examples/run_pipeline.py --default --interactive
```

## 📁 Project Structure

```
.
├── rag_pipeline/         # Main package
│   ├── core/            # Core RAG pipeline implementation
│   │   └── core.py      # Main RAGPipeline class
│   ├── db/             # Database operations
│   │   └── chroma_manager.py  # ChromaDB management
│   ├── engine/         # Document loading and query processing
│   │   └── data_loader.py    # Document loading
│   ├── config.py       # Centralized configuration
│   └── tests/          # Test files
├── examples/           # Example usage scripts
└── .env               # Environment variables
```

## 🔧 Configuration

The system uses a centralized configuration in `config.py` for:

### Model Configurations

1. **OpenAI Configurations**:

   - `default`: Uses gpt-4o with text-embedding-3-large
     ´

2. **Azure OpenAI Configurations**:
   - `azure_default`: Uses Azure GPT-4 with text-embedding-ada-002

### Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

## 💻 Programmatic Usage

```python
from rag_pipeline import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline(
    data_dir="docs/",
    collection_name="my_collection",  # Optional
    model_config="default",          # Optional
)

# Load and index documents
pipeline.load_documents()

# Query the documents
response = pipeline.query("Compare all versions of Document A")
print(response)
```

## 🔍 Example Queries

The pipeline can answer various questions about your documents:

```
"Compare all versions of the Project Overview document. What are the key differences?"
"Which version of the Technical Specification is more recent?"
"List all documents that appear to be different versions of the same content."
"Identify any outdated documents that should be archived."
```

## 📊 Inspecting the Vector Database

The project includes a dedicated tool for inspecting and managing ChromaDB collections:

```bash
# List all collections
poetry run python rag_pipeline/tools/inspect_chroma.py --list

# View documents in a specific collection
poetry run python rag_pipeline/tools/inspect_chroma.py --collection your_collection_name
```

