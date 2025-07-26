import os
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema.retriever import BaseRetriever

from config import Config

class VectorStore:
    def __init__(self):
        # Initialize embeddings model (using free HuggingFace model)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load existing vector store"""
        try:
            if os.path.exists(Config.CHROMA_PERSIST_DIRECTORY):
                # Load existing vector store
                self.vector_store = Chroma(
                    persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                print(f"Loaded existing vector store from {Config.CHROMA_PERSIST_DIRECTORY}")
            else:
                # Create new vector store
                self.vector_store = Chroma(
                    persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
                print(f"Created new vector store at {Config.CHROMA_PERSIST_DIRECTORY}")
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to vector store"""
        try:
            if not documents:
                return []
            
            # Add documents to vector store
            ids = self.vector_store.add_documents(documents)
            
            # Persist the vector store
            self.vector_store.persist()
            
            print(f"Added {len(documents)} documents to vector store")
            return ids
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        try:
            if not self.vector_store:
                raise Exception("Vector store not initialized")
            
            results = self.vector_store.similarity_search(query, k=k)
            return results
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            raise
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Search for similar documents with similarity scores"""
        try:
            if not self.vector_store:
                raise Exception("Vector store not initialized")
            
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
            
        except Exception as e:
            print(f"Error in similarity search with score: {e}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if not self.vector_store:
                return {"error": "Vector store not initialized"}
            
            collection = self.vector_store._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "collection_name": collection.name,
                "persist_directory": Config.CHROMA_PERSIST_DIRECTORY
            }
            
        except Exception as e:
            return {"error": f"Error getting collection stats: {e}"}
    
    def clear_collection(self):
        """Clear all documents from the vector store"""
        try:
            if self.vector_store:
                self.vector_store._collection.delete(where={})
                self.vector_store.persist()
                print("Cleared all documents from vector store")
        except Exception as e:
            print(f"Error clearing collection: {e}")
            raise
    
    def delete_documents_by_metadata(self, metadata_filter: Dict[str, Any]):
        """Delete documents based on metadata filter"""
        try:
            if self.vector_store:
                self.vector_store._collection.delete(where=metadata_filter)
                self.vector_store.persist()
                print(f"Deleted documents with metadata filter: {metadata_filter}")
        except Exception as e:
            print(f"Error deleting documents: {e}")
            raise 