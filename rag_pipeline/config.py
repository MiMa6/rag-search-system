"""
Configuration settings for the RAG pipeline.
"""

from typing import Dict, List

# OpenAI model configurations
MODEL_CONFIG = {
    "default": {
        "llm_model": "gpt-4",
        "embedding_model": "text-embedding-3-small",
    },
    "legacy": {
        "llm_model": "gpt-3.5-turbo",
        "embedding_model": "text-embedding-ada-002",
    },
    "balanced": {
        "llm_model": "gpt-4",
        "embedding_model": "text-embedding-ada-002",
    },
}

# Supported file types and their readers
FILE_TYPES = {
    "default": [".pdf", ".txt", ".docx", ".md"],
    "text_only": [".txt", ".md"],
    "documents": [".pdf", ".docx"],
}

# ChromaDB settings
CHROMA_CONFIG = {
    "persist_directory": "./chroma_db",
    "collection_prefix": "rag_documents",
}

# Query engine settings
QUERY_CONFIG = {
    "default_response_mode": "compact",
    "supported_response_modes": ["compact", "tree_summarize"],
}


def get_model_config(config_name: str = "default") -> Dict[str, str]:
    """
    Get model configuration by name.

    Args:
        config_name: Name of the configuration to use

    Returns:
        Dictionary containing LLM and embedding model names
    """
    if config_name not in MODEL_CONFIG:
        raise ValueError(f"Unsupported model configuration: {config_name}")
    return MODEL_CONFIG[config_name]


def get_file_types(config_name: str = "default") -> List[str]:
    """
    Get file types configuration by name.

    Args:
        config_name: Name of the configuration to use

    Returns:
        List of supported file extensions
    """
    if config_name not in FILE_TYPES:
        raise ValueError(f"Unsupported file types configuration: {config_name}")
    return FILE_TYPES[config_name]
