use anyhow::Result;
use chrono::Local;
use eframe::egui;
use log::{error, info};
use opencv::{
    core::Mat,
    imgcodecs,
    imgproc,
    prelude::*,
    videoio::{VideoCapture, CAP_V4L2},
};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

fn main() -> Result<(), eframe::Error> {
    env_logger::init();
    
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1024.0, 768.0])
            .with_min_inner_size([800.0, 600.0])
            .with_icon(eframe::icon_data::from_png_bytes(&[]).unwrap_or_default()),
        ..Default::default()
    };

    eframe::run_native(
        "USB Microscope Control - Rust Edition",
        options,
        Box::new(|cc| {
            // Set dark mode
            cc.egui_ctx.set_visuals(egui::Visuals::dark());
            Ok(Box::new(MicroscopeApp::new(cc)))
        }),
    )
}

#[derive(Debug)]
pub enum MicroscopeError {
    OpenCvError(opencv::Error),
    ConnectionError(String),
    CaptureError(String),
}

impl std::fmt::Display for MicroscopeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MicroscopeError::OpenCvError(e) => write!(f, "OpenCV Error: {}", e),
            MicroscopeError::ConnectionError(msg) => write!(f, "Connection Error: {}", msg),
            MicroscopeError::CaptureError(msg) => write!(f, "Capture Error: {}", msg),
        }
    }
}

impl std::error::Error for MicroscopeError {}

impl From<opencv::Error> for MicroscopeError {
    fn from(error: opencv::Error) -> Self {
        MicroscopeError::OpenCvError(error)
    }
}

struct MicroscopeApp {
    // Microscope status
    is_connected: bool,
    is_streaming: bool,
    
    // Video capture
    capture: Option<VideoCapture>,
    current_frame: Arc<Mutex<Option<Mat>>>,
    frame_texture: Option<egui::TextureHandle>,
    
    // UI state
    brightness: f32,
    contrast: f32,
    resolution_index: usize,
    auto_save: bool,
    save_directory: String,
    
    // Statistics
    fps: f32,
    frame_count: u64,
    last_fps_update: Instant,
    
    // Logs
    log_messages: Vec<String>,
    
    // Settings
    resolutions: Vec<(i32, i32, &'static str)>,
}

impl MicroscopeApp {
    fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        Self {
            is_connected: false,
            is_streaming: false,
            capture: None,
            current_frame: Arc::new(Mutex::new(None)),
            frame_texture: None,
            brightness: 0.5,
            contrast: 0.5,
            resolution_index: 0,
            auto_save: false,
            save_directory: std::env::var("HOME").unwrap_or_else(|_| ".".to_string()),
            fps: 0.0,
            frame_count: 0,
            last_fps_update: Instant::now(),
            log_messages: Vec::new(),
            resolutions: vec![
                (640, 480, "640×480 (Default)"),
                (320, 240, "320×240 (Low Res)"),
                (1280, 720, "1280×720 (HD)"),
            ],
        }
    }
    
    fn add_log(&mut self, message: String) {
        let timestamp = Local::now().format("%H:%M:%S");
        self.log_messages.push(format!("[{}] {}", timestamp, message));
        
        // Log message count limit
        if self.log_messages.len() > 100 {
            self.log_messages.remove(0);
        }
        
        info!("{}", message);
    }
    
    fn connect_microscope(&mut self) -> Result<(), MicroscopeError> {
        if self.is_connected {
            return Ok(());
        }
        
        self.add_log("Attempting to connect microscope...".to_string());
        
        // Try connecting with OpenCV VideoCapture
        let mut cap = VideoCapture::new(4, CAP_V4L2)?; // /dev/video4
        
        if !cap.is_opened()? {
            return Err(MicroscopeError::ConnectionError(
                "Cannot open video device".to_string(),
            ));
        }
        
        // Set resolution
        let (width, height, _) = self.resolutions[self.resolution_index];
        cap.set(opencv::videoio::CAP_PROP_FRAME_WIDTH, width as f64)?;
        cap.set(opencv::videoio::CAP_PROP_FRAME_HEIGHT, height as f64)?;
        cap.set(opencv::videoio::CAP_PROP_FPS, 30.0)?;
        
        self.capture = Some(cap);
        self.is_connected = true;
        
        self.add_log("Microscope connected successfully!".to_string());
        Ok(())
    }
    
    fn disconnect_microscope(&mut self) {
        if !self.is_connected {
            return;
        }
        
        self.stop_streaming();
        self.capture = None;
        self.is_connected = false;
        
        self.add_log("Microscope disconnected".to_string());
    }
    
    fn start_streaming(&mut self) {
        if !self.is_connected || self.is_streaming {
            return;
        }
        
        self.is_streaming = true;
        self.frame_count = 0;
        self.last_fps_update = Instant::now();
        
        self.add_log("Video streaming started".to_string());
    }
    
    fn stop_streaming(&mut self) {
        if !self.is_streaming {
            return;
        }
        
        self.is_streaming = false;
        self.add_log("Video streaming stopped".to_string());
    }
    
    fn capture_frame(&mut self) -> Result<(), MicroscopeError> {
        if let Some(ref mut cap) = self.capture {
            let mut frame = Mat::default();
            cap.read(&mut frame)?;
            
use std::env;

fn main() {
    // Store frame in shared memory
    if let Ok(mut current_frame) = self.current_frame.lock() {
        *current_frame = Some(frame);
    }
                
                self.frame_count += 1;
                
                // FPS calculation
                let now = Instant::now();
                if now.duration_since(self.last_fps_update) >= Duration::from_secs(1) {
                    self.fps = self.frame_count as f32;
                    self.frame_count = 0;
                    self.last_fps_update = now;
                }
                
                return Ok(());
            }
        }
        
        Err(MicroscopeError::CaptureError("Frame capture failed".to_string()))
    }
    
    fn save_image(&mut self) -> Result<(), MicroscopeError> {
        let frame_to_save = {
            if let Ok(current_frame) = self.current_frame.lock() {
                if let Some(ref frame) = *current_frame {
                    Some(frame.clone())
                } else {
                    None
                }
            } else {
                None
            }
        };
        
        if let Some(frame) = frame_to_save {
            let timestamp = Local::now().format("%Y%m%d_%H%M%S");
            let filename = format!("{}/microscope_{}.jpg", self.save_directory, timestamp);
            
            imgcodecs::imwrite(&filename, &frame, &opencv::core::Vector::new())?;
            
            self.add_log(format!("Image saved: {}", filename));
            return Ok(());
        }
        
        Err(MicroscopeError::CaptureError("No frame to save".to_string()))
    }
    
    fn update_frame_texture(&mut self, ctx: &egui::Context) {
        if let Ok(current_frame) = self.current_frame.lock() {
            if let Some(ref frame) = *current_frame {
                // OpenCV Mat to egui texture conversion
                if let Ok(rgb_frame) = self.mat_to_rgb_image(frame) {
                    let size = [rgb_frame.width() as usize, rgb_frame.height() as usize];
                    let flat_samples = rgb_frame.as_flat_samples();
                    let pixels = flat_samples.as_slice();
                    
                    let color_image = egui::ColorImage::from_rgb(size, pixels);
                    
                    if let Some(ref mut texture) = self.frame_texture {
                        texture.set(color_image, egui::TextureOptions::default());
                    } else {
                        self.frame_texture = Some(ctx.load_texture(
                            "microscope_frame",
                            color_image,
                            egui::TextureOptions::default(),
                        ));
                    }
                }
            }
        }
    }
    
    fn mat_to_rgb_image(&self, mat: &Mat) -> Result<image::RgbImage, MicroscopeError> {
        let mut rgb_mat = Mat::default();
        imgproc::cvt_color(mat, &mut rgb_mat, imgproc::COLOR_BGR2RGB, 0)?;
        
        let rows = rgb_mat.rows();
        let cols = rgb_mat.cols();
        let data = rgb_mat.data_bytes()?;
        
        image::RgbImage::from_raw(cols as u32, rows as u32, data.to_vec())
            .ok_or_else(|| MicroscopeError::CaptureError("Image conversion failed".to_string()))
    }
}

impl eframe::App for MicroscopeApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Capture frames during streaming
        if self.is_streaming {
            if let Err(e) = self.capture_frame() {
                error!("Frame capture error: {}", e);
            } else {
                self.update_frame_texture(ctx);
            }
        }
        
        // Main UI
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("🔬 USB Microscope Control - Rust Edition");
            ui.separator();
            
            // Connection panel
            ui.horizontal(|ui| {
                if ui.button(if self.is_connected { "🔌 Disconnect" } else { "🔌 Connect" }).clicked() {
                    if self.is_connected {
                        self.disconnect_microscope();
                    } else {
                        if let Err(e) = self.connect_microscope() {
                            self.add_log(format!("Connection failed: {}", e));
                        }
                    }
                }
                
                ui.label(format!("Status: {}", if self.is_connected { "✅ Connected" } else { "❌ Disconnected" }));
                
                if self.is_connected {
                    ui.separator();
                    if ui.button(if self.is_streaming { "⏹ Stop" } else { "▶ Start" }).clicked() {
                        if self.is_streaming {
                            self.stop_streaming();
                        } else {
                            self.start_streaming();
                        }
                    }
                    
                    if self.is_streaming {
                        ui.label(format!("FPS: {:.1}", self.fps));
                    }
                }
            });
            
            ui.separator();
            
            // Video display area
            if let Some(ref texture) = self.frame_texture {
                let available_size = ui.available_size();
                let image_size = texture.size_vec2();
                let aspect_ratio = image_size.x / image_size.y;
                
                // Scale to fit screen
                let display_size = if available_size.x / aspect_ratio < available_size.y - 200.0 {
                    egui::vec2(available_size.x, available_size.x / aspect_ratio)
                } else {
                    egui::vec2((available_size.y - 200.0) * aspect_ratio, available_size.y - 200.0)
                };
                
                ui.add(egui::Image::from_texture(texture).fit_to_exact_size(display_size));
            } else {
                let available_size = ui.available_size();
                ui.allocate_ui_with_layout(
                    egui::vec2(available_size.x, 300.0),
                    egui::Layout::centered_and_justified(egui::Direction::TopDown),
                    |ui| {
                        ui.label("📹 No Video");
                        if !self.is_connected {
                            ui.label("Please connect the microscope");
                        } else if !self.is_streaming {
                            ui.label("Please start streaming");
                        }
                    },
                );
            }
        });
        
        // Side panel - Controls
        egui::SidePanel::right("controls").show(ctx, |ui| {
            ui.heading("🎛️ Controls");
            
            if self.is_connected {
                ui.separator();
                
                // Resolution selection
                ui.label("Resolution:");
                egui::ComboBox::from_label("")
                    .selected_text(self.resolutions[self.resolution_index].2)
                    .show_ui(ui, |ui| {
                        for (i, (_, _, name)) in self.resolutions.iter().enumerate() {
                            ui.selectable_value(&mut self.resolution_index, i, *name);
                        }
                    });
                
                ui.separator();
                
                // Brightness control
                ui.label("Brightness:");
                ui.add(egui::Slider::new(&mut self.brightness, 0.0..=1.0).step_by(0.01));
                
                // Contrast control
                ui.label("Contrast:");
                ui.add(egui::Slider::new(&mut self.contrast, 0.0..=1.0).step_by(0.01));
                
                ui.separator();
                
                // Save options
                ui.checkbox(&mut self.auto_save, "Auto Save");
                
                if ui.button("📸 Take Photo").clicked() {
                    if let Err(e) = self.save_image() {
                        self.add_log(format!("Save failed: {}", e));
                    }
                }
                
                if ui.button("📁 Select Save Folder").clicked() {
                    if let Some(path) = rfd::FileDialog::new().pick_folder() {
                        self.save_directory = path.display().to_string();
                        self.add_log(format!("Save folder: {}", self.save_directory));
                    }
                }
                
                ui.label(format!("Save location: {}", self.save_directory));
            }
        });
        
        // Bottom panel - Logs
        egui::TopBottomPanel::bottom("logs").show(ctx, |ui| {
            ui.heading("📋 Logs");
            
            egui::ScrollArea::vertical()
                .max_height(150.0)
                .stick_to_bottom(true)
                .show(ui, |ui| {
                    for message in &self.log_messages {
                        ui.label(message);
                    }
                });
        });
        
        // Request continuous repaint for streaming
        if self.is_streaming {
            ctx.request_repaint_after(Duration::from_millis(33)); // ~30 FPS
        }
    }
}
