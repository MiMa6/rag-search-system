"""
Example usage of the RAG pipeline for document comparison.
"""

from rag_pipeline.core import RAGPipeline


def main():
    # Initialize the RAG pipeline with test documents
    rag = RAGPipeline(
        data_dir="rag_pipeline/data/test_docs",
        collection_name="test_documents",
        model_name="gpt-3.5-turbo",
    )

    # Load and index documents
    rag.load_documents()

    # Example queries for document comparison
    questions = [
        "Compare all versions of the Project Overview document. What are the key differences between versions?",
        "Which version of the Technical Specification is more recent, and what major changes were made?",
        "List all documents that appear to be different versions of the same content, ordered by date.",
        "Identify any documents that could be considered outdated and should be archived, explaining why.",
    ]

    # Query the documents
    for question in questions:
        print("\n" + "=" * 80)
        print(f"Question: {question}")
        print("-" * 80)
        response = rag.query(question)
        print(f"Answer: {response}")


if __name__ == "__main__":
    main()
