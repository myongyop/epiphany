use std::sync::Mutex;
use lazy_static::lazy_static;
use crate::models::{MicroscopeStatus, CaptureResult, StreamFrame};
use crate::utils::{AppConfig, PythonBridge};

// Global streaming state
lazy_static! {
    static ref STREAMING_STATE: Mutex<bool> = Mutex::new(false);
    static ref APP_CONFIG: AppConfig = AppConfig::new();
}

#[tauri::command]
pub async fn check_microscope() -> std::result::Result<MicroscopeStatus, String> {
    log::info!("Checking microscope connection");
    
    let bridge = PythonBridge::new(AppConfig::new());
    
    match bridge.check_device_connection() {
        Ok(connected) => {
            if connected {
                Ok(MicroscopeStatus {
                    connected: true,
                    device_id: Some(format!(
                        "{:04x}:{:04x}",
                        APP_CONFIG.device.vendor_id,
                        APP_CONFIG.device.product_id
                    )),
                    resolution: format!(
                        "{}x{}",
                        APP_CONFIG.device.default_width,
                        APP_CONFIG.device.default_height
                    ),
                    fps: APP_CONFIG.device.default_fps as f32,
                })
            } else {
                Ok(MicroscopeStatus::default())
            }
        }
        Err(e) => {
            log::error!("Failed to check microscope: {}", e);
            Err(e.to_string())
        }
    }
}

#[tauri::command]
pub async fn get_live_frame() -> std::result::Result<StreamFrame, String> {
    log::debug!("Capturing live frame");
    
    let bridge = PythonBridge::new(AppConfig::new());
    let temp_file = APP_CONFIG.get_temp_file("microscope_live_frame.jpg");
    let temp_file_str = temp_file.to_string_lossy();
    
    match bridge.capture_frame(&temp_file_str) {
        Ok(output) => {
            let lines: Vec<&str> = output.lines().collect();
            
            if lines.len() >= 3 && lines[0] == "SUCCESS" {
                let base64_data = lines[1];
                if let Ok(timestamp) = lines[2].parse::<u64>() {
                    return Ok(StreamFrame::success(base64_data.to_string(), timestamp));
                }
            }
            
            let error_msg = if output.starts_with("ERROR:") {
                output[6..].to_string()
            } else {
                "Camera busy or unavailable".to_string()
            };
            
            Ok(StreamFrame::error(error_msg))
        }
        Err(e) => {
            log::error!("Failed to capture live frame: {}", e);
            Ok(StreamFrame::error(e.to_string()))
        }
    }
}

#[tauri::command]
pub async fn capture_image() -> std::result::Result<CaptureResult, String> {
    log::info!("Capturing high-quality image");
    
    let bridge = PythonBridge::new(AppConfig::new());
    let temp_file = APP_CONFIG.get_temp_file("microscope_capture.jpg");
    let temp_file_str = temp_file.to_string_lossy();
    
    match bridge.capture_high_quality_image(&temp_file_str) {
        Ok(output) => {
            if output.starts_with("SUCCESS:") {
                let json_part = &output[8..]; // Remove "SUCCESS:" prefix
                if let Ok(data) = serde_json::from_str::<serde_json::Value>(json_part) {
                    if let Some(base64_data) = data["base64"].as_str() {
                        return Ok(CaptureResult::success(
                            Some(temp_file_str.to_string()),
                            Some(base64_data.to_string()),
                        ));
                    }
                }
            }
            
            let error_msg = if output.starts_with("ERROR:") {
                output[6..].to_string()
            } else {
                "Unknown error occurred".to_string()
            };
            
            Ok(CaptureResult::error(error_msg))
        }
        Err(e) => {
            log::error!("Failed to capture image: {}", e);
            Ok(CaptureResult::error(e.to_string()))
        }
    }
}

#[tauri::command]
pub async fn start_streaming() -> std::result::Result<bool, String> {
    log::info!("Starting video stream");
    
    let mut streaming = STREAMING_STATE
        .lock()
        .map_err(|e| format!("Failed to acquire streaming lock: {}", e))?;
    *streaming = true;
    Ok(true)
}

#[tauri::command]
pub async fn stop_streaming() -> std::result::Result<bool, String> {
    log::info!("Stopping video stream");
    
    let mut streaming = STREAMING_STATE
        .lock()
        .map_err(|e| format!("Failed to acquire streaming lock: {}", e))?;
    *streaming = false;
    Ok(true)
}

#[tauri::command]
pub async fn is_streaming() -> std::result::Result<bool, String> {
    let streaming = STREAMING_STATE
        .lock()
        .map_err(|e| format!("Failed to acquire streaming lock: {}", e))?;
    Ok(*streaming)
}

#[tauri::command]
pub async fn test_camera() -> std::result::Result<String, String> {
    log::info!("Testing camera connection");
    
    let bridge = PythonBridge::new(AppConfig::new());
    
    match bridge.execute_script("print('Hello from Python!')") {
        Ok(result) => Ok(format!("Test successful: {}", result.trim())),
        Err(e) => {
            log::error!("Camera test failed: {}", e);
            Err(e.to_string())
        }
    }
}