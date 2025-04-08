#!/usr/bin/env python
"""
Simple inspection tool for ChromaDB collections.
Allows listing and deleting collections.
"""

import os
import sys
import argparse
import chromadb
from rag_pipeline.config import CHROMA_CONFIG


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


def delete_collection(chroma_client, collection_name, force=False):
    """Delete a specific ChromaDB collection."""
    try:
        collection_names = [c.name for c in chroma_client.list_collections()]
        if collection_name not in collection_names:
            print(f"Error: Collection '{collection_name}' not found.")
            return False

        collection = chroma_client.get_collection(collection_name)
        doc_count = collection.count()

        if not force:
            print(
                f"Warning: About to delete collection '{collection_name}' with {doc_count} documents."
            )
            confirmation = input("Are you sure? (y/N): ").lower()
            if confirmation != "y":
                print("Operation cancelled.")
                return False

        chroma_client.delete_collection(collection_name)
        print(f"Successfully deleted collection '{collection_name}'.")
        return True

    except Exception as e:
        print(f"Error deleting collection: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="List and delete ChromaDB collections")
    parser.add_argument("--list", action="store_true", help="List all collections")
    parser.add_argument("--delete", type=str, help="Name of collection to delete")
    parser.add_argument(
        "--force", action="store_true", help="Force deletion without confirmation"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=CHROMA_CONFIG["persist_directory"],
        help="Path to ChromaDB directory",
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: ChromaDB directory not found at '{args.path}'")
        sys.exit(1)

    chroma_client = chromadb.PersistentClient(path=args.path)

    if args.delete:
        delete_collection(chroma_client, args.delete, force=args.force)
    else:
        collections = list_collections(chroma_client)
        if collections:
            print("\nUse --delete COLLECTION_NAME to delete a collection")
            print("Add --force to skip deletion confirmation")


if __name__ == "__main__":
    main()
