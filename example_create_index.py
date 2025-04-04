#!/usr/bin/env python
"""
Example script to create an index from documents for the RAG pipeline.

This is step 2 in the RAG workflow - creating the index.
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the RAG pipeline components
from rag_pipeline.data_loader import DataLoader
from rag_pipeline.chroma_manager import ChromaDBManager


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Create an index from documents for the RAG pipeline"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        default="rag_pipeline/data/test_docs",
        help="Directory containing the documents (use the output directory from example_generate_docs.py)",
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default=None,
        help="Name for the ChromaDB collection (default: auto-generated based on model config)",
    )
    args = parser.parse_args()

    # Check if the data directory exists
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Data directory '{data_dir}' not found.")
        print(
            "Please run 'python example_generate_docs.py' first to generate test documents."
        )
        return

    print(f"Step 2: Creating index from documents in '{data_dir}'...")

    # Step 1: Load documents using DataLoader
    print("\nLoading documents...")
    data_loader = DataLoader(
        data_dir=str(data_dir),
        # Using default file types configuration
    )
    documents = data_loader.load_documents()

    # Step 2: Create index using ChromaDBManager
    print("\nCreating index...")
    chroma_manager = ChromaDBManager(
        collection_name=args.collection_name,
        # Using default model configuration
    )

    # Store the collection name for later use
    collection_name = chroma_manager.collection_name

    # Create the index
    index = chroma_manager.create_index(documents)

    print("\nIndex created successfully!")
    print(f"Collection name: {collection_name}")
    print("\nNext step: Run the following command to query the index:")
    print(f"python example_query.py --collection-name {collection_name}")


if __name__ == "__main__":
    main()
