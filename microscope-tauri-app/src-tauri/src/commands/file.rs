use base64::Engine;
use crate::utils::{AppConfig, EpiphanyError, Result};

#[tauri::command]
pub async fn save_image(image_base64: String, filename: String) -> std::result::Result<String, String> {
    log::info!("Saving image: {}", filename);
    
    let config = AppConfig::new();
    
    match save_base64_file(&image_base64, &filename, &config) {
        Ok(path) => {
            log::info!("Image saved successfully: {}", path);
            Ok(path)
        }
        Err(e) => {
            log::error!("Failed to save image: {}", e);
            Err(e.to_string())
        }
    }
}

#[tauri::command]
pub async fn save_log(log_content: String, filename: String) -> std::result::Result<String, String> {
    log::info!("Saving log: {}", filename);
    
    let config = AppConfig::new();
    
    match save_base64_file(&log_content, &filename, &config) {
        Ok(path) => {
            log::info!("Log saved successfully: {}", path);
            Ok(path)
        }
        Err(e) => {
            log::error!("Failed to save log: {}", e);
            Err(e.to_string())
        }
    }
}

fn save_base64_file(base64_content: &str, filename: &str, config: &AppConfig) -> Result<String> {
    let file_data = base64::engine::general_purpose::STANDARD
        .decode(base64_content)
        .map_err(EpiphanyError::from)?;
    
    let file_path = config.get_output_file(filename);
    
    std::fs::write(&file_path, file_data)
        .map_err(EpiphanyError::from)?;
    
    Ok(file_path.to_string_lossy().to_string())
}