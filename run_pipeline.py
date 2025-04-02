"""
Main entry point for running the RAG pipeline with different configurations.

This script provides a command-line interface to run the RAG pipeline with various
model and file type configurations. It supports three main configurations:
- default: GPT-4 + text-embedding-3-small (newest)
- legacy: GPT-3.5-turbo + text-embedding-ada-002 (older)
- balanced: GPT-4 + text-embedding-ada-002 (mixed)

Usage:
    poetry run python run_pipeline.py --default
    poetry run python run_pipeline.py --legacy
    poetry run python run_pipeline.py --balanced
"""

import argparse
from rag_pipeline.core import RAGPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run RAG pipeline with specific configuration"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--default",
        action="store_true",
        help="Use default configuration (GPT-4 + text-embedding-3-small)",
    )
    group.add_argument(
        "--legacy",
        action="store_true",
        help="Use legacy configuration (GPT-3.5 + text-embedding-ada-002)",
    )
    group.add_argument(
        "--balanced",
        action="store_true",
        help="Use balanced configuration (GPT-4 + text-embedding-ada-002)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Initialize all configurations
    configurations = {
        "default": RAGPipeline(
            data_dir="rag_pipeline/data/test_docs",
            model_config="default",
            file_types="default",
        ),
        "legacy": RAGPipeline(
            data_dir="rag_pipeline/data/test_docs",
            model_config="legacy",
            file_types="documents",  # Only process PDF and DOCX files
        ),
        "balanced": RAGPipeline(
            data_dir="rag_pipeline/data/test_docs",
            model_config="balanced",
            file_types="text_only",  # Only process text and markdown files
        ),
    }

    # Select the configuration based on command line argument
    if args.default:
        selected_config = "default"
    elif args.legacy:
        selected_config = "legacy"
    else:  # balanced
        selected_config = "balanced"

    rag = configurations[selected_config]

    # Load and index documents for selected configuration
    print(f"\nLoading documents for {rag.collection_name}...")
    print(f"Using model: {rag.model_name}")
    print(f"Using embedding: {rag.embedding_model}")
    print(f"Processing file types: {rag.file_types}")
    rag.load_documents()

    # Example queries for document comparison
    questions = [
        "Compare all versions of the Project Overview document. What are the key differences between versions?",
        "Which version of the Technical Specification is more recent, and what major changes were made?",
        "List all documents that appear to be different versions of the same content, ordered by date.",
        "Identify any documents that could be considered outdated and should be archived, explaining why.",
    ]

    # Query the documents using selected configuration
    print(f"\n{'='*80}")
    print(f"Using {rag.collection_name} pipeline ({selected_config} configuration)")
    print(f"{'='*80}")
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 80)
        response = rag.query(question)
        print(f"Answer: {response}")


if __name__ == "__main__":
    main()
