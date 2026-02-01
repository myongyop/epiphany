# 🛠️ Development Guide

## Development Environment Setup

### 1. System Requirements

#### Ubuntu/Linux
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Node.js and pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh

# System dependencies
sudo apt update
sudo apt install -y \
    libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    python3-opencv \
    python3-pip
```

#### macOS
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install rust node pnpm python opencv
```

#### Windows
```powershell
# Install via Chocolatey
choco install rust nodejs python opencv

# Or install directly
# - Rust: https://rustup.rs/
# - Node.js: https://nodejs.org/
# - Python: https://python.org/
```

### 2. Project Setup

```bash
# Clone project
git clone <repository-url>
cd microscope-tauri-app

# Install dependencies
pnpm install

# Python dependencies
pip3 install opencv-python base64 subprocess
```

## Development Workflow

### 1. Run Development Server
```bash
# Development mode (with hot reload)
pnpm tauri dev

# Run on specific port
VITE_PORT=3000 pnpm tauri dev
```

### 2. Code Modification Cycle

#### Frontend (React/TypeScript)
```bash
# Work in src/ directory
# - App.tsx: Main component
# - App.css: Styling
# - main.tsx: Entry point

# Type checking
pnpm tsc --noEmit

# Linting
pnpm eslint src/
```

#### Backend (Rust)
```bash
# Work in src-tauri/src/ directory
# - lib.rs: API handlers

# Code formatting
cargo fmt

# Linting
cargo clippy

# Testing
cargo test
```

### 3. Build and Deployment

```bash
# Development build
pnpm tauri build --debug

# Production build
pnpm tauri build

# Build for specific platform
pnpm tauri build --target x86_64-pc-windows-msvc  # Windows
pnpm tauri build --target x86_64-apple-darwin     # macOS
pnpm tauri build --target x86_64-unknown-linux-gnu # Linux
```

## Code Structure and Patterns

### Frontend Architecture

#### Component Structure
```typescript
// App.tsx - Main application
interface MicroscopeStatus {
  connected: boolean;
  device_id?: string;
  resolution: string;
  fps: number;
}

interface CaptureResult {
  success: boolean;
  image_path?: string;
  image_base64?: string;
  error?: string;
}
```

#### State Management
```typescript
// Using React Hooks
const [status, setStatus] = useState<MicroscopeStatus>();
const [currentImage, setCurrentImage] = useState<string>("");
const [logs, setLogs] = useState<string[]>([]);

// Check status every 5 seconds
useEffect(() => {
  const interval = setInterval(checkMicroscope, 5000);
  return () => clearInterval(interval);
}, []);
```

### Backend Architecture

#### Tauri Commands
```rust
// Check microscope status
#[tauri::command]
async fn check_microscope() -> Result<MicroscopeStatus, String> {
    // Execute Python script
    let output = Command::new("python3")
        .arg("-c")
        .arg("import subprocess; ...")
        .output()?;
    
    // Parse results and return
}

// Image capture
#[tauri::command]
async fn capture_image() -> Result<CaptureResult, String> {
    // Image capture through OpenCV
    // Base64 encoding
    // Return results
}
```

#### Error Handling
```rust
#[derive(Debug, Serialize, Deserialize)]
pub enum MicroscopeError {
    OpenCvError(String),
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
```

## Debugging Guide

### 1. Frontend Debugging

#### Browser Developer Tools
```bash
# F12 or Ctrl+Shift+I in development mode
# Check logs in Console tab
console.log("Debug info:", status);
```

#### React DevTools
```bash
# Install Chrome extension
# Check state in Components tab
```

### 2. Backend Debugging

#### Rust Logs
```rust
use log::{info, warn, error, debug};

#[tauri::command]
async fn debug_function() -> Result<String, String> {
    debug!("Function called");
    info!("Processing request");
    warn!("Potential issue detected");
    error!("Error occurred");
    Ok("Success".to_string())
}
```

#### Environment Variables
```bash
# Set log level
RUST_LOG=debug pnpm tauri dev
RUST_LOG=info pnpm tauri dev
```

### 3. Python Script Debugging

#### Direct Execution
```bash
# Test Python script independently
python3 -c "
import cv2
cap = cv2.VideoCapture(4)
print('Camera opened:', cap.isOpened())
ret, frame = cap.read()
print('Frame captured:', ret)
cap.release()
"
```

#### Log Output
```python
import sys
print('DEBUG: Camera initialization', file=sys.stderr)
```

## Performance Optimization

### 1. Frontend Optimization

#### React Optimization
```typescript
// Memoization
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data}</div>;
});

// Callback optimization
const handleClick = useCallback(() => {
  // Handler logic
}, [dependency]);

// Effect optimization
useEffect(() => {
  // Effect logic
}, [specificDependency]); // Specific dependencies instead of empty array
```

#### CSS Optimization
```css
/* Utilize GPU acceleration */
.animated-element {
  transform: translateZ(0);
  will-change: transform;
}

/* Efficient selectors */
.specific-class > .child-element {
  /* Use specific selectors */
}
```

### 2. Backend Optimization

#### Rust Optimization
```rust
// Async processing
#[tauri::command]
async fn async_operation() -> Result<String, String> {
    tokio::spawn(async {
        // Async work
    }).await.map_err(|e| e.to_string())?
}

// Memory efficient processing
fn process_image(data: &[u8]) -> Result<Vec<u8>, String> {
    // Use references to minimize copying
}
```

#### Compilation Optimization
```toml
# Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = "abort"
```

## Testing Strategy

### 1. Unit Tests

#### Frontend Testing
```typescript
// Jest + React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders microscope control interface', () => {
  render(<App />);
  expect(screen.getByText('USB Microscope Control')).toBeInTheDocument();
});

test('capture button works', async () => {
  render(<App />);
  const captureButton = screen.getByText('Capture');
  fireEvent.click(captureButton);
  // Check async results
});
```

#### Backend Testing
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_check_microscope() {
        let result = check_microscope().await;
        assert!(result.is_ok());
    }

    #[test]
    fn test_error_handling() {
        let error = MicroscopeError::ConnectionError("Test".to_string());
        assert_eq!(error.to_string(), "Connection Error: Test");
    }
}
```

### 2. Integration Tests

```bash
# E2E testing (Playwright etc.)
pnpm add -D @playwright/test

# Run tests
pnpm playwright test
```

## Deployment Guide

### 1. Local Build
```bash
# Build for all platforms
pnpm tauri build

# Output locations
# - Linux: src-tauri/target/release/bundle/deb/
# - Windows: src-tauri/target/release/bundle/msi/
# - macOS: src-tauri/target/release/bundle/dmg/
```

### 2. CI/CD Setup

#### GitHub Actions
```yaml
name: Build and Release

on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      
      - run: pnpm install
      - run: pnpm tauri build
```

### 3. Auto Updates

```rust
// Tauri auto-update setup
use tauri::updater;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let handle = app.handle();
            tauri::async_runtime::spawn(async move {
                updater::builder(handle).check().await;
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Security Considerations

### 1. Tauri Security Settings
```json
// tauri.conf.json
{
  "tauri": {
    "security": {
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'",
      "dangerousDisableAssetCspModification": false
    },
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "execute": true,
        "sidecar": false
      }
    }
  }
}
```

### 2. Input Validation
```rust
#[tauri::command]
async fn save_image(image_base64: String, filename: String) -> Result<String, String> {
    // Filename validation
    if filename.contains("..") || filename.contains("/") {
        return Err("Invalid filename".to_string());
    }
    
    // Base64 validation
    if !image_base64.chars().all(|c| c.is_alphanumeric() || c == '+' || c == '/' || c == '=') {
        return Err("Invalid base64 data".to_string());
    }
    
    // Continue processing...
}
```

This guide enables developers to efficiently develop and maintain the project.