# 🌐 USB Microscope Tauri App Documentation

## 📋 Project Overview

This project is a modern web GUI application for controlling USB microscopes. 
It uses a hybrid architecture of **Python** (image processing) + **Rust** (backend) + **React + TypeScript** (frontend).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React + TS    │    │   Rust Backend  │    │  Python OpenCV │
│   (Frontend)    │◄──►│   (Tauri API)   │◄──►│ (Image Process) │
│                 │    │                 │    │                 │
│ • Modern UI     │    │ • Fast API      │    │ • Camera Access│
│ • Real-time     │    │ • Cross-platform│    │ • Image Capture│
│ • Responsive    │    │ • Memory Safe   │    │ • Base64 Encode│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Key Features

### Frontend (React + TypeScript)
- **Modern Web UI**: Latest React 18 + TypeScript
- **Dark Theme**: Eye-friendly deep dark mode
- **Responsive Design**: Support for all screen sizes
- **Real-time Updates**: Check microscope status every 5 seconds
- **Intuitive UX**: One-click capture and save

### Backend (Rust + Tauri)
- **High Performance API**: Rust's memory safety and speed
- **Cross-platform**: Windows, macOS, Linux support
- **Security**: Tauri security model applied
- **Small Binary**: Optimized bundle size

### Image Processing (Python + OpenCV)
- **Powerful Image Processing**: Utilizing OpenCV library
- **USB Camera Access**: Direct access through V4L2
- **Real-time Capture**: 30fps support
- **Various Formats**: JPEG, PNG, etc. support

## 📁 Project Structure

```
microscope-tauri-app/
├── src/                    # React Frontend
│   ├── App.tsx            # Main application component
│   ├── App.css            # Dark theme styles
│   └── main.tsx           # React entry point
├── src-tauri/             # Rust Backend
│   ├── src/
│   │   └── lib.rs         # Tauri API handlers
│   ├── Cargo.toml         # Rust dependencies
│   └── tauri.conf.json    # Tauri configuration
├── docs/                  # Documentation (this directory)
├── package.json           # Node.js dependencies
└── README.md              # Project introduction
```

## 🛠️ Development Environment Setup

### Prerequisites
- **Node.js** 18+ and pnpm
- **Rust** 1.70+
- **Python** 3.8+ and OpenCV
- **System Libraries**: libgtk-3-dev, webkit2gtk-4.0-dev

### Installation and Execution
```bash
# 1. Install dependencies
pnpm install

# 2. Run development mode
pnpm tauri dev

# 3. Production build
pnpm tauri build
```

## 🎨 UI/UX Design

### Dark Theme
- **Background**: Deep gradient (#0f172a → #334155)
- **Glassmorphism**: Blur effects and translucent panels
- **Neon Accents**: Color coding by status
- **Smooth Animations**: Hover and click effects

### Component Structure
1. **Header**: App title and connection status
2. **Control Panel**: Main function buttons
3. **Image Display**: Show captured images
4. **Activity Log**: Real-time operation history

## 🔧 API Documentation

### Rust Backend Commands

#### `check_microscope()`
Check microscope connection status.
```typescript
const status = await invoke<MicroscopeStatus>("check_microscope");
```

#### `capture_image()`
Capture image from microscope.
```typescript
const result = await invoke<CaptureResult>("capture_image");
```

#### `save_image(imageBase64: string, filename: string)`
Save captured image to file.
```typescript
const path = await invoke<string>("save_image", {
  imageBase64: base64Data,
  filename: "microscope_image.jpg"
});
```

## 🐛 Troubleshooting

### Common Issues

**Q: Microscope not recognized**
```bash
# Check USB devices
lsusb | grep -i microscope

# Check permissions
groups | grep video
```

**Q: Python OpenCV errors**
```bash
# Reinstall OpenCV
pip3 install --upgrade opencv-python
```

**Q: Tauri build errors**
```bash
# Update Rust
rustup update

# Reinstall dependencies
pnpm install
```

## 📈 Performance Optimization

### Frontend
- Prevent unnecessary re-renders using React.memo
- Image lazy loading
- CSS animation optimization

### Backend
- Utilize Rust's zero-cost abstractions
- Prevent UI blocking with asynchronous processing
- Memory-efficient image processing

## 🔮 Future Plans

- [ ] Real-time video streaming
- [ ] Image filters and effects
- [ ] Add measurement tools
- [ ] Cloud storage integration
- [ ] Mobile app version

## 📄 License

MIT License - Free to use, modify, and distribute