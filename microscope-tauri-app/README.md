# 🔬 Epiphany - USB Microscope Control

Professional USB microscope software with modern web interface built on Tauri.

![Epiphany Screenshot](../Microscope%20Image_screenshot_01.02.2026.png)

## ✨ Features

- 🎨 **Modern Dark UI** - Professional Razor-inspired design
- ⚡ **Real-time Streaming** - 30fps live video with minimal latency  
- 📸 **High-Quality Capture** - Professional image capture and saving
- 📊 **Activity Logging** - Comprehensive session tracking and export
- 🔄 **Auto-Connect** - Seamless device detection and connection
- 🎛️ **Intuitive Controls** - One-click operations

## 🚀 Quick Start

```bash
# Install dependencies
pnpm install

# Development mode
pnpm tauri dev

# Production build
pnpm tauri build
```

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: Rust + Tauri  
- **Image Processing**: Python + OpenCV
- **Styling**: Modern CSS with custom properties

## 📱 Interface Components

### Header
- Connection status with visual indicators
- Modern toggle switch for device control
- Real-time FPS and device information

### Controls  
- High-quality image capture
- Live streaming controls
- One-click image saving

### Display
- Real-time microscope feed
- Professional image quality
- Responsive 3:1 layout ratio

### Activity Log
- Session tracking and statistics
- Comprehensive operation logging  
- Export functionality for analysis

## 🔧 Development

### Project Structure
```
src/
├── components/          # Modular UI components
│   ├── Header/         # Connection status and controls
│   ├── Controls/       # Action buttons
│   ├── Display/        # Video display
│   └── Logs/          # Activity logging
├── hooks/              # Custom React hooks
│   ├── useMicroscope.ts # Device management
│   └── useStreaming.ts  # Video streaming
├── types/              # TypeScript definitions
└── App.tsx            # Main application

src-tauri/src/
├── commands/           # API endpoints
│   ├── microscope.rs  # Device commands
│   └── file.rs        # File operations
├── models/            # Data structures
├── utils/             # Helper functions
└── lib.rs            # Main entry point
```

### Key Technologies
- **Tauri 2.0** - Desktop app framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Rust** - Backend performance

## 📊 Performance

- **Startup**: < 2 seconds
- **Memory**: ~50MB runtime
- **Streaming**: 30fps stable
- **Latency**: < 100ms processing

## 🎨 Design System

### Colors
- Primary Teal: `#14b8a6`
- Primary Cyan: `#06b6d4` 
- Accent Green: `#10b981`
- Dark Background: `#0a0a0a`

### Layout
- CSS Grid with 3:1 ratio
- Flexbox component layouts
- Mobile-first responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Free to use, modify, and distribute
