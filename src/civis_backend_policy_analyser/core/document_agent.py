import uuid
import fitz
from loguru import logger

from langchain_text_splitters import RecursiveCharacterTextSplitter

from civis_backend_policy_analyser.core.model import get_rag_chain
from civis_backend_policy_analyser.core.vector_db_store import VectorDB


class DocumentAgent:
    """
    DocumentAgent orchestrates the full document processing workflow:
    - PDF ingestion and extraction
    - Semantic and agentic chunking
    - Vector storage with PGVector
    - DeepSeek-based summarization and assessment
    - Cleanup operations

    Attributes:
        vector_store (VectorDB): Backend PGVector client
        doc_chunks (dict): Cached document chunks by doc ID
        doc_raw_text (dict): Cached raw document content by doc ID
    """
    def __init__(self, document_id = None):
        """
        Instantiating a DocumentAgent to create a content or run the queries on the content.

        Args:
            document_id (str): Value is based on the request type.
                - If user is querying on the data then `document_id` should be present.
                - If user is creating external data soure, then it'll return the generate the `document_id`.

        """
        self.document_id = str(uuid.uuid4()) if not document_id else document_id
        self.vector_store = VectorDB(self.document_id)

    async def load_and_chunk(self, upload_file):
        """
        Ingests a document upload, extracts the text, chunks it, and stores vectors.

        Args:
            upload_file (UploadFile): A FastAPI file upload object (PDF)

        Returns:
            str: Unique document ID for downstream retrieval

        """
        content = await upload_file.read()
        text = self.__extract_text_from_pdf(content)
        logger.info(f"Document content extraction done.")
        
        document_chunks = self.__chunk_document(text)
        self.vector_store.store_embedding(document_chunks)
        logger.info("Document chunks has been embedded successfully to the vector store.")
        return {"document_id": self.document_id}

    def __extract_text_from_pdf(file_bytes):
        """
        Extracts plain text from a binary PDF file.

        Args:
            file_bytes (bytes): Raw PDF content

        Returns:
            str: Full extracted text from all pages
        """
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)

    def __chunk_document(text):
        """
        Performs semantic and recursive chunking of document text.

        Args:
            text (str): Full document content

        Returns:
            list: List of individual text chunks
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = splitter.split_text(text)
        logger.info(f"Documents have been splitted in to {len(chunks)} chunks.")
        return chunks

    def summarize(self, summary_prompt: str = "Summarize this:"):
        """
        Summarizes all the chunks associated with a document.

        Returns:
            str: Combined LLM-generated summary
        """
        rag_chain = get_rag_chain(self.vector_store.retriever)
        result = rag_chain.run(summary_prompt)
        return result

    def assess(self, prompts: list[str]):
        """
        Performs retrieval-based assessment for each prompt.

        Returns:
            dict: Prompt → generated output
        """
        rag_chain = get_rag_chain(self.vector_store.retriever)
        return {prompt: rag_chain.run(prompt) for prompt in prompts}

    def cleanup(self):
        """
        Deletes all associated vector data and cache from memory/storage.

        Args:
            doc_id (str): Identifier of the document to remove
        """
        self.vector_store.delete_all_vectors()
