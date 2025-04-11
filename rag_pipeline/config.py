"""
Configuration settings for the RAG pipeline.

This module provides configuration management for the RAG pipeline, including:
- Model configurations for both OpenAI and Azure OpenAI
- File type handling configurations
- ChromaDB storage settings
- Query engine settings

Environment Variables Required:
----------------------------
For OpenAI:
    - OPENAI_API_KEY: Your OpenAI API key

For Azure OpenAI:
    - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
    - Update api_base in azure configurations with your Azure OpenAI endpoint

```
"""

from typing import Dict, List, Literal

# Provider types
ProviderType = Literal["openai", "azure"]

# Model configurations
MODEL_CONFIGS: Dict[str, Dict[str, str]] = {
    # OpenAI configurations
    "default": {
        "provider": "openai",
        "llm_model": "gpt-4o",
        "embedding_model": "text-embedding-3-large",
    },
    "fast": {
        "provider": "openai",
        "llm_model": "gpt-4",
        "embedding_model": "text-embedding-3-small",
    },
    "legacy": {
        "provider": "openai",
        "llm_model": "gpt-3.5-turbo",
        "embedding_model": "text-embedding-3-small",
    },
    # Azure OpenAI configurations
    "azure_default": {
        "provider": "azure",
        "llm_model": "gpt-4",  # Azure deployment name
        "embedding_model": "text-embedding-ada-002",  # Azure deployment name
        "api_base": "YOUR_AZURE_OPENAI_ENDPOINT",
        "api_version": "2024-02-15-preview",
    },
    "azure_fast": {
        "provider": "azure",
        "llm_model": "gpt-35-turbo",  # Azure deployment name
        "embedding_model": "text-embedding-ada-002",  # Azure deployment name
        "api_base": "YOUR_AZURE_OPENAI_ENDPOINT",
        "api_version": "2024-02-15-preview",
    },
}

# File type configurations
FILE_TYPES: Dict[str, List[str]] = {
    "default": [".pdf", ".docx", ".txt", ".md"],
    "text_only": [".txt", ".md"],
    "documents": [".pdf", ".docx"],
}

# ChromaDB configuration
CHROMA_CONFIG = {
    "collection_prefix": "rag_collection",
    "persist_directory": "data/chroma_db",
    "anonymized_telemetry": False,
}

# Query configuration
QUERY_CONFIG = {
    "default_response_mode": "compact",
    "supported_response_modes": ["compact", "refine", "tree_summarize"],
}

# Node parser configuration
NODE_PARSER_CONFIG = {
    "chunk_size": 512,  # Smaller chunk size for more granular splitting
    "chunk_overlap": 50,  # Overlap to maintain context between chunks
    "separator": " ",  # Split on spaces if no sentence boundaries found
}


def get_model_config(config_name: str = "default") -> Dict[str, str]:
    """
    Get the model configuration for the specified name.

    Args:
        config_name: Name of the configuration to use. Options are:
            - OpenAI: "default", "fast", "legacy"
            - Azure OpenAI: "azure_default", "azure_fast"

    Returns:
        Dict containing model settings including:
            - provider: "openai" or "azure"
            - llm_model: Model name/deployment name
            - embedding_model: Embedding model name/deployment name
            - api_base: Azure OpenAI endpoint (for Azure configs)
            - api_version: Azure OpenAI API version (for Azure configs)

    Raises:
        ValueError: If the configuration name is not recognized
    """
    if config_name not in MODEL_CONFIGS:
        raise ValueError(f"Unknown model configuration: {config_name}")
    return MODEL_CONFIGS[config_name]


def get_file_types(config_name: str = "default") -> List[str]:
    """
    Get the file types configuration for the specified name.

    Args:
        config_name: Name of the configuration to use. Options are:
            - "default": All supported file types
            - "text_only": Text and markdown files
            - "documents": PDF and DOCX files

    Returns:
        List of file extensions

    Raises:
        ValueError: If the configuration name is not recognized
    """
    if config_name not in FILE_TYPES:
        raise ValueError(f"Unknown file types configuration: {config_name}")
    return FILE_TYPES[config_name]
