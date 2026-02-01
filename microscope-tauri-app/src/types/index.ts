export interface MicroscopeStatus {
  connected: boolean;
  device_id?: string;
  resolution: string;
  fps: number;
}

export interface CaptureResult {
  success: boolean;
  image_path?: string;
  image_base64?: string;
  error?: string;
}

export interface StreamFrame {
  success: boolean;
  image_base64?: string;
  timestamp: number;
  error?: string;
}

export interface SessionStats {
  sessionStartTime: number;
  maxFps: number;
  captureCount: number;
  recordingSessionCount: number;
}

export interface AppState {
  status: MicroscopeStatus;
  currentImage: string;
  isCapturing: boolean;
  isLiveStreaming: boolean;
  logs: string[];
  fps: number;
  stats: SessionStats;
}