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
    from rag_pipeline.query_engine import RAGQueryEngine
except ImportError as e:
    logger.error(f"Failed to import RAGQueryEngine: {e}")
    raise


class RAGHandler:
    """Handler for RAG queries"""

    def __init__(self, collection_name: str = "test_docs_eng_2"):
        """Initialize the RAG handler with specified collection"""
        self.collection_name = collection_name
        self._query_engine = None

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
    if len(sys.argv) > 1:
        handler = RAGHandler()
        result = handler.handle_query(sys.argv[1])
        # Print as JSON string for the Node.js server to parse
        print(json.dumps(result))
