# PDF Chat Application

A modern web application that allows users to upload PDF documents and interact with them through an AI-powered chat interface. Built with React frontend and Python FastAPI backend.

## 🚀 Features

- **PDF Upload & Viewing**: Upload and view PDF documents with built-in PDF viewer
- **AI Chat Interface**: Ask questions about your PDF content using AI
- **Resizable Layout**: Drag to resize chat and PDF panels
- **Citation System**: Click on citations to navigate to specific PDF pages
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Vector Database**: Efficient document search using ChromaDB
- **Modern UI**: Clean, professional interface with smooth animations

## 🏗️ Architecture

- **Frontend**: React.js with modern CSS and responsive design
- **Backend**: Python FastAPI with LangChain for AI processing
- **Database**: ChromaDB for vector storage
- **AI Model**: HuggingFace T5 model for question answering
- **PDF Processing**: PyPDF for document text extraction

## 📁 Project Structure

```
Notebooklm-clone/
├── frontend/          # React frontend application
├── backend/           # Python FastAPI backend
├── setup.md          # Detailed setup instructions
└── README.md         # This file
```

## 🚀 Quick Installation

### Prerequisites
- Node.js (v16+) and Python (v3.8+)

### Setup
```bash
# Clone and setup backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Start both servers
# Terminal 1: cd backend && python run.py
# Terminal 2: cd frontend && npm start
```

### Configure
- Add HuggingFace API token to `backend/config.py`
- Open http://localhost:3000

## 📖 Detailed Setup

For detailed setup instructions, see [setup.md](setup.md)

## 🎯 Usage

1. **Upload a PDF**: Drag and drop or click to upload a PDF document
2. **Wait for Processing**: The system will extract text and create embeddings
3. **Start Chatting**: Ask questions about your document content
4. **Navigate with Citations**: Click on page citations to jump to specific pages
5. **Resize Panels**: Drag the divider to adjust chat and PDF panel sizes

## 🔧 Configuration

### Backend Configuration

Edit `backend/config.py` to customize:
- HuggingFace API token
- Model settings
- Server host and port
- Vector database settings

### Frontend Configuration

Edit `frontend/src/services/api.js` to change:
- Backend API URL
- Request timeouts
- Error handling

## 🛠️ Development

### Backend Development
```bash
cd backend
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

### Frontend Development
```bash
cd frontend
npm start
```

### API Testing
- Visit http://localhost:8000/docs for interactive API documentation
- Use the built-in Swagger UI to test endpoints

## 📚 API Endpoints

- `POST /upload` - Upload PDF document
- `POST /chat` - Send chat message
- `GET /health` - Check server health
- `GET /stats` - Get system statistics
- `DELETE /clear-memory` - Clear chat memory
- `DELETE /clear-documents` - Clear all documents

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check if virtual environment is activated
   - Verify all dependencies are installed
   - Check port 8000 is not in use

2. **Frontend can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in backend
   - Verify API URL in frontend

3. **PDF upload fails**
   - Check file size (max 10MB)
   - Ensure file is a valid PDF
   - Check backend logs for errors

4. **AI responses are slow**
   - First request may be slow (model loading)
   - Check HuggingFace API token is valid
   - Monitor backend logs for errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for AI framework
- [ChromaDB](https://www.trychroma.com/) for vector database
- [React](https://reactjs.org/) for frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for backend framework
- [HuggingFace](https://huggingface.co/) for AI models 