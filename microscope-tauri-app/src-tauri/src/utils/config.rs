use std::env;
use std::path::PathBuf;
use crate::models::DeviceConfig;

pub struct AppConfig {
    pub device: DeviceConfig,
    pub python_path: String,
    pub temp_dir: PathBuf,
    pub output_dir: PathBuf,
}

impl AppConfig {
    pub fn new() -> Self {
        let home_dir = env::var("HOME").unwrap_or_else(|_| ".".to_string());
        let current_dir = env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
        
        Self {
            device: DeviceConfig::default(),
            python_path: Self::get_python_path(&current_dir),
            temp_dir: PathBuf::from("/tmp"),
            output_dir: PathBuf::from(&home_dir),
        }
    }

    fn get_python_path(current_dir: &PathBuf) -> String {
        let venv_python = current_dir.join("../../venv/bin/python3");
        
        if venv_python.exists() {
            venv_python.to_string_lossy().to_string()
        } else {
            "python3".to_string()
        }
    }

    pub fn get_temp_file(&self, filename: &str) -> PathBuf {
        self.temp_dir.join(filename)
    }

    pub fn get_output_file(&self, filename: &str) -> PathBuf {
        self.output_dir.join(filename)
    }
}

impl Default for AppConfig {
    fn default() -> Self {
        Self::new()
    }
}