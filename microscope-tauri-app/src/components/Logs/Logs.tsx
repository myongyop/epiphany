import React from "react";
import { SessionStats } from "../../types";
import "./Logs.css";

interface LogsProps {
  logs: string[];
  stats: SessionStats;
  onSaveLog: () => void;
}

export const Logs: React.FC<LogsProps> = ({
  logs,
  stats,
  onSaveLog,
}) => {
  const sessionDuration = Math.floor((Date.now() - stats.sessionStartTime) / 1000);

  return (
    <div className="log-panel">
      <div className="log-header">
        <h3>📋 Activity Log</h3>
      </div>
      <div className="log-content">
        {logs.map((log, index) => (
          <div key={index} className="log-entry">
            {log}
          </div>
        ))}
      </div>
      <div className="log-footer">
        <div className="log-stats">
          <span>Session: {sessionDuration}s</span>
          <span>Captures: {stats.captureCount}</span>
          <span>Max FPS: {stats.maxFps}</span>
        </div>
        <button 
          onClick={onSaveLog}
          className="btn-log-save"
          title="Save session log for analysis"
        >
          💾 Save Log
        </button>
      </div>
    </div>
  );
};