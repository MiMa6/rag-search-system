#!/usr/bin/env python
"""
Example script to generate test documents for the RAG pipeline.

This is step 1 in the RAG workflow - generating test documents.
"""

import sys
import os

# Import the test document generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.synthetic_data.generate_test_docs import main as generate_docs

if __name__ == "__main__":
    print("Step 1: Generating test documents...")
    generate_docs()
    print("Test documents generated successfully!")
    print("Documents are stored in rag_pipeline/data/test_docs/")
    print("\nNext step: Run 'python example_create_index.py' to create the index.")
