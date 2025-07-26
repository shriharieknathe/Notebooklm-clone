# Backend Installation

## Quick Setup

### Prerequisites
- Python (v3.8 or higher)

### Installation Steps

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API token**
   - Edit `config.py` and add your HuggingFace API token
   - Or set environment variable: `HUGGINGFACE_API_TOKEN=your_token_here`

5. **Start the server**
   ```bash
   python run.py
   ```

6. **Verify installation**
   - Server runs on http://localhost:8000
   - API docs at http://localhost:8000/docs

### Troubleshooting

- **Import errors**: Ensure virtual environment is activated
- **Port 8000 in use**: Kill existing process or use different port
- **API token errors**: Verify HuggingFace token is valid
- **Memory issues**: Reduce MAX_TOKENS in config.py 