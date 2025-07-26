from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    question: str = Field(..., description="The question to ask about the PDF")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The AI's response to the question")
    citations: List[Dict[str, Any]] = Field(default=[], description="Citations from the source documents")
    question: str = Field(..., description="The original question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")

class UploadResponse(BaseModel):
    message: str = Field(..., description="Upload status message")
    file_id: str = Field(..., description="Unique identifier for the uploaded file")
    filename: str = Field(..., description="Original filename")
    num_chunks: int = Field(..., description="Number of text chunks created")
    file_path: str = Field(..., description="Path where file is stored")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Health message")
    vector_store_stats: Dict[str, Any] = Field(default={}, description="Vector store statistics")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")

class ClearMemoryResponse(BaseModel):
    message: str = Field(..., description="Memory clearing status message")
    session_id: Optional[str] = Field(None, description="Session ID if applicable") 