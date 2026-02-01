use std::process::Command;
use crate::utils::{AppConfig, EpiphanyError, Result};

pub struct PythonBridge {
    config: AppConfig,
}

impl PythonBridge {
    pub fn new(config: AppConfig) -> Self {
        Self { config }
    }

    pub fn execute_script(&self, script: &str) -> Result<String> {
        let output = Command::new(&self.config.python_path)
            .arg("-c")
            .arg(script)
            .output()
            .map_err(|e| EpiphanyError::PythonExecutionError(format!("Failed to execute: {}", e)))?;

        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);

        if !stderr.is_empty() {
            log::debug!("Python stderr: {}", stderr);
        }

        if !output.status.success() {
            return Err(EpiphanyError::PythonExecutionError(format!(
                "Python script failed with exit code: {}. Stderr: {}",
                output.status.code().unwrap_or(-1),
                stderr
            )));
        }

        Ok(stdout.to_string())
    }

    pub fn check_device_connection(&self) -> Result<bool> {
        let script = format!(
            r#"
import subprocess
import sys
try:
    result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and '{:04x}:{:04x}' in result.stdout:
        print('CONNECTED:{:04x}:{:04x}')
    else:
        print('DISCONNECTED')
except subprocess.TimeoutExpired:
    print('ERROR:lsusb timeout')
except Exception as e:
    print(f'ERROR:{{e}}')
"#,
            self.config.device.vendor_id,
            self.config.device.product_id,
            self.config.device.vendor_id,
            self.config.device.product_id
        );

        let output = self.execute_script(&script)?;
        Ok(output.contains("CONNECTED"))
    }

    pub fn capture_frame(&self, temp_file: &str) -> Result<String> {
        let script = format!(
            r#"
import cv2
import base64
import sys
import time
import os

try:
    cap = cv2.VideoCapture({})
    
    if not cap.isOpened():
        print('ERROR:Cannot open camera')
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, {})
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, {})
    cap.set(cv2.CAP_PROP_FPS, {})
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    for _ in range(1):
        cap.read()
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print('ERROR:Cannot capture frame')
        sys.exit(1)
    
    cv2.imwrite('{}', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    
    with open('{}', 'rb') as f:
        img_data = f.read()
    
    img_base64 = base64.b64encode(img_data).decode('utf-8')
    timestamp = int(time.time() * 1000)
    
    os.remove('{}')
    
    print('SUCCESS')
    print(img_base64)
    print(timestamp)
    
except Exception as e:
    print('ERROR:' + str(e))
"#,
            self.config.device.video_device_index,
            self.config.device.default_width,
            self.config.device.default_height,
            self.config.device.default_fps,
            temp_file,
            temp_file,
            temp_file
        );

        self.execute_script(&script)
    }

    pub fn capture_high_quality_image(&self, temp_file: &str) -> Result<String> {
        let script = format!(
            r#"
import cv2
import base64
import sys

try:
    cap = cv2.VideoCapture({})
    
    if not cap.isOpened():
        print('ERROR:Cannot open camera')
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, {})
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, {})
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print('ERROR:Cannot capture frame')
        sys.exit(1)
    
    cv2.imwrite('{}', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    print('SUCCESS:' + '{{"base64":"' + img_base64 + '"}}')
    
except Exception as e:
    print('ERROR:' + str(e))
"#,
            self.config.device.video_device_index,
            self.config.device.default_width,
            self.config.device.default_height,
            temp_file
        );

        self.execute_script(&script)
    }
}