import React, { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import './PDFViewer.css';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const PDFViewer = ({ pdfFile, currentPage, onPageChange, onTotalPages }) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);

  useEffect(() => {
    setPageNumber(currentPage);
  }, [currentPage]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    onTotalPages(numPages);
  };

  const changePage = (offset) => {
    const newPageNumber = pageNumber + offset;
    if (newPageNumber >= 1 && newPageNumber <= numPages) {
      setPageNumber(newPageNumber);
      onPageChange(newPageNumber);
    }
  };

  const previousPage = () => {
    changePage(-1);
  };

  const nextPage = () => {
    changePage(1);
  };

  const zoomIn = () => {
    setScale(prevScale => Math.min(prevScale + 0.2, 3.0));
  };

  const zoomOut = () => {
    setScale(prevScale => Math.max(prevScale - 0.2, 0.5));
  };

  if (!pdfFile) {
    return (
      <div className="pdf-viewer">
        <div className="pdf-content">
          <div className="no-pdf">
            <p>No PDF file uploaded</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="pdf-viewer">
      <div className="pdf-toolbar">
        <div className="page-controls">
          <button 
            onClick={previousPage} 
            disabled={pageNumber <= 1}
            className="page-button"
          >
            ‹ Previous
          </button>
          <span className="page-info">
            Page {pageNumber} of {numPages || '...'}
          </span>
          <button 
            onClick={nextPage} 
            disabled={pageNumber >= (numPages || 1)}
            className="page-button"
          >
            Next ›
          </button>
        </div>
        <div className="zoom-controls">
          <button onClick={zoomOut} className="zoom-button">-</button>
          <span className="zoom-level">{Math.round(scale * 100)}%</span>
          <button onClick={zoomIn} className="zoom-button">+</button>
        </div>
      </div>
      
      <div className="pdf-content">
        <div className="pdf-document">
          <Document
            file={pdfFile}
            onLoadSuccess={onDocumentLoadSuccess}
            onLoadError={(error) => {
              console.error('Error loading PDF:', error);
            }}
            loading={<div className="loading">Loading PDF...</div>}
            error={<div className="error">Error loading PDF. Please try again.</div>}
          >
            <Page
              pageNumber={pageNumber}
              scale={scale}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="pdf-page"
            />
          </Document>
        </div>
      </div>
    </div>
  );
};

export default PDFViewer; 