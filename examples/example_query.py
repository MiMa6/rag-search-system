#!/usr/bin/env python
"""
Example script to query an existing index using the RAG pipeline.

This is step 3 in the RAG workflow - querying the index.
"""

import argparse
import os
import sys
import traceback
from dotenv import load_dotenv
import chromadb
from rag_pipeline import RAGPipeline
from rag_pipeline.config import CHROMA_CONFIG

# Load environment variables
load_dotenv()


def list_collections():
    """List all available collections in ChromaDB."""
    try:
        client = chromadb.PersistentClient(path=CHROMA_CONFIG["persist_directory"])
        collections = client.list_collections()

        if not collections:
            print("\nNo collections found.")
            return

        print("\nAvailable collections:")
        for collection in collections:
            count = client.get_collection(collection.name).count()
            print(f"  - {collection.name} ({count} documents)")
    except Exception as e:
        print(f"\nError listing collections: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Query an existing index using the RAG pipeline"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        help="Name of the ChromaDB collection to query",
    )
    parser.add_argument(
        "--model-config",
        type=str,
        default="default",
        choices=["default", "fast", "legacy", "azure_default", "azure_fast"],
        help="Model configuration to use",
    )
    parser.add_argument(
        "--response-mode",
        type=str,
        default=None,
        help="Response mode (defaults to config setting)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available collections",
    )
    args = parser.parse_args()

    if args.list:
        list_collections()
        return

    # Initialize pipeline
    pipeline = RAGPipeline(
        collection_name=args.collection_name,
        model_config=args.model_config,
    )

    try:
        # Load existing index
        pipeline.load_documents()
    except Exception as e:
        print(f"\nError loading collection: {e}")
        print("\nAvailable collections:")
        list_collections()
        return

    # Interactive query mode
    print(f"\nQuerying collection: {pipeline.collection_name}")
    print("Type 'exit' to quit")

    while True:
        question = input("\nEnter your question: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            break
        if not question:
            continue

        print("\nQuerying...")
        response = pipeline.query(question, response_mode=args.response_mode)
        print(f"\nResponse: {response}")


if __name__ == "__main__":
    main()
