#!/usr/bin/env python
"""
Example script to create an index from documents for the RAG pipeline.

This is step 2 in the RAG workflow - creating the index.
"""

import argparse
from pathlib import Path
from rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Create an index from documents for the RAG pipeline"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="rag_pipeline/data/test_docs",
        help="Directory containing the documents",
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default=None,
        help="Name for the ChromaDB collection (default: auto-generated)",
    )
    parser.add_argument(
        "--model-config",
        type=str,
        default="default",
        choices=["default", "fast", "legacy", "azure_default", "azure_fast"],
        help="Model configuration to use",
    )
    args = parser.parse_args()

    # Check if the data directory exists
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Data directory '{data_dir}' not found.")
        return

    print(f"Creating index from documents in '{data_dir}'...")

    # Initialize and load documents using RAGPipeline
    pipeline = RAGPipeline(
        data_dir=str(data_dir),
        collection_name=args.collection_name,
        model_config=args.model_config,
    )

    # Load documents and create index
    pipeline.load_documents()

    print("\nIndex created successfully!")
    print(f"Collection name: {pipeline.collection_name}")
    print("\nNext step: Run 'python example_query.py' to query the index")


if __name__ == "__main__":
    main()
