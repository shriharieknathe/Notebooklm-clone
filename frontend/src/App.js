import React, { useState } from 'react';
import './App.css';
import PDFUpload from './components/PDFUpload';
import PDFChat from './components/PDFChat';
import apiService from './services/api';

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileUpload = async (file) => {
    setIsUploading(true);
    setUploadProgress(0);
    
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

    try {
      // Try to upload to backend (but don't block if it fails)
      await apiService.uploadPDF(file);
    } catch (error) {
      console.error('Backend upload failed:', error);
      // Continue anyway - we'll still show the PDF
    }
    
    clearInterval(progressInterval);
    setUploadProgress(100);
    
    // Wait a moment to show completion
    setTimeout(() => {
      setPdfFile(file);
      setIsUploading(false);
      setUploadProgress(0);
    }, 500);
  };

  const handleRemoveDocument = () => {
    setPdfFile(null);
  };

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