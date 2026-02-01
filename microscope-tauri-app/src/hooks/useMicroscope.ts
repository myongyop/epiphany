import { useState, useCallback } from "react";
import { invoke } from "@tauri-apps/api/core";
import { MicroscopeStatus, CaptureResult } from "../types";

export const useMicroscope = () => {
  const [status, setStatus] = useState<MicroscopeStatus>({
    connected: false,
    device_id: undefined,
    resolution: "",
    fps: 0,
  });

  const checkMicroscope = useCallback(async (): Promise<MicroscopeStatus> => {
    try {
      const result = await invoke<MicroscopeStatus>("check_microscope");
      setStatus(result);
      return result;
    } catch (error) {
      console.error("Error checking microscope:", error);
      const disconnectedStatus: MicroscopeStatus = {
        connected: false,
        device_id: undefined,
        resolution: "",
        fps: 0,
      };
      setStatus(disconnectedStatus);
      return disconnectedStatus;
    }
  }, []);

  const captureImage = useCallback(async (): Promise<CaptureResult> => {
    try {
      return await invoke<CaptureResult>("capture_image");
    } catch (error) {
      console.error("Error capturing image:", error);
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }, []);

  const disconnect = useCallback(() => {
    setStatus({
      connected: false,
      device_id: undefined,
      resolution: "",
      fps: 0,
    });
  }, []);

  return {
    status,
    checkMicroscope,
    captureImage,
    disconnect,
  };
};