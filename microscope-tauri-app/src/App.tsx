import { useState, useEffect, useCallback } from "react";
import { invoke } from "@tauri-apps/api/core";
import { Header, Controls, Display, Logs } from "./components";
import { useMicroscope, useStreaming } from "./hooks";
import { CaptureResult, SessionStats } from "./types";
import "./App.css";

function App() {
  const [currentImage, setCurrentImage] = useState<string>("/sample-microscope.jpg");
  const [isCapturing, setIsCapturing] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [fps, setFps] = useState<number>(0);
  
  // Statistics and session information
  const [stats, setStats] = useState<SessionStats>({
    sessionStartTime: Date.now(),
    maxFps: 0,
    captureCount: 0,
    recordingSessionCount: 0,
  });

  const { status, checkMicroscope, captureImage, disconnect } = useMicroscope();

  const addLog = useCallback((message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev.slice(-9), `[${timestamp}] ${message}`]);
  }, []);

  const handleFpsUpdate = useCallback((newFps: number) => {
    setFps(newFps);
  }, []);

  const handleMaxFpsUpdate = useCallback((newMaxFps: number) => {
    setStats(prev => ({
      ...prev,
      maxFps: Math.max(prev.maxFps, newMaxFps),
    }));
  }, []);

  const handleImageUpdate = useCallback((imageData: string) => {
    setCurrentImage(imageData);
  }, []);

  const { isLiveStreaming, recordingSessionCount, startLiveStream, stopLiveStream, toggleStreaming } = useStreaming({
    onLog: addLog,
    onFpsUpdate: handleFpsUpdate,
    onMaxFpsUpdate: handleMaxFpsUpdate,
    onImageUpdate: handleImageUpdate,
    isConnected: status.connected,
  });

  // Update recording session count in stats
  useEffect(() => {
    setStats(prev => ({
      ...prev,
      recordingSessionCount,
    }));
  }, [recordingSessionCount]);

  const toggleConnection = async () => {
    if (status.connected) {
      // Disconnect
      disconnect();
      stopLiveStream();
      setCurrentImage("/sample-microscope.jpg");
      addLog("Microscope disconnected");
    } else {
      // Attempt connection
      const result = await checkMicroscope();
      if (result.connected) {
        addLog(`Microscope connected: ${result.device_id}`);
        // Auto-start streaming when connected
        startLiveStream();
      } else {
        addLog("Microscope connection failed");
      }
    }
  };

  const captureHighQualityImage = async () => {
    if (!status.connected) {
      addLog("Please connect microscope first");
      return;
    }

    setIsCapturing(true);
    try {
      const result: CaptureResult = await captureImage();
      if (result.success && result.image_base64) {
        // Temporarily replace with high-quality image
        const highQualityImage = `data:image/jpeg;base64,${result.image_base64}`;
        setCurrentImage(highQualityImage);
        addLog("High-quality image captured");
        
        // Return to live stream after 3 seconds
        setTimeout(() => {
          if (isLiveStreaming) {
            addLog("Resumed live streaming");
          }
        }, 3000);
      } else {
        addLog(`Capture failed: ${result.error || "Unknown error"}`);
      }
    } catch (error) {
      addLog(`Capture error: ${error}`);
    } finally {
      setIsCapturing(false);
    }
  };

  const saveImage = async () => {
    if (!currentImage) {
      addLog("No image to save");
      return;
    }

    try {
      const base64Data = currentImage.split(',')[1]; // Remove data:image/jpeg;base64, prefix
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `microscope_${timestamp}.jpg`;
      
      const savedPath = await invoke<string>("save_image", {
        imageBase64: base64Data,
        filename: filename
      });
      
      setStats(prev => ({
        ...prev,
        captureCount: prev.captureCount + 1,
      }));
      addLog(`Image saved: ${savedPath}`);
    } catch (error) {
      addLog(`Save error: ${error}`);
    }
  };

  const saveLog = async () => {
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `epiphany_log_${timestamp}.txt`;
      
      // Add session information
      const sessionInfo = [
        `=== Epiphany Session Log ===`,
        `Generated: ${new Date().toLocaleString()}`,
        `Session Duration: ${Math.floor((Date.now() - stats.sessionStartTime) / 1000)}s`,
        `Total Log Entries: ${logs.length}`,
        `Device: ${status.device_id || 'Not connected'}`,
        `Resolution: ${status.resolution || 'N/A'}`,
        `Max FPS: ${stats.maxFps}`,
        `Images Captured: ${stats.captureCount}`,
        `Recording Sessions: ${stats.recordingSessionCount}`,
        ``,
        `=== Activity Log ===`,
        ...logs,
        ``,
        `=== End of Log ===`
      ].join('\n');
      
      // Encode to Base64
      const logBase64 = btoa(unescape(encodeURIComponent(sessionInfo)));
      
      const savedPath = await invoke<string>("save_log", {
        logContent: logBase64,
        filename: filename
      });
      
      addLog(`Session log saved: ${savedPath}`);
    } catch (error) {
      addLog(`Failed to save log: ${error}`);
    }
  };

  // Add initial log messages
  useEffect(() => {
    addLog("Epiphany started - ready to connect");
    addLog("Click 'Connect' to connect to microscope");
  }, [addLog]);

  return (
    <div className="microscope-app">
      <Header
        status={status}
        isLiveStreaming={isLiveStreaming}
        fps={fps}
        onToggleConnection={toggleConnection}
      />

      <main className="app-main">
        <Controls
          isConnected={status.connected}
          isCapturing={isCapturing}
          isLiveStreaming={isLiveStreaming}
          currentImage={currentImage}
          onCaptureImage={captureHighQualityImage}
          onToggleStreaming={toggleStreaming}
          onSaveImage={saveImage}
        />

        <div className="content-area">
          <Display
            currentImage={currentImage}
            isLiveStreaming={isLiveStreaming}
          />

          <Logs
            logs={logs}
            stats={stats}
            onSaveLog={saveLog}
          />
        </div>
      </main>
    </div>
  );
}

export default App;
