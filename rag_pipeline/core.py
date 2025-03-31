"""
Core implementation of the RAG pipeline using LlamaIndex.
"""

import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import PDFReader, DocxReader
import chromadb

# Load environment variables
load_dotenv()


class RAGPipeline:
    def __init__(
        self,
        data_dir: str = "data",
        collection_name: str = "rag_documents",
        model_name: str = "gpt-3.5-turbo",
    ):
        """
        Initialize the RAG pipeline.

        Args:
            data_dir (str): Directory containing the documents
            collection_name (str): Name for the ChromaDB collection
            model_name (str): OpenAI model to use
        """
        self.data_dir = Path(data_dir)
        self.collection_name = collection_name
        self.model_name = model_name

        # Initialize components
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )

        # Setup LlamaIndex components
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # Setup embedding and LLM
        self.embed_model = OpenAIEmbedding()
        self.llm = OpenAI(model=model_name)

        # Update global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.node_parser = SentenceSplitter()

        self.index = None

    def load_documents(self, file_types: Optional[List[str]] = None) -> None:
        """
        Load documents from the data directory.

        Args:
            file_types: List of file extensions to include (e.g., [".pdf", ".txt"])
        """
        if not file_types:
            file_types = [".pdf", ".txt", ".docx", ".md"]

        reader = SimpleDirectoryReader(
            input_dir=str(self.data_dir),
            required_exts=file_types,
            file_extractor={
                ".pdf": PDFReader(),
                ".docx": DocxReader(),
            },
            recursive=True,
            exclude_hidden=True,
        )
        documents = reader.load_data()

        # Create or update the index
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
        )
        print(f"Loaded and indexed {len(documents)} documents")

    def query(self, question: str, response_mode: str = "compact") -> str:
        """
        Query the RAG pipeline.

        Args:
            question: The question to ask
            response_mode: Response mode ("compact" or "tree_summarize")

        Returns:
            str: The response from the model
        """
        if not self.index:
            raise ValueError(
                "No documents have been loaded. Call load_documents() first."
            )

        query_engine = self.index.as_query_engine(
            response_mode=response_mode,
        )
        response = query_engine.query(question)
        return str(response)
