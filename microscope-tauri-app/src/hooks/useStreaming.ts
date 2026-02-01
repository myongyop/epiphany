import { useState, useCallback, useRef, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { StreamFrame } from "../types";

interface UseStreamingProps {
  onLog: (message: string) => void;
  onFpsUpdate: (fps: number) => void;
  onMaxFpsUpdate: (maxFps: number) => void;
  onImageUpdate: (imageData: string) => void;
  isConnected: boolean;
}

export const useStreaming = ({
  onLog,
  onFpsUpdate,
  onMaxFpsUpdate,
  onImageUpdate,
  isConnected,
}: UseStreamingProps) => {
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [recordingSessionCount, setRecordingSessionCount] = useState(0);

  // Refs for performance tracking
  const frameCountRef = useRef(0);
  const lastFpsUpdateRef = useRef(Date.now());
  const streamIntervalRef = useRef<number | null>(null);
  const isRequestingFrameRef = useRef(false);

  const getLiveFrame = useCallback(async () => {
    if (!isConnected || isRequestingFrameRef.current) return;

    isRequestingFrameRef.current = true;

    try {
      const frame = await invoke<StreamFrame>("get_live_frame");

      if (frame.success && frame.image_base64) {
        onImageUpdate(`data:image/jpeg;base64,${frame.image_base64}`);

        // FPS calculation
        frameCountRef.current++;
        const now = Date.now();
        if (now - lastFpsUpdateRef.current >= 1000) {
          const currentFps = frameCountRef.current;
          onFpsUpdate(currentFps);
          onMaxFpsUpdate(currentFps);
          frameCountRef.current = 0;
          lastFpsUpdateRef.current = now;
        }
      } else if (frame.error) {
        console.warn("Frame error (ignoring):", frame.error);
      }
    } catch (error) {
      console.error("getLiveFrame error:", error);
      onLog(`Live frame error: ${error}`);
    } finally {
      isRequestingFrameRef.current = false;
    }
  }, [isConnected, onLog, onFpsUpdate, onMaxFpsUpdate, onImageUpdate]);

  const startLiveStream = useCallback(async () => {
    if (!isConnected || isLiveStreaming) return;

    try {
      await invoke("start_streaming");
      setIsLiveStreaming(true);
      setRecordingSessionCount(prev => prev + 1);
      onLog("Live recording started");

      // Update frames at 10fps (100ms interval)
      streamIntervalRef.current = setInterval(getLiveFrame, 100);
    } catch (error) {
      onLog(`Failed to start streaming: ${error}`);
    }
  }, [isConnected, isLiveStreaming, getLiveFrame, onLog]);

  const stopLiveStream = useCallback(async () => {
    if (!isLiveStreaming) return;

    // Clear interval immediately
    if (streamIntervalRef.current) {
      clearInterval(streamIntervalRef.current);
      streamIntervalRef.current = null;
    }

    // Update state immediately
    setIsLiveStreaming(false);
    onFpsUpdate(0);
    frameCountRef.current = 0;
    isRequestingFrameRef.current = false;

    try {
      await invoke("stop_streaming");
      onLog("Live recording stopped");
    } catch (error) {
      onLog(`Failed to stop streaming: ${error}`);
    }
  }, [isLiveStreaming, onLog, onFpsUpdate]);

  const toggleStreaming = useCallback(async () => {
    if (isLiveStreaming) {
      await stopLiveStream();
    } else {
      await startLiveStream();
    }
  }, [isLiveStreaming, startLiveStream, stopLiveStream]);

  // Clean up streaming on component unmount
  useEffect(() => {
    return () => {
      if (streamIntervalRef.current) {
        clearInterval(streamIntervalRef.current);
      }
    };
  }, []);

  return {
    isLiveStreaming,
    recordingSessionCount,
    startLiveStream,
    stopLiveStream,
    toggleStreaming,
  };
};