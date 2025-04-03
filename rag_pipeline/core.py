"""
Core implementation of the RAG pipeline using LlamaIndex.
"""

import os
from pathlib import Path
from typing import List, Optional, Set
from datetime import datetime

from dotenv import load_dotenv
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    Document,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import PDFReader, DocxReader
import chromadb

from .config import (
    get_model_config,
    get_file_types,
    CHROMA_CONFIG,
    QUERY_CONFIG,
)

# Load environment variables
load_dotenv()


class RAGPipeline:
    def __init__(
        self,
        data_dir: str = "data",
        collection_name: str = None,
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

        # Get model configuration
        model_settings = get_model_config(model_config)
        self.provider = model_settings["provider"]
        self.model_name = model_settings["llm_model"]
        self.embedding_model = model_settings["embedding_model"]

        # Get file types configuration
        self.file_types = get_file_types(file_types)

        # Setup collection name
        if collection_name is None:
            collection_name = f"{CHROMA_CONFIG['collection_prefix']}_{model_config}"
        self.collection_name = collection_name

        # Initialize components
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_CONFIG["persist_directory"]
        )
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )

        # Setup LlamaIndex components
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # Setup embedding and LLM based on provider
        if self.provider == "azure":
            # Azure OpenAI setup
            self.embed_model = AzureOpenAIEmbedding(
                model=self.embedding_model,
                deployment_name=self.embedding_model,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
            self.llm = AzureOpenAI(
                model=self.model_name,
                deployment_name=self.model_name,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
        else:
            # OpenAI setup
            self.embed_model = OpenAIEmbedding(
                model=self.embedding_model, mode=OpenAIEmbeddingMode.SIMILARITY_MODE
            )
            self.llm = OpenAI(model=self.model_name)

        # Update global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.node_parser = SentenceSplitter()

        self.index = None
        self._processed_files: Set[str] = set()

    def load_documents(self, file_types: Optional[List[str]] = None) -> None:
        """
        Load documents from the data directory.

        Args:
            file_types: Optional list of file extensions to include (overrides config)
        """
        if file_types is None:
            file_types = self.file_types

        # Read documents with directory reader
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
