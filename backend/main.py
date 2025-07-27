import os
import uuid
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import Config
from models import (
    ChatRequest, ChatResponse, UploadResponse, 
    HealthResponse, ErrorResponse, ClearMemoryResponse
)
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from vector_search_service import VectorSearchService
from llm_service import LLMService

# Initialize FastAPI app
app = FastAPI(
    title="PDF Chat API",
    description="A FastAPI backend for PDF document chat using LangChain and OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
pdf_processor = None
vector_store = None
vector_search_service = None
llm_service = None

def get_pdf_processor():
    global pdf_processor
    if pdf_processor is None:
        pdf_processor = PDFProcessor()
    return pdf_processor

def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store

def get_vector_search_service():
    global vector_search_service
    if vector_search_service is None:
        vector_store = get_vector_store()
        vector_search_service = VectorSearchService(vector_store)
    return vector_search_service

def get_llm_service():
    global llm_service
    if llm_service is None:
        vector_store = get_vector_store()
        llm_service = LLMService(vector_store)
    return llm_service

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Initialize services
        get_pdf_processor()
        get_vector_store()
        get_vector_search_service()
        # Note: LLM service is not initialized by default to save memory
        print("All services initialized successfully")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_collection_stats()
        
        return HealthResponse(
            status="healthy",
            message="PDF Chat API is running",
            vector_store_stats=stats
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"Service error: {str(e)}",
            vector_store_stats={}
        )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_collection_stats()
        
        return HealthResponse(
            status="healthy",
            message="All services are operational",
            vector_store_stats=stats
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"Health check failed: {str(e)}",
            vector_store_stats={}
        )

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    pdf_processor: PDFProcessor = Depends(get_pdf_processor),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Upload and process a PDF file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > Config.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size too large")
        
        # Process PDF
        result = pdf_processor.process_pdf(file_content, file.filename)
        
        # Add to vector store
        chunk_ids = vector_store.add_documents(result["chunks"])
        
        return UploadResponse(
            message="PDF uploaded and processed successfully",
            file_id=result["metadata"]["file_id"],
            filename=file.filename,
            num_chunks=result["num_chunks"],
            file_path=result["file_path"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    vector_search_service: VectorSearchService = Depends(get_vector_search_service)
):
    """Search and retrieve relevant content from the uploaded PDF"""
    try:
        # Use vector search by default (memory efficient)
        response = vector_search_service.search_and_summarize(request.question)
        
        return ChatResponse(
            answer=response["answer"],
            citations=response["citations"],
            question=request.question,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting search response: {str(e)}")

@app.post("/chat/llm", response_model=ChatResponse)
async def chat_with_llm(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """Chat with LLM about the uploaded PDF (uses more memory)"""
    try:
        # Get response from LLM service
        response = llm_service.get_response(request.question)
        
        return ChatResponse(
            answer=response["answer"],
            citations=response["citations"],
            question=request.question,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting LLM response: {str(e)}")

@app.post("/clear-memory", response_model=ClearMemoryResponse)
async def clear_memory(
    session_id: str = None,
    vector_search_service: VectorSearchService = Depends(get_vector_search_service)
):
    """Clear conversation memory (not needed for vector search)"""
    try:
        # Vector search doesn't maintain memory, so just return success
        return ClearMemoryResponse(
            message="Vector search service doesn't maintain conversation memory",
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/stats")
async def get_stats(vector_store: VectorStore = Depends(get_vector_store)):
    """Get vector store statistics"""
    try:
        stats = vector_store.get_collection_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.get("/debug/documents")
async def get_documents(vector_store: VectorStore = Depends(get_vector_store)):
    """Get sample documents from vector store for debugging"""
    try:
        # Get a few sample documents
        sample_docs = vector_store.vector_store.get()
        
        # Extract document content
        documents = []
        if sample_docs and 'documents' in sample_docs:
            for i, doc in enumerate(sample_docs['documents'][:5]):  # First 5 documents
                documents.append({
                    "id": i,
                    "content": doc[:500] + "..." if len(doc) > 500 else doc,
                    "metadata": sample_docs.get('metadatas', [{}])[i] if 'metadatas' in sample_docs else {}
                })
        
        return {
            "total_documents": len(sample_docs.get('documents', [])) if sample_docs else 0,
            "sample_documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting documents: {str(e)}")

@app.delete("/clear-documents")
async def clear_documents(vector_store: VectorStore = Depends(get_vector_store)):
    """Clear all documents from vector store"""
    try:
        vector_store.clear_collection()
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    ) 