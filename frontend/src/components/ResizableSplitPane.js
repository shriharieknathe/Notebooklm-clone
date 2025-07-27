import React, { useState, useRef, useEffect } from 'react';
import './ResizableSplitPane.css';

const ResizableSplitPane = ({ 
  left, 
  right, 
  defaultLeftWidth = "40%", 
  minLeftWidth = "25%", 
  maxLeftWidth = "60%" 
}) => {
  const [leftWidth, setLeftWidth] = useState(defaultLeftWidth);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef(null);

  // Convert percentage to pixels for calculations
  const getPixelValue = (value) => {
    if (typeof value === 'string' && value.includes('%')) {
      const percentage = parseFloat(value);
      return (percentage / 100) * window.innerWidth;
    }
    return parseFloat(value);
  };

  // Convert pixels to percentage for state
  const getPercentageValue = (pixels) => {
    const percentage = (pixels / window.innerWidth) * 100;
    return `${Math.round(percentage)}%`;
  };

  const handleMouseDown = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    
    const containerRect = containerRef.current.getBoundingClientRect();
    const newLeftWidthPixels = e.clientX - containerRect.left;
    
    const minPixels = getPixelValue(minLeftWidth);
    const maxPixels = getPixelValue(maxLeftWidth);
    
    // Ensure the width stays within bounds
    if (newLeftWidthPixels >= minPixels && newLeftWidthPixels <= maxPixels) {
      setLeftWidth(getPercentageValue(newLeftWidthPixels));
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  return (
    <div 
      ref={containerRef}
      className="resizable-split-pane"
      style={{ cursor: isDragging ? 'col-resize' : 'default' }}
    >
      <div 
        className="left-pane"
        style={{ width: leftWidth }}
      >
        {left}
      </div>
      
      <div 
        className="resizer"
        onMouseDown={handleMouseDown}
        style={{ cursor: 'col-resize' }}
      />
      
      <div className="right-pane">
        {right}
      </div>
    </div>
  );
};

export default ResizableSplitPane; 