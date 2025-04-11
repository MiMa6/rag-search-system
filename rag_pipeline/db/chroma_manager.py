"""
ChromaDB collection management for the RAG pipeline.
"""

import os
from typing import List, Optional

from llama_index.core import Settings, StorageContext, VectorStoreIndex, Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from ..config import get_model_config, CHROMA_CONFIG, NODE_PARSER_CONFIG


class ChromaDBManager:
    """Handle ChromaDB collection management and vector store operations."""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        model_config: str = "default",
    ):
        """
        Initialize the ChromaDB manager.

        Args:
            collection_name (str): Name for the ChromaDB collection (optional)
            model_config (str): Name of the model configuration to use
        """
        # Get model configuration for embedding setup
        model_settings = get_model_config(model_config)
        self.provider = model_settings["provider"]
        self.embedding_model = model_settings["embedding_model"]

        # Setup collection name
        if collection_name is None:
            collection_name = f"{CHROMA_CONFIG['collection_prefix']}_{model_config}"
        self.collection_name = collection_name

        # Initialize ChromaDB components
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_CONFIG["persist_directory"]
        )
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # Setup embedding model based on provider
        if self.provider == "azure":
            self.embed_model = AzureOpenAIEmbedding(
                model=self.embedding_model,
                deployment_name=self.embedding_model,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
        else:
            self.embed_model = OpenAIEmbedding(
                model=self.embedding_model, mode=OpenAIEmbeddingMode.SIMILARITY_MODE
            )

        # Set global settings for embedding and node parsing
        Settings.embed_model = self.embed_model
        Settings.node_parser = SentenceSplitter(**NODE_PARSER_CONFIG)

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

    def get_existing_index(self) -> Optional[VectorStoreIndex]:
        """
        Load an existing index from the persistent store.

        Returns:
            VectorStoreIndex: The loaded index, or None if collection doesn't exist or is empty
        """
        if self.collection_name not in [
            c.name for c in self.chroma_client.list_collections()
        ]:
            return None

        if self.chroma_collection.count() == 0:
            return None

        return VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
        )

    def get_document_count(self) -> int:
        """
        Get the number of documents in the collection.

        Returns:
            int: Number of documents in the collection
        """
        return self.chroma_collection.count()

    def delete_collection(self) -> None:
        """Delete the current collection."""
        self.chroma_client.delete_collection(self.collection_name)
        print(f"Deleted collection '{self.collection_name}'")
