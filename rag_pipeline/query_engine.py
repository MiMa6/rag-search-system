"""
Query engine component for the RAG pipeline.
"""

import os

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI

from .config import get_model_config, QUERY_CONFIG
from .chroma_manager import ChromaDBManager


class RAGQueryEngine:
    """Query engine for the RAG pipeline."""

    def __init__(
        self,
        collection_name: str = None,
        model_config: str = "default",
    ):
        """
        Initialize the RAG query engine.

        Args:
            collection_name (str): Name for the ChromaDB collection (optional)
            model_config (str): Name of the model configuration to use
        """
        # Get model configuration
        model_settings = get_model_config(model_config)
        self.provider = model_settings["provider"]
        self.model_name = model_settings["llm_model"]

        # Initialize ChromaDB manager to get the vector store
        self.chroma_manager = ChromaDBManager(
            collection_name=collection_name,
            model_config=model_config,
        )

        # Load existing index
        self.index = self.chroma_manager.get_existing_index()

        # Setup LLM based on provider
        if self.provider == "azure":
            # Azure OpenAI setup
            self.llm = AzureOpenAI(
                model=self.model_name,
                deployment_name=self.model_name,
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=model_settings["api_base"],
                api_version=model_settings["api_version"],
            )
        else:
            # OpenAI setup
            self.llm = OpenAI(model=self.model_name)

        # Set global LLM
        Settings.llm = self.llm

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
                "Index not loaded. Make sure the collection exists and has documents."
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
