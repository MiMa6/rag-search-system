# RAG Pipeline

A Retrieval Augmented Generation (RAG) pipeline for intelligent document comparison and analysis.

## 🎯 Overview

This project implements a RAG pipelines that enables sophisticated document comparison and version analysis across multiple file formats. It leverages advanced language models to provide intelligent insights about document differences, versioning, and content evolution.

## ✨ Features

- Multi-format document support (TXT, DOCX, PDF)
- Intelligent document version comparison
- Semantic search capabilities

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/MiMa6/rag-pipelines
# Install required libraries
poetry install
```

## 🚀 Quick Start

1. Place your documents in the `rag_pipeline/data` directory
2. Run the pipeline:

```python
from rag_pipeline.core import RAGPipeline

# Initialize the pipeline
rag = RAGPipeline(
    data_dir="rag_pipeline/data/your_docs",
    collection_name="your_collection",
    model_name="gpt-3.5-turbo"
)

# Load and index documents
rag.load_documents()

# Query your documents
response = rag.query("Compare all versions of Document A")
print(response)
```

## 📁 Project Structure

```
rag_pipeline/
├── data/           # Document storage
├── tests/          # Test suite
├── utils/          # Utility functions
├── core.py         # Core pipeline implementation
└── __init__.py     # Package initialization
```

## 🔍 Example Usage

The pipeline comes with example scripts demonstrating its capabilities:

- `example.py`: Shows basic usage and document comparison
- `generate_test_docs.py`: Creates test documents for experimentation

Example queries you can run:

```python
questions = [
    "Compare all versions of the Project Overview document",
    "What are the key differences between Technical Specification versions?",
    "List documents that need archiving"
]
```

## 🔧 Configuration

The RAG pipeline can be configured with the following parameters:

- `data_dir`: Directory containing your documents
- `collection_name`: Name for your document collection
- `model_name`: Language model to use (default: "gpt-3.5-turbo")
