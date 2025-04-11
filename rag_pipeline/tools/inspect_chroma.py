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


def inspect_collection(chroma_client, collection_name):
    """
    Interactively inspect a collection's contents, including documents and metadata.
    """
    try:
        collection = chroma_client.get_collection(collection_name)
        doc_count = collection.count()
        print(f"\nCollection: {collection_name}")
        print(f"Total documents: {doc_count}")

        if doc_count == 0:
            print("Collection is empty.")
            return

        # Get all documents with their metadata and embeddings
        results = collection.get(include=["documents", "metadatas", "embeddings"])

        while True:
            print("\nInspection Options:")
            print("1. List all document IDs")
            print("2. View document contents")
            print("3. View document metadata")
            print("4. Search similar documents")
            print("5. Back to main menu")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                print("\nDocument IDs:")
                for i, doc_id in enumerate(results["ids"]):
                    print(f"{i+1}. {doc_id}")

            elif choice == "2":
                doc_idx = get_document_index(len(results["ids"]))
                if doc_idx is not None:
                    print("\nDocument Contents:")
                    print("-" * 80)
                    print(results["documents"][doc_idx][:1000])  # Show first 1000 chars
                    if len(results["documents"][doc_idx]) > 1000:
                        print("... (truncated)")
                    print("-" * 80)

            elif choice == "3":
                doc_idx = get_document_index(len(results["ids"]))
                if doc_idx is not None:
                    print("\nDocument Metadata:")
                    print("-" * 80)
                    metadata = results["metadatas"][doc_idx]
                    for key, value in metadata.items():
                        print(f"{key}: {value}")
                    print("-" * 80)

            elif choice == "4":
                doc_idx = get_document_index(len(results["ids"]))
                if doc_idx is not None:
                    query_embedding = results["embeddings"][doc_idx]
                    similar_docs = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=5,
                        include=["documents", "metadatas", "distances"],
                    )
                    print("\nSimilar Documents:")
                    print("-" * 80)
                    for i, (doc, meta, dist) in enumerate(
                        zip(
                            similar_docs["documents"][0],
                            similar_docs["metadatas"][0],
                            similar_docs["distances"][0],
                        )
                    ):
                        print(f"\n{i+1}. Distance: {dist:.4f}")
                        print(f"Metadata: {meta}")
                        print(f"Preview: {doc[:200]}...")
                    print("-" * 80)

            elif choice == "5":
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"Error inspecting collection: {str(e)}")


def get_document_index(max_docs):
    """Helper function to get valid document index from user input."""
    while True:
        try:
            idx = int(input(f"\nEnter document number (1-{max_docs}): ").strip()) - 1
            if 0 <= idx < max_docs:
                return idx
            print(f"Please enter a number between 1 and {max_docs}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Inspect and manage ChromaDB collections"
    )
    parser.add_argument("--list", action="store_true", help="List all collections")
    parser.add_argument("--delete", type=str, help="Name of collection to delete")

    parser.add_argument(
        "--force", action="store_true", help="Force deletion without confirmation"
    )
    parser.add_argument("--inspect", type=str, help="Name of collection to inspect")
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

    if args.inspect:
        inspect_collection(chroma_client, args.inspect)
    elif args.delete:
        delete_collection(chroma_client, args.delete, force=args.force)
    else:
        collections = list_collections(chroma_client)
        if collections:
            print("\nAvailable commands:")
            print("  --inspect COLLECTION_NAME : Inspect collection contents")
            print("  --delete COLLECTION_NAME  : Delete a collection")
            print("  --force                   : Skip deletion confirmation")


if __name__ == "__main__":
    main()
