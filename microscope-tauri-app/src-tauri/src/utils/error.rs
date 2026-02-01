use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Serialize, Deserialize)]
pub enum EpiphanyError {
    PythonExecutionError(String),
    DeviceNotFound,
    CameraAccessError(String),
    FileOperationError(String),
    ConfigurationError(String),
    StreamingError(String),
}

impl fmt::Display for EpiphanyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            EpiphanyError::PythonExecutionError(msg) => {
                write!(f, "Python execution failed: {}", msg)
            }
            EpiphanyError::DeviceNotFound => {
                write!(f, "Microscope device not found")
            }
            EpiphanyError::CameraAccessError(msg) => {
                write!(f, "Camera access error: {}", msg)
            }
            EpiphanyError::FileOperationError(msg) => {
                write!(f, "File operation failed: {}", msg)
            }
            EpiphanyError::ConfigurationError(msg) => {
                write!(f, "Configuration error: {}", msg)
            }
            EpiphanyError::StreamingError(msg) => {
                write!(f, "Streaming error: {}", msg)
            }
        }
    }
}

impl std::error::Error for EpiphanyError {}

pub type Result<T> = std::result::Result<T, EpiphanyError>;

impl From<std::io::Error> for EpiphanyError {
    fn from(error: std::io::Error) -> Self {
        EpiphanyError::FileOperationError(error.to_string())
    }
}

impl From<base64::DecodeError> for EpiphanyError {
    fn from(error: base64::DecodeError) -> Self {
        EpiphanyError::FileOperationError(format!("Base64 decode error: {}", error))
    }
}