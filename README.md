# RAG Pipeline

A Retrieval Augmented Generation (RAG) pipeline for intelligent document comparison and analysis.

## 🎯 Overview

This project implements a RAG pipeline that enables sophisticated document comparison and version analysis across multiple file formats. It leverages advanced language models to provide intelligent insights about document differences, versioning, and content evolution.

## ✨ Features

- Multi-format document support (TXT, DOCX, PDF)
- Intelligent document version comparison
- Semantic search capabilities
- Configurable model and embedding combinations
- Flexible file type processing
- Command-line interface for easy execution

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/MiMa6/rag-pipelines
# Install required libraries
poetry install
```

## 🚀 Quick Start

1. Place your documents in the `rag_pipeline/data` directory
2. Run the pipeline using the command-line interface:

```bash
# Use default configuration (GPT-4 + text-embedding-3-small)
poetry run python run_pipeline.py --default

# Use legacy configuration (GPT-3.5 + text-embedding-ada-002)
poetry run python run_pipeline.py --legacy

# Use balanced configuration (GPT-4 + text-embedding-ada-002)
poetry run python run_pipeline.py --balanced
```

## 📁 Project Structure

```
rag_pipeline/
├── data/           # Document storage
├── tests/          # Test suite
├── utils/          # Utility functions
├── core.py         # Core pipeline implementation
├── config.py       # Configuration management
├── run_pipeline.py # Main entry point
└── __init__.py     # Package initialization
```

## 🔧 Configuration

The RAG pipeline supports three main configurations:

### Model Configurations

- **default**: GPT-4 + text-embedding-3-small (newest)
- **legacy**: GPT-3.5-turbo + text-embedding-ada-002 (older)
- **balanced**: GPT-4 + text-embedding-ada-002 (mixed)

### File Type Configurations

- **default**: [.pdf, .txt, .docx, .md]
- **text_only**: [.txt, .md]
- **documents**: [.pdf, .docx]

### Programmatic Usage

You can also use the pipeline programmatically with custom configurations:

```python
from rag_pipeline.core import RAGPipeline

# Initialize with specific configuration
rag = RAGPipeline(
    data_dir="rag_pipeline/data/your_docs",
    model_config="default",  # or "legacy" or "balanced"
    file_types="default"     # or "text_only" or "documents"
)

# Load and index documents
rag.load_documents()

# Query your documents
response = rag.query("Compare all versions of Document A")
print(response)
```

## 🔍 Example Queries

The pipeline can answer various questions about your documents:

```python
questions = [
    "Compare all versions of the Project Overview document",
    "What are the key differences between Technical Specification versions?",
    "List documents that need archiving",
    "Which version of the Technical Specification is more recent?",
    "List all documents that appear to be different versions of the same content"
]
```
