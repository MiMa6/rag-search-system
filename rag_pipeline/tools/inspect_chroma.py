#!/usr/bin/env python
"""
Simple inspection tool for ChromaDB collections.

This script helps you examine the contents of your ChromaDB collections
to troubleshoot issues or verify data.
"""

import os
import sys
import argparse
import json
from pathlib import Path

import chromadb

# Import the configuration from the RAG pipeline
from rag_pipeline.config import CHROMA_CONFIG


def print_separator():
    """Print a separator line."""
    print("-" * 80)


def list_collections(chroma_client):
    """List all available collections in the ChromaDB instance."""
    collections = chroma_client.list_collections()

    if not collections:
        print("No collections found in the ChromaDB instance.")
        return []

    print(f"Found {len(collections)} collection(s):")
    for i, collection in enumerate(collections):
        col = chroma_client.get_collection(collection.name)
        count = col.count()
        print(f"  {i+1}. {collection.name} ({count} documents)")

    return [c.name for c in collections]


def inspect_collection(chroma_client, collection_name, limit=5):
    """Inspect a specific ChromaDB collection."""
    try:
        collection = chroma_client.get_collection(collection_name)
    except ValueError:
        print(f"Error: Collection '{collection_name}' not found.")
        return

    count = collection.count()
    print(f"Collection: {collection_name}")
    print(f"Document count: {count}")

    if count == 0:
        print("Warning: This collection is empty. No documents to show.")
        return

    # Get sample documents
    result = collection.query(
        query_texts=[""],  # Empty query to get random documents
        n_results=min(limit, count),
        include=["documents", "metadatas", "embeddings"],
    )

    # Show document details
    print_separator()
    print(f"Sample documents (showing {min(limit, count)} of {count}):")

    for i, doc_id in enumerate(result["ids"][0]):
        print(f"\nDocument {i+1} (ID: {doc_id}):")

        # Show metadata
        metadata = result["metadatas"][0][i] if result["metadatas"][0][i] else {}
        print(f"  Metadata: {json.dumps(metadata, indent=2)}")

        # Show document preview
        content = result["documents"][0][i]
        content_preview = content[:250] + "..." if len(content) > 250 else content
        print(f"  Content preview: {content_preview}")

        # Show embedding info
        if result["embeddings"] and len(result["embeddings"][0]) > 0:
            embedding = result["embeddings"][0][i]
            embedding_info = (
                f"Dimension: {len(embedding)}, First 3 values: {embedding[:3]}"
            )
            print(f"  Embedding: {embedding_info}")

    print_separator()
    print("Note: If you're seeing an empty collection or missing data, ensure:")
    print("  1. You've successfully created an index using example_create_index.py")
    print("  2. The correct collection name is being used")
    print("  3. The documents were properly loaded and embedded")


def delete_collection(chroma_client, collection_name, force=False):
    """Delete a specific ChromaDB collection."""
    try:
        # Check if collection exists
        collection_names = [c.name for c in chroma_client.list_collections()]
        if collection_name not in collection_names:
            print(f"Error: Collection '{collection_name}' not found.")
            return False

        # Get collection info
        collection = chroma_client.get_collection(collection_name)
        doc_count = collection.count()

        # Confirm deletion if not forced
        if not force:
            print(
                f"Warning: About to delete collection '{collection_name}' with {doc_count} documents."
            )
            confirmation = input("Are you sure? (y/N): ").lower()
            if confirmation != "y":
                print("Operation cancelled.")
                return False

        # Delete the collection
        chroma_client.delete_collection(collection_name)
        print(f"Successfully deleted collection '{collection_name}'.")
        return True

    except Exception as e:
        print(f"Error deleting collection: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Inspect and manage ChromaDB collections"
    )
    parser.add_argument("--list", action="store_true", help="List all collections")
    parser.add_argument(
        "--collection", type=str, help="Collection name to inspect or delete"
    )
    parser.add_argument(
        "--limit", type=int, default=5, help="Number of documents to display"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=CHROMA_CONFIG["persist_directory"],
        help="Path to ChromaDB directory",
    )
    parser.add_argument(
        "--delete", action="store_true", help="Delete the specified collection"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force deletion without confirmation"
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all collections (use with caution)",
    )

    args = parser.parse_args()

    # Check if ChromaDB directory exists
    if not os.path.exists(args.path):
        print(f"Error: ChromaDB directory not found at '{args.path}'")
        print("Run example_create_index.py first to create a collection")
        sys.exit(1)

    # Initialize ChromaDB client
    print(f"Connecting to ChromaDB at: {args.path}")
    chroma_client = chromadb.PersistentClient(path=args.path)

    # Handle delete all collections
    if args.delete_all:
        collections = chroma_client.list_collections()
        if not collections:
            print("No collections found to delete.")
            return

        if not args.force:
            print(f"Warning: About to delete ALL {len(collections)} collections:")
            for c in collections:
                print(f"  - {c.name}")
            confirmation = input("Are you sure? This cannot be undone! (y/N): ").lower()
            if confirmation != "y":
                print("Operation cancelled.")
                return

        for collection in collections:
            delete_collection(chroma_client, collection.name, force=True)
        print(f"Successfully deleted all {len(collections)} collections.")
        return

    # Handle delete specific collection
    if args.delete and args.collection:
        delete_collection(chroma_client, args.collection, force=args.force)
        return

    # List collections if requested or no specific collection provided
    if args.list or not args.collection:
        collections = list_collections(chroma_client)

        if not args.collection and collections:
            print("\nUse --collection NAME to inspect a specific collection")
            print("Use --delete --collection NAME to delete a collection")
            print("Use --delete-all to remove all collections")

    # Inspect a specific collection if requested
    if args.collection and not args.delete:
        print_separator()
        inspect_collection(chroma_client, args.collection, args.limit)


if __name__ == "__main__":
    main()
