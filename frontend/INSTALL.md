# Frontend Installation

## Quick Setup

### Prerequisites
- Node.js (v16 or higher)

### Installation Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the application**
   ```bash
   npm start
   ```

4. **Access the app**
   - Opens automatically at http://localhost:3000
   - Or manually navigate to http://localhost:3000

### Troubleshooting

- **Port 3000 in use**: Change port in package.json or kill existing process
- **Installation fails**: Clear npm cache with `npm cache clean --force`
- **Can't connect to backend**: Ensure backend is running on port 8000 