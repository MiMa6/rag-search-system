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

    parser.add_argument(
        "--collection-name",
        type=str,
        default="rag_pipeline/data/test_docs",
        help="Collection name",
    )

    # Add flag to make progam interactive and user input instead of using example queistons
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run the program in interactive mode",
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
        data_dir=args.data_dir,
        collection_name=args.collection_name,
        model_config=model_config,
        file_types=args.file_types,
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

    print(f"\n{'='*80}")
    print(f"Using {pipeline.collection_name} pipeline ({model_config} configuration)")
    print(f"{'='*80}")

    if args.interactive:
        while True:
            user_question = input("\nEnter your question (or 'quit' to exit): ").strip()
            if user_question.lower() == "quit":
                break
            if not user_question:
                continue
            print("-" * 80)
            response = pipeline.query(user_question)
            print(f"Answer: {response}")
    else:
        for question in questions:
            print(f"\nQuestion: {question}")
            print("-" * 80)
            response = pipeline.query(question)
            print(f"Answer: {response}")


if __name__ == "__main__":
    main()
