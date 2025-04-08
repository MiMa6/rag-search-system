"""
ChromaDB collection management for the RAG pipeline.
"""

import os
from typing import List

from llama_index.core import Settings, StorageContext, VectorStoreIndex, Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from ..config import get_model_config, CHROMA_CONFIG


class ChromaDBManager:
    """Handle ChromaDB collection management."""

    def __init__(
        self,
        collection_name: str = None,
        model_config: str = "default",
    ):
        """
        Initialize the ChromaDB manager.

        Args:
            collection_name (str): Name for the ChromaDB collection (optional)
            model_config (str): Name of the model configuration to use
        """
        # Get model configuration
        model_settings = get_model_config(model_config)
        self.provider = model_settings["provider"]
        self.model_name = model_settings["llm_model"]
        self.embedding_model = model_settings["embedding_model"]
        self.model_config = model_config

        # Setup collection name
        if collection_name is None:
            collection_name = f"{CHROMA_CONFIG['collection_prefix']}_{model_config}"
        self.collection_name = collection_name

        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_CONFIG["persist_directory"]
        )
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )

        # Setup vector store
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # Setup embedding based on provider
        if self.provider == "azure":
            # Azure OpenAI setup
            self.embed_model = AzureOpenAIEmbedding(
                model=self.embedding_model,
                deployment_name=self.embedding_model,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
        else:
            # OpenAI setup
            self.embed_model = OpenAIEmbedding(
                model=self.embedding_model, mode=OpenAIEmbeddingMode.SIMILARITY_MODE
            )

        # Set global embedding model
        Settings.embed_model = self.embed_model
        Settings.node_parser = SentenceSplitter()

    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Create or update the vector index with documents.

        Args:
            documents: List of documents to index

        Returns:
            VectorStoreIndex: The created index
        """
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
        )
        print(
            f"Created index for {len(documents)} documents in collection '{self.collection_name}'"
        )
        return index

    def get_existing_index(self) -> VectorStoreIndex:
        """
        Load an existing index from the persistent store.

        Returns:
            VectorStoreIndex: The loaded index
        """
        # Check if the collection exists and has documents
        collections = [c.name for c in self.chroma_client.list_collections()]
        if self.collection_name not in collections:
            print(f"\nError: Collection '{self.collection_name}' does not exist.")
            print(
                "\nTip: Run 'python example_create_index.py' to create an index first."
            )
            return None

        # Check if collection has documents
        collection = self.chroma_client.get_collection(self.collection_name)
        if collection.count() == 0:
            print(
                f"\nError: Collection '{self.collection_name}' exists but has no documents."
            )
            print(
                "\nTip: Run 'python example_create_index.py' to create an index with documents."
            )
            return None

        # Use the VectorStoreIndex.from_vector_store method instead
        # This properly reconstructs the index from the vector store
        return VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
        )
