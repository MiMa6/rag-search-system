"""
Main entry point for running the RAG pipeline with different configurations.
"""

import argparse
from pathlib import Path
from rag_pipeline.core.core import RAGPipeline
from rag_pipeline.config import get_model_config, get_file_types, MODEL_CONFIGS


def main():
    parser = argparse.ArgumentParser(
        description="Run RAG pipeline with different configurations"
    )

    # Model configuration arguments
    model_group = parser.add_mutually_exclusive_group(required=True)
    model_group.add_argument(
        "--default",
        action="store_true",
        help="Use default configuration (gpt-4o + text-embedding-3-large)",
    )
    model_group.add_argument(
        "--fast",
        action="store_true",
        help="Use fast configuration (gpt-4 + text-embedding-3-small)",
    )
    model_group.add_argument(
        "--legacy",
        action="store_true",
        help="Use legacy configuration (gpt-3.5-turbo + text-embedding-3-small)",
    )
    model_group.add_argument(
        "--azure-default",
        action="store_true",
        help="Use Azure OpenAI default configuration",
    )
    model_group.add_argument(
        "--azure-fast", action="store_true", help="Use Azure OpenAI fast configuration"
    )

    # Optional arguments
    parser.add_argument(
        "--data-dir",
        type=str,
        default="rag_pipeline/data/test_docs",  # Updated default path
        help="Directory containing documents",
    )
    parser.add_argument(
        "--file-types",
        type=str,
        default="default",
        choices=["default", "text_only", "documents"],
        help="File types to process",
    )

    args = parser.parse_args()

    # Determine model configuration
    if args.default:
        model_config = "default"
    elif args.fast:
        model_config = "fast"
    elif args.legacy:
        model_config = "legacy"
    elif args.azure_default:
        model_config = "azure_default"
    elif args.azure_fast:
        model_config = "azure_fast"

    # Initialize pipeline
    pipeline = RAGPipeline(
        data_dir=args.data_dir, model_config=model_config, file_types=args.file_types
    )

    # Load and process documents
    print(f"Loading documents from {args.data_dir}...")
    pipeline.load_documents()

    # Example queries for document comparison
    questions = [
        "Compare all versions of the Project Overview document. What are the key differences between versions?",
        "Which version of the Technical Specification is more recent, and what major changes were made?",
        "List all documents that appear to be different versions of the same content, ordered by date.",
        "Identify any documents that could be considered outdated and should be archived, explaining why.",
    ]

    # Query the documents using selected configuration
    print(f"\n{'='*80}")
    print(f"Using {pipeline.collection_name} pipeline ({model_config} configuration)")
    print(f"{'='*80}")
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 80)
        response = pipeline.query(question)
        print(f"Answer: {response}")


if __name__ == "__main__":
    main()
