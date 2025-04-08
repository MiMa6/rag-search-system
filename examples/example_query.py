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

# Load environment variables
load_dotenv()

# Import the RAG pipeline components
from rag_pipeline.engine.query_engine import RAGQueryEngine
import chromadb
from rag_pipeline.config import CHROMA_CONFIG


def list_available_collections():
    """List all available collections in ChromaDB."""
    try:
        chroma_client = chromadb.PersistentClient(
            path=CHROMA_CONFIG["persist_directory"]
        )
        collections = chroma_client.list_collections()
        if collections:
            print("\nAvailable collections:")
            for c in collections:
                collection = chroma_client.get_collection(c.name)
                count = collection.count()
                print(f"  - {c.name} ({count} documents)")
                # Try to get more details about the collection
                try:
                    result = collection.peek()
                    if result and "ids" in result and result["ids"]:
                        print(f"    - First document ID: {result['ids'][0]}")
                        print(
                            f"    - Has embeddings: {bool(result.get('embeddings', False))}"
                        )
                except Exception as e:
                    print(f"    - Error peeking: {e}")
        else:
            print("\nNo collections found.")
            print(f"ChromaDB directory: {CHROMA_CONFIG['persist_directory']}")
    except Exception as e:
        print(f"\nError listing collections: {e}")


def main():
    # Parse command line arguments
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
        help="Name of the model configuration to use",
    )
    parser.add_argument(
        "--response-mode",
        type=str,
        default=None,
        help="Response mode (optional, defaults to config setting)",
    )
    parser.add_argument("--question", type=str, help="Question to ask the RAG pipeline")
    parser.add_argument(
        "--debug", action="store_true", help="Print full error traceback"
    )
    parser.add_argument(
        "--list-collections",
        action="store_true",
        help="List all available collections",
    )
    args = parser.parse_args()

    # If list-collections flag is set, list collections and exit
    if args.list_collections:
        list_available_collections()
        return

    # If no question is provided, use interactive mode
    interactive_mode = args.question is None

    print(
        f"Step 3: Querying index from collection '{args.collection_name or 'default'}'..."
    )

    try:
        # Initialize the query engine
        query_engine = RAGQueryEngine(
            collection_name=args.collection_name,
            model_config=args.model_config,
        )

        if interactive_mode:
            print("\nEntering interactive query mode. Type 'exit' to quit.")
            while True:
                # Get question from user
                question = input("\nEnter your question: ")
                if question.lower() in ["exit", "quit", "q"]:
                    break

                # Query the index
                print("\nQuerying...")
                response = query_engine.query(
                    question, response_mode=args.response_mode
                )

                # Print the response
                print("\nResponse:")
                print(response)
        else:
            # Query the index with the provided question
            print(f"\nQuestion: {args.question}")
            print("\nQuerying...")
            response = query_engine.query(
                args.question, response_mode=args.response_mode
            )

            # Print the response
            print("\nResponse:")
            print(response)

    except Exception as e:
        print(f"\nError: {str(e)}")

        if args.debug:
            print("\n========== FULL TRACEBACK ==========")
            traceback.print_exc()
            print("====================================\n")

        print("\nChecking ChromaDB collections...")
        list_available_collections()

        print(
            "\nTip: Make sure you've created an index first by running 'python example_create_index.py'"
        )


if __name__ == "__main__":
    main()
