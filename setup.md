# PDF Chat Application - Complete Setup Guide

This guide will help you set up both the frontend and backend for the PDF Chat application with LangChain integration.

## Project Structure

```
PDF Assignment/
├── frontend/          # React.js frontend
│   ├── src/
│   ├── package.json
│   └── README.md
├── backend/           # Python FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── setup.md          # This file
```

## Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **OpenAI API Key** (for AI responses)
- **Git** (optional)

## Step 1: Backend Setup

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Install Additional Dependencies
```bash
# For sentence transformers (embeddings)
pip install torch torchvision torchaudio
```

### 1.5 Create Environment File
Create a `.env` file in the backend directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
FRONTEND_URL=http://localhost:3000
```

### 1.6 Start Backend Server
```bash
python run.py
```

The backend will start on `http://localhost:8000`

**API Documentation**: http://localhost:8000/docs

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Start Frontend Development Server
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## Step 3: Testing the Application

### 3.1 Verify Backend Health
Visit: http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "message": "All services are operational",
  "vector_store_stats": {
    "total_documents": 0,
    "collection_name": "langchain",
    "persist_directory": "./chroma_db"
  }
}
```

### 3.2 Test Frontend Connection
The frontend will automatically check the backend connection on startup.

### 3.3 Upload and Chat
1. Upload a PDF file using the drag-and-drop interface
2. Wait for processing (text extraction and vector storage)
3. Start chatting with the AI about your document

## Features Available

### ✅ Backend Features
- **PDF Processing**: Text extraction and chunking
- **Vector Database**: ChromaDB with HuggingFace embeddings
- **AI Integration**: OpenAI GPT-3.5-turbo with RAG
- **API Endpoints**: Upload, chat, memory management
- **Health Monitoring**: System status and statistics

### ✅ Frontend Features
- **Real PDF Upload**: Drag-and-drop interface
- **PDF Viewer**: Display uploaded PDFs with navigation
- **Chat Interface**: Real-time AI conversations
- **Citations**: Click to navigate to source pages
- **Error Handling**: Graceful error management

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with stats |
| POST | `/upload` | Upload and process PDF |
| POST | `/chat` | Chat with AI about documents |
| POST | `/clear-memory` | Clear conversation memory |
| GET | `/stats` | Vector store statistics |
| DELETE | `/clear-documents` | Clear all documents |

## Configuration Options

### Backend Configuration (`backend/config.py`)

```python
# LLM Configuration
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# Vector Database Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### Frontend Configuration (`frontend/src/services/api.js`)

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Ensure backend is running on port 8000
   - Check firewall settings
   - Verify CORS configuration

2. **OpenAI API Error**
   - Verify API key in `.env` file
   - Check API key has sufficient credits
   - Ensure internet connection

3. **PDF Upload Fails**
   - Check file size (max 10MB)
   - Ensure file is valid PDF
   - Check backend logs for errors

4. **Vector Database Issues**
   - Delete `chroma_db` folder and restart
   - Check disk space
   - Verify write permissions

### Performance Optimization

1. **Large PDFs**: Reduce `CHUNK_SIZE` in config
2. **Memory Usage**: Use smaller embedding models
3. **Response Time**: Adjust `MAX_TOKENS` and temperature

## Free Alternative Setup

If you don't want to use OpenAI (paid), you can use free alternatives:

### Option 1: HuggingFace Inference API
```python
# In backend/llm_service.py
from langchain_community.llms import HuggingFaceHub

self.llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    huggingfacehub_api_token="your_hf_token"  # Free
)
```

### Option 2: Local Models
```bash
pip install transformers torch
```

```python
# In backend/llm_service.py
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

model = pipeline("text2text-generation", model="google/flan-t5-base")
self.llm = HuggingFacePipeline(pipeline=model)
```

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `src/components/`
3. **API**: Update `api.js` for new endpoints

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files
npx serve -s build
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review backend logs
3. Check browser console for frontend errors
4. Verify all dependencies are installed

## License

This project is created for educational purposes as a take-home assignment. 