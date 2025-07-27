import React, { useState, useEffect } from 'react';
import ChatPanel from './ChatPanel';
import PDFViewer from './PDFViewer';
import ResizableSplitPane from './ResizableSplitPane';
import apiService from '../services/api';
import './PDFChat.css';

const PDFChat = ({ pdfFile, onRemoveDocument }) => {
  const [messages, setMessages] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Add initial welcome message
  useEffect(() => {
    setMessages([
      {
        id: 1,
        type: 'system',
        content: 'Your document is ready!',
        suggestions: [
          'What is the main topic of this document?',
          'Can you summarize the key points?',
          'What are the conclusions or recommendations?'
        ]
      }
    ]);
  }, []);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get AI response from backend
      const response = await apiService.chatWithAI(message);
      
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.answer,
        citations: response.citations || [],
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      const errorResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: `I apologize, but I encountered an error while processing your question: ${error.message}. Please try again.`,
        citations: [],
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCitationClick = (page) => {
    setCurrentPage(page);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleTotalPages = (pages) => {
    // Total pages is now handled internally by PDFViewer
    console.log('Total pages:', pages);
  };

  return (
    <ResizableSplitPane
      left={
        <ChatPanel 
          messages={messages}
          onSendMessage={handleSendMessage}
          onCitationClick={handleCitationClick}
          onRemoveDocument={onRemoveDocument}
          isLoading={isLoading}
        />
      }
      right={
        <PDFViewer 
          pdfFile={pdfFile}
          currentPage={currentPage}
          onPageChange={handlePageChange}
          onTotalPages={handleTotalPages}
        />
      }
      defaultLeftWidth="40%"
      minLeftWidth="25%"
      maxLeftWidth="60%"
    />
  );
};

export default PDFChat; 