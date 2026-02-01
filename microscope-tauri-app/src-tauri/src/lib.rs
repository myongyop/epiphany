mod models;
mod utils;
mod commands;

use commands::*;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Initialize logging
    env_logger::init();
    
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            check_microscope,
            get_live_frame,
            capture_image,
            start_streaming,
            stop_streaming,
            is_streaming,
            save_image,
            save_log,
            test_camera
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
