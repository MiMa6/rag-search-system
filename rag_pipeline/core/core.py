"""
Core implementation of the RAG pipeline using LlamaIndex.
"""

import os
from pathlib import Path
from typing import List, Optional, Set

from dotenv import load_dotenv
from llama_index.core import Settings, Document
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI

from ..config import (
    get_model_config,
    get_file_types,
    QUERY_CONFIG,
)
from ..db.chroma_manager import ChromaDBManager
from ..engine.data_loader import DataLoader

# Load environment variables
load_dotenv()


class RAGPipeline:
    def __init__(
        self,
        data_dir: str = "data",
        collection_name: Optional[str] = None,
        model_config: str = "default",
        file_types: str = "default",
    ):
        """
        Initialize the RAG pipeline.

        Args:
            data_dir (str): Directory containing the documents
            collection_name (str): Name for the ChromaDB collection (optional)
            model_config (str): Name of the model configuration to use
            file_types (str): Name of the file types configuration to use
        """
        self.data_dir = Path(data_dir)
        self.file_types = get_file_types(file_types)
        self.collection_name = collection_name

        # Initialize components
        self.data_loader = DataLoader(
            data_dir=str(self.data_dir),
            file_types=file_types,
        )

        # Get model configuration for LLM setup
        model_settings = get_model_config(model_config)
        self.provider = model_settings["provider"]
        self.model_name = model_settings["llm_model"]

        # Initialize ChromaDB manager
        self.chroma_manager = ChromaDBManager(
            collection_name=collection_name,
            model_config=model_config,
        )

        # Setup LLM based on provider
        if self.provider == "azure":
            self.llm = AzureOpenAI(
                model=self.model_name,
                deployment_name=self.model_name,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
        else:
            self.llm = OpenAI(model=self.model_name)

        # Set global LLM
        Settings.llm = self.llm

        self.index = None
        self._processed_files: Set[str] = set()

    def load_documents(self, file_types: Optional[List[str]] = None) -> None:
        """
        Load documents from the data directory. If a collection exists in Chroma,
        it will load the existing index instead of reprocessing the documents.

        Args:
            file_types: Optional list of file extensions to include (overrides config)
        """
        # Try to load existing index first
        doc_count = self.chroma_manager.get_document_count()
        if doc_count > 0:
            print(f"Loading existing index with {doc_count} documents...")
            self.index = self.chroma_manager.get_existing_index()
            return

        # If no existing index, load and process documents
        documents = self.data_loader.load_documents(file_types)
        if documents:
            self.index = self.chroma_manager.create_index(documents)

    def query(self, question: str, response_mode: str = None) -> str:
        """
        Query the RAG pipeline.

        Args:
            question: The question to ask
            response_mode: Response mode (optional, defaults to config setting)

        Returns:
            str: The response from the model
        """
        if not self.index:
            raise ValueError(
                "No documents have been loaded. Call load_documents() first."
            )

        if response_mode is None:
            response_mode = QUERY_CONFIG["default_response_mode"]
        elif response_mode not in QUERY_CONFIG["supported_response_modes"]:
            raise ValueError(f"Unsupported response mode: {response_mode}")

        query_engine = self.index.as_query_engine(
            response_mode=response_mode,
        )
        response = query_engine.query(question)
        return str(response)

    def delete_index(self) -> None:
        """Delete the current index and its collection."""
        self.chroma_manager.delete_collection()
        self.index = None

    @property
    def supported_file_types(self) -> List[str]:
        """Get list of supported file types."""
        return self.data_loader.supported_extensions
