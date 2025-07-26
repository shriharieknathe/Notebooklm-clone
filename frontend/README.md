# Frontend - PDF Chat Application

React-based frontend for the PDF Chat Application with modern UI, responsive design, and real-time chat functionality.

## 🚀 Features

- **Modern React App**: Built with React 18 and modern JavaScript
- **PDF Viewer**: Integrated PDF viewing with page navigation
- **Resizable Layout**: Drag to resize chat and PDF panels
- **Real-time Chat**: Interactive chat interface with AI responses
- **Citation System**: Click citations to navigate to PDF pages
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Upload Interface**: Drag-and-drop PDF upload with progress tracking
- **Error Handling**: Comprehensive error handling and user feedback

```

## 🚀 Quick Installation

### Prerequisites
- Node.js (v16+)

### Setup
```bash
cd frontend
npm install
npm start
```

### Access
- Opens automatically at http://localhost:3000

## 🎯 Usage

### Development

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject from Create React App (not recommended)
npm run eject
```

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run test suite
- `npm run eject` - Eject from Create React App

## 🔧 Configuration

### API Configuration

Edit `src/services/api.js` to configure:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Backend URL
const TIMEOUT = 30000; // Request timeout in milliseconds
```

### Environment Variables

Create `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TIMEOUT=30000
```

## 🎨 Components

### PDFUpload
- Handles PDF file selection and upload
- Drag-and-drop functionality
- Upload progress tracking
- File validation

### PDFChat
- Main chat interface component
- Manages chat state and messages
- Handles AI responses and citations
- Coordinates between chat and PDF viewer

### ChatPanel
- Displays chat messages
- Handles user input
- Shows typing indicators
- Manages message suggestions

### PDFViewer
- Renders PDF documents
- Page navigation controls
- Zoom functionality
- Citation navigation

### Message
- Individual message display
- Supports user, AI, and system messages
- Citation button handling
- Message formatting

### ResizableSplitPane
- Resizable layout component
- Drag to resize panels
- Responsive design
- Touch support for mobile

## 🎨 Styling

### CSS Architecture
- **Component-based CSS**: Each component has its own CSS file
- **Modern CSS**: Uses flexbox, grid, and CSS custom properties
- **Responsive Design**: Mobile-first approach with media queries
- **Smooth Animations**: CSS transitions and transforms

### Color Scheme
- **Primary**: Purple (#8b5cf6)
- **Secondary**: Gray (#6b7280)
- **Background**: White (#ffffff)
- **Border**: Light gray (#e5e7eb)

## 🔌 API Integration

### Backend Communication
- **Base URL**: http://localhost:8000
- **Endpoints**:
  - `POST /upload` - Upload PDF
  - `POST /chat` - Send chat message
  - `GET /health` - Health check

### Error Handling
- Network error handling
- User-friendly error messages
- Retry mechanisms
- Loading states

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

### Mobile Features
- Touch-friendly interface
- Swipe gestures
- Optimized layout for small screens
- Vertical split on mobile

## 🐛 Troubleshooting

### Common Issues

1. **App won't start**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Delete node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in backend
   - Verify API URL in `src/services/api.js`

3. **PDF upload fails**
   - Check file size (max 10MB)
   - Ensure file is a valid PDF
   - Check network connection

4. **Styling issues**
   - Clear browser cache
   - Check CSS file paths
   - Verify component imports

### Development Tips

1. **Use React Developer Tools** for debugging
2. **Check browser console** for errors
3. **Use Network tab** to monitor API calls
4. **Test on different screen sizes**

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

### Deploy Options

1. **Netlify**: Drag and drop the `build` folder
2. **Vercel**: Connect GitHub repository
3. **AWS S3**: Upload build files to S3 bucket
4. **GitHub Pages**: Use `gh-pages` package

### Environment Variables for Production

Set these in your hosting platform:
- `REACT_APP_API_URL` - Production backend URL
- `REACT_APP_TIMEOUT` - API timeout

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 