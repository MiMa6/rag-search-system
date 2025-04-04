"""
Document loading component for the RAG pipeline.
"""

from pathlib import Path
from typing import List, Optional

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.readers.file import PDFReader, DocxReader

from .config import get_file_types


class DataLoader:
    """Handle document loading and processing."""

    def __init__(
        self,
        data_dir: str = "data",
        file_types: str = "default",
    ):
        """
        Initialize the data loader.

        Args:
            data_dir (str): Directory containing the documents
            file_types (str): Name of the file types configuration to use
        """
        self.data_dir = Path(data_dir)
        self.file_types = get_file_types(file_types)

    def load_documents(self, file_types: Optional[List[str]] = None) -> List[Document]:
        """
        Load documents from the data directory.

        Args:
            file_types: Optional list of file extensions to include (overrides config)

        Returns:
            List[Document]: Loaded documents
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
        print(f"Loaded {len(documents)} documents from {self.data_dir}")
        return documents
