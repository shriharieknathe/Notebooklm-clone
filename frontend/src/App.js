import React, { useState, useEffect } from 'react';
import './App.css';
import PDFUpload from './components/PDFUpload';
import PDFChat from './components/PDFChat';
import apiService from './services/api';

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend health on component mount
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.healthCheck();
      setBackendStatus('connected');
    } catch (error) {
      console.error('Backend connection failed:', error);
      setBackendStatus('disconnected');
    }
  };

  const handleFileUpload = async (file) => {
    if (backendStatus !== 'connected') {
      alert('Backend is not connected. Please ensure the backend server is running.');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    
    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Upload to backend
      const uploadResult = await apiService.uploadPDF(file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Wait a moment to show completion
      setTimeout(() => {
        setPdfFile(file);
        setIsUploading(false);
        setUploadProgress(0);
      }, 500);

    } catch (error) {
      console.error('Upload failed:', error);
      alert(`Upload failed: ${error.message}`);
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleRemoveDocument = () => {
    setPdfFile(null);
  };

  if (backendStatus === 'checking') {
    return (
      <div className="App">
        <div className="loading-screen">
          <div className="loading-spinner"></div>
          <p>Checking backend connection...</p>
        </div>
      </div>
    );
  }

  if (backendStatus === 'disconnected') {
    return (
      <div className="App">
        <div className="error-screen">
          <h2>Backend Connection Error</h2>
          <p>The backend server is not running or not accessible.</p>
          <p>Please ensure the backend server is running on http://localhost:8000</p>
          <button onClick={checkBackendHealth} className="retry-button">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      {!pdfFile ? (
        <PDFUpload 
          onFileUpload={handleFileUpload}
          isUploading={isUploading}
          uploadProgress={uploadProgress}
        />
      ) : (
        <PDFChat 
          pdfFile={pdfFile}
          onRemoveDocument={handleRemoveDocument}
        />
      )}
    </div>
  );
}

export default App; 