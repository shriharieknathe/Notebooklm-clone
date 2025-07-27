import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUpload } from 'react-icons/fi';
import './PDFUpload.css';

const PDFUpload = ({ onFileUpload, isUploading, uploadProgress }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (file.type === 'application/pdf') {
        onFileUpload(file);
      } else {
        alert('Please upload a PDF file');
      }
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  if (isUploading) {
    return (
      <div className="upload-container">
        <div className="upload-card">
          <div className="upload-progress">
            <div className="progress-spinner"></div>
            <div className="progress-text">Uploading PDF</div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <div className="progress-percentage">{uploadProgress}%</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="upload-container">
      <div className="upload-card" {...getRootProps()}>
        <input {...getInputProps()} />
        <div className="upload-icon">
          <FiUpload size={48} />
        </div>
        <h2 className="upload-title">Upload PDF to start chatting</h2>
        <p className="upload-subtitle">Click or drag and drop your file here</p>
      </div>
    </div>
  );
};

export default PDFUpload; 