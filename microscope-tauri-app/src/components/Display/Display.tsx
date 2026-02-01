import React from "react";
import "./Display.css";

interface DisplayProps {
  currentImage: string;
  isLiveStreaming: boolean;
}

export const Display: React.FC<DisplayProps> = ({
  currentImage,
  isLiveStreaming,
}) => {
  return (
    <div className="image-display">
      {currentImage ? (
        <div className="video-container">
          <img 
            src={currentImage} 
            alt="Microscope view" 
            className="microscope-image"
          />
          {isLiveStreaming && (
            <div className="live-indicator">
              <span className="live-dot"></span>
              LIVE
            </div>
          )}
        </div>
      ) : (
        <div className="no-image">
          <div className="placeholder">
            📹 No Image
            <p>Loading sample image...</p>
          </div>
        </div>
      )}
    </div>
  );
};