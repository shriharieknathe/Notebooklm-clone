# Backend - PDF Chat Application

Python FastAPI backend for the PDF Chat Application with AI-powered document processing, vector database storage, and RESTful API endpoints.

## 🚀 Features

- **FastAPI Framework**: High-performance async web framework
- **PDF Processing**: Extract text from PDF documents using PyPDF
- **Vector Database**: ChromaDB for efficient document search and retrieval
- **AI Integration**: HuggingFace T5 model for question answering
- **RAG System**: Retrieval-Augmented Generation for accurate responses
- **File Upload**: Handle PDF file uploads with validation
- **Chat Memory**: Maintain conversation context
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **CORS Support**: Cross-origin resource sharing for frontend integration


## 🚀 Quick Installation

### Prerequisites
- Python (v3.8+)

### Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Configure
- Add HuggingFace API token to `config.py`
- Server runs on http://localhost:8000

## 🎯 Usage

### Development Server

```bash
# Start development server with auto-reload
python run.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Endpoints

### Core Endpoints

- **`POST /upload`** - Upload PDF document
  - Accepts multipart form data with PDF file
  - Returns processing status and document info

- **`POST /chat`** - Send chat message
  - Accepts JSON with question text
  - Returns AI response with citations

- **`GET /health`** - Health check
  - Returns server status and basic info

### Utility Endpoints

- **`GET /stats`** - System statistics
  - Returns document count, memory usage, etc.

- **`DELETE /clear-memory`** - Clear chat memory
  - Clears conversation history

- **`DELETE /clear-documents`** - Clear all documents
  - Removes all uploaded PDFs and vectors

- **`GET /debug/documents`** - Debug endpoint
  - Returns sample documents from vector store

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend directory:

```env
HUGGINGFACE_API_TOKEN=your_token_here
MODEL_NAME=google/flan-t5-base
MAX_TOKENS=512
TEMPERATURE=0.7
```

### Configuration File

Edit `config.py` to customize:

```python
class Config:
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8000
    
    # HuggingFace settings
    HUGGINGFACE_API_TOKEN = "your_token_here"
    MODEL_NAME = "google/flan-t5-base"
    
    # LLM settings
    TEMPERATURE = 0.7
    MAX_TOKENS = 512
    MAX_LENGTH = 512
    
    # Vector database settings
    CHROMA_PERSIST_DIRECTORY = "./chroma_db"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # File upload settings
    UPLOAD_DIR = "./uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

## 🏗️ Architecture

### Components

1. **PDF Processor** (`pdf_processor.py`)
   - Handles PDF file uploads
   - Extracts text content
   - Splits text into chunks
   - Manages file storage

2. **Vector Store** (`vector_store.py`)
   - ChromaDB integration
   - Document embedding
   - Similarity search
   - Vector storage management

3. **LLM Service** (`llm_service.py`)
   - HuggingFace model integration
   - RAG (Retrieval-Augmented Generation)
   - Response generation
   - Citation processing

4. **API Layer** (`main.py`)
   - FastAPI application
   - Endpoint definitions
   - Request/response handling
   - Error management

### Data Flow

1. **PDF Upload**: File → Text Extraction → Chunking → Vector Embedding → Storage
2. **Chat Query**: Question → Vector Search → Context Retrieval → AI Generation → Response
3. **Citation**: Page Reference → PDF Navigation → User Interface

## 🎨 Features

### PDF Processing
- **Text Extraction**: Extract text from PDF documents
- **Chunking**: Split text into manageable chunks
- **Metadata**: Store page numbers and file information
- **Validation**: File type and size validation

### AI Integration
- **RAG System**: Retrieval-Augmented Generation
- **Context Awareness**: Use document content for responses
- **Citation Generation**: Link responses to source pages
- **Memory Management**: Maintain conversation context

### Vector Database
- **Efficient Search**: Fast similarity search
- **Persistence**: Store vectors on disk
- **Metadata**: Rich document metadata
- **Scalability**: Handle multiple documents

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

2. **Port already in use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000  # macOS/Linux
   netstat -ano | findstr :8000  # Windows
   
   # Kill the process or use different port
   uvicorn main:app --port 8001
   ```

3. **HuggingFace API errors**
   - Verify API token is valid
   - Check internet connection
   - Ensure model name is correct

4. **Memory issues**
   - Reduce `MAX_TOKENS` in config
   - Use smaller model
   - Clear memory regularly

### Debug Mode

Enable debug logging:

```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Check

Test server health:

```bash
curl http://localhost:8000/health
```

## 🚀 Deployment

### Production Setup

1. **Install production dependencies**
   ```bash
   pip install gunicorn uvicorn[standard]
   ```

2. **Create production config**
   ```python
   # production_config.py
   HOST = "0.0.0.0"
   PORT = 8000
   WORKERS = 4
   ```

3. **Start with Gunicorn**
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- `HUGGINGFACE_API_TOKEN` - Your HuggingFace API token
- `HOST` - Server host (0.0.0.0 for production)
- `PORT` - Server port
- `CHROMA_PERSIST_DIRECTORY` - Vector database path
- `UPLOAD_DIR` - File upload directory

## 📊 Monitoring

### Logs
- Application logs in console
- Error tracking and debugging
- Performance monitoring

### Metrics
- Request/response times
- Memory usage
- Document count
- API usage statistics

## 🔒 Security

### Best Practices
- Use HTTPS in production
- Validate file uploads
- Rate limiting
- Input sanitization
- Environment variable management

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [LangChain](https://langchain.com/) for AI integration
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [HuggingFace](https://huggingface.co/) for AI models 