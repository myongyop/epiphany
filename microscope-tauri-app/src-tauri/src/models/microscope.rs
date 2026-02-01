use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MicroscopeStatus {
    pub connected: bool,
    pub device_id: Option<String>,
    pub resolution: String,
    pub fps: f32,
}

impl Default for MicroscopeStatus {
    fn default() -> Self {
        Self {
            connected: false,
            device_id: None,
            resolution: String::new(),
            fps: 0.0,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CaptureResult {
    pub success: bool,
    pub image_path: Option<String>,
    pub image_base64: Option<String>,
    pub error: Option<String>,
}

impl CaptureResult {
    pub fn success(image_path: Option<String>, image_base64: Option<String>) -> Self {
        Self {
            success: true,
            image_path,
            image_base64,
            error: None,
        }
    }

    pub fn error(error: String) -> Self {
        Self {
            success: false,
            image_path: None,
            image_base64: None,
            error: Some(error),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct StreamFrame {
    pub success: bool,
    pub image_base64: Option<String>,
    pub timestamp: u64,
    pub error: Option<String>,
}

impl StreamFrame {
    pub fn success(image_base64: String, timestamp: u64) -> Self {
        Self {
            success: true,
            image_base64: Some(image_base64),
            timestamp,
            error: None,
        }
    }

    pub fn error(error: String) -> Self {
        Self {
            success: false,
            image_base64: None,
            timestamp: 0,
            error: Some(error),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct DeviceConfig {
    pub vendor_id: u16,
    pub product_id: u16,
    pub video_device_index: u8,
    pub default_width: u32,
    pub default_height: u32,
    pub default_fps: u32,
}

impl Default for DeviceConfig {
    fn default() -> Self {
        Self {
            vendor_id: 0x05e3,  // Genesys Logic
            product_id: 0xf12a, // Digital Microscope
            video_device_index: 4,
            default_width: 640,
            default_height: 480,
            default_fps: 30,
        }
    }
}