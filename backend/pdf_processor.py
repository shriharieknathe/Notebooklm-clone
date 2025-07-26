import os
import uuid
from typing import List, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

from config import Config

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        # Create upload directory if it doesn't exist
        os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """Save uploaded file to disk and return the file path"""
        file_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix.lower()
        
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            raise ValueError(f"File type {file_extension} not allowed")
        
        file_path = os.path.join(Config.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return file_path
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file using PyPDFLoader"""
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Combine all pages into a single text
            full_text = ""
            for page in pages:
                full_text += page.page_content + "\n"
            
            return full_text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def split_text_into_chunks(self, text: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Split text into chunks for vector storage"""
        try:
            # Create a document with metadata
            doc = Document(page_content=text, metadata=metadata or {})
            
            # Split the document into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            return chunks
        except Exception as e:
            raise Exception(f"Error splitting text into chunks: {str(e)}")
    
    def process_pdf(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Complete PDF processing pipeline"""
        try:
            # Save file
            file_path = self.save_uploaded_file(file_content, filename)
            
            # Extract text
            text = self.extract_text_from_pdf(file_path)
            
            # Create metadata
            metadata = {
                "filename": filename,
                "file_path": file_path,
                "file_id": Path(file_path).stem,
                "source": "pdf_upload"
            }
            
            # Split into chunks
            chunks = self.split_text_into_chunks(text, metadata)
            
            return {
                "file_path": file_path,
                "text": text,
                "chunks": chunks,
                "metadata": metadata,
                "num_chunks": len(chunks)
            }
            
        except Exception as e:
            # Clean up file if processing fails
            if 'file_path' in locals():
                try:
                    os.remove(file_path)
                except:
                    pass
            raise e
    
    def cleanup_file(self, file_path: str):
        """Remove temporary file after processing"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}") 