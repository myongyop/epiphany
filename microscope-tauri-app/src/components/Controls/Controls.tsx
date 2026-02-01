import React from "react";
import "./Controls.css";

interface ControlsProps {
  isConnected: boolean;
  isCapturing: boolean;
  isLiveStreaming: boolean;
  currentImage: string;
  onCaptureImage: () => void;
  onToggleStreaming: () => void;
  onSaveImage: () => void;
}

export const Controls: React.FC<ControlsProps> = ({
  isConnected,
  isCapturing,
  isLiveStreaming,
  currentImage,
  onCaptureImage,
  onToggleStreaming,
  onSaveImage,
}) => {
  return (
    <div className="control-panel">
      <div className="button-group">
        <button 
          onClick={onCaptureImage}
          disabled={!isConnected || isCapturing}
          className="btn btn-success"
        >
          {isCapturing ? '📸 Capturing...' : '📸 Capture HQ'}
        </button>
        
        <button 
          onClick={onToggleStreaming}
          disabled={!isConnected}
          className={`btn ${isLiveStreaming ? 'btn-danger' : 'btn-info'}`}
        >
          {isLiveStreaming ? '⏹ Stop Recording' : '🔴 Recording Live'}
        </button>
        
        <button 
          onClick={onSaveImage}
          disabled={!currentImage}
          className="btn btn-secondary"
        >
          💾 Save Image
        </button>
      </div>
    </div>
  );
};