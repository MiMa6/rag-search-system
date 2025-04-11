import os
import sys
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path so we can import rag_pipeline
current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent.parent
sys.path.append(str(root_dir))

try:
    from rag_pipeline.engine.query_engine import RAGQueryEngine
except ImportError as e:
    logger.error(f"Failed to import RAGQueryEngine: {e}")
    raise


class RAGHandler:
    """Handler for RAG queries"""

    def __init__(self, collection_name: str = "test_colection"):
        """Initialize the RAG handler with specified collection"""
        self.collection_name = collection_name
        self._query_engine = None

    @staticmethod
    def list_collections() -> dict:
        """
        List all available collections in ChromaDB

        Returns:
            dict: Response containing success status and list of collections
        """
        try:
            # Change to the root directory to ensure ChromaDB can find its files
            os.chdir(root_dir)
            from rag_pipeline.engine.query_engine import get_chroma_client

            client = get_chroma_client()
            collections = client.list_collections()
            collection_names = [col.name for col in collections]

            logger.info(f"Found collections: {collection_names}")
            return {"success": True, "collections": collection_names}
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            return {"success": False, "error": str(e)}

    @property
    def query_engine(self):
        """Lazy initialization of query engine"""
        if self._query_engine is None:
            try:
                # Change to the root directory to ensure ChromaDB can find its files
                os.chdir(root_dir)
                logger.info(
                    f"Initializing RAGQueryEngine with collection: {self.collection_name}"
                )
                self._query_engine = RAGQueryEngine(
                    collection_name=self.collection_name, model_config="default"
                )
            except Exception as e:
                logger.error(f"Failed to initialize RAGQueryEngine: {e}")
                raise
        return self._query_engine

    def handle_query(self, question: str) -> dict:
        """
        Handle a query and return structured response

        Args:
            question: The question to process

        Returns:
            dict: Response containing success status and either response or error message
        """
        try:
            logger.info(f"Processing question: {question}")
            response = self.query_engine.query(question)
            return {"success": True, "response": str(response)}
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {"success": False, "error": str(e)}


# For command line testing
if __name__ == "__main__":
    if len(sys.argv) > 2:  # Check for both question and collection
        question = sys.argv[1]
        collection = sys.argv[2]
        handler = RAGHandler(collection_name=collection)
        result = handler.handle_query(question)
        print(json.dumps(result))
    else:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "Both question and collection name are required",
                }
            )
        )
