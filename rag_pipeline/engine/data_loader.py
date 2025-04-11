"""
Document loading component for the RAG pipeline.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.readers.file import PDFReader, DocxReader

from ..config import get_file_types


class DataLoader:
    """Handle document loading and processing."""

    def __init__(
        self,
        data_dir: str = "data",
        file_types: str = "default",
        recursive: bool = False,
        exclude_hidden: bool = True,
        file_extractor: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the data loader.

        Args:
            data_dir (str): Directory containing the documents
            file_types (str): Name of the file types configuration to use
            recursive (bool): Whether to recursively search subdirectories
            exclude_hidden (bool): Whether to exclude hidden files
            file_extractor (Dict[str, Any]): Custom file extractors (optional)
        """
        self.data_dir = Path(data_dir)
        self.file_types = get_file_types(file_types)
        self.recursive = recursive
        self.exclude_hidden = exclude_hidden

        # Setup default extractors if none provided
        self.file_extractor = file_extractor or {
            ".pdf": PDFReader(),
            ".docx": DocxReader(),
        }

    def load_documents(self, file_types: Optional[List[str]] = None) -> List[Document]:
        """
        Load documents from the data directory.

        Args:
            file_types: Optional list of file extensions to include (overrides config)

        Returns:
            List[Document]: Loaded documents

        Raises:
            ValueError: If data directory doesn't exist
        """
        if not self.data_dir.exists():
            raise ValueError(f"Data directory not found: {self.data_dir}")

        if file_types is None:
            file_types = self.file_types

        # Read documents with directory reader
        reader = SimpleDirectoryReader(
            input_dir=str(self.data_dir),
            required_exts=file_types,
            file_extractor=self.file_extractor,
            recursive=self.recursive,
            exclude_hidden=self.exclude_hidden,
        )
        documents = reader.load_data()

        if not documents:
            print(
                f"Warning: No documents found in {self.data_dir} with extensions {file_types}"
            )
        else:
            print(f"Loaded {len(documents)} documents from {self.data_dir}")

        return documents

    @property
    def supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return list(self.file_extractor.keys()) if self.file_extractor else []

    def add_file_extractor(self, extension: str, extractor: Any) -> None:
        """
        Add a custom file extractor for a specific extension.

        Args:
            extension (str): File extension (e.g., '.pdf')
            extractor: The extractor instance to use for this file type
        """
        if not extension.startswith("."):
            extension = f".{extension}"
        self.file_extractor[extension] = extractor
