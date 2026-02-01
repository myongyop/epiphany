import React from "react";
import { MicroscopeStatus } from "../../types";
import "./Header.css";

interface HeaderProps {
  status: MicroscopeStatus;
  isLiveStreaming: boolean;
  fps: number;
  onToggleConnection: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  status,
  isLiveStreaming,
  fps,
  onToggleConnection,
}) => {
  return (
    <header className="app-header">
      <div className="header-left">
        <h1>🔬 Epiphany</h1>
        <span className="app-subtitle">USB Microscope</span>
      </div>
      <div className="header-right">
        <div className={`connection-status ${status.connected ? 'connected' : 'disconnected'}`}>
          <div className="status-indicator"></div>
          <span className="status-text">
            {status.connected ? 'Connected' : 'Disconnected'}
          </span>
          {status.connected && (
            <span className="device-info">
              {status.device_id} | {status.resolution} | {status.fps}fps
              {isLiveStreaming && fps > 0 && ` | Live: ${fps}fps`}
            </span>
          )}
        </div>
        <div className="toggle-container">
          <span className="toggle-label">Connect</span>
          <button 
            onClick={onToggleConnection}
            className={`toggle-switch ${status.connected ? 'on' : 'off'}`}
          >
            <div className="toggle-slider"></div>
          </button>
        </div>
      </div>
    </header>
  );
};