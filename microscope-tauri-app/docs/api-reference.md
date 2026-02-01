# 🔌 API Reference

## Tauri Backend Commands

This document provides detailed API reference for all Tauri commands provided by the Rust backend.

## 📡 Commands Overview

| Command | Description | Parameters | Return Type |
|---------|-------------|------------|-------------|
| `check_microscope` | Check microscope connection status | None | `MicroscopeStatus` |
| `capture_image` | Capture image | None | `CaptureResult` |
| `start_streaming` | Start live streaming | None | `boolean` |
| `stop_streaming` | Stop live streaming | None | `boolean` |
| `save_image` | Save image file | `image_base64`, `filename` | `string` |

## 📊 Data Types

### MicroscopeStatus

Represents the current connection status and configuration information of the microscope.

```typescript
interface MicroscopeStatus {
  connected: boolean;      // Connection status
  device_id?: string;      // USB device ID (e.g., "05e3:f12a")
  resolution: string;      // Current resolution (e.g., "640x480")
  fps: number;            // Frame rate (e.g., 30.0)
}
```

**Example Response:**
```json
{
  "connected": true,
  "device_id": "05e3:f12a",
  "resolution": "640x480",
  "fps": 30.0
}
```

### CaptureResult

Represents the result of an image capture operation.

```typescript
interface CaptureResult {
  success: boolean;        // Whether capture was successful
  image_path?: string;     // Temporarily saved image path
  image_base64?: string;   // Base64 encoded image data
  error?: string;          // Error message (on failure)
}
```

**Success Response:**
```json
{
  "success": true,
  "image_path": "/tmp/microscope_capture.jpg",
  "image_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "image_path": null,
  "image_base64": null,
  "error": "Cannot open camera"
}
```

## 🔍 Command Details

### check_microscope()

Check the connection status of the microscope. Scans the USB device list to find supported microscopes.

**Signature:**
```rust
#[tauri::command]
async fn check_microscope() -> Result<MicroscopeStatus, String>
```

**Frontend Usage:**
```typescript
import { invoke } from "@tauri-apps/api/core";

const checkConnection = async () => {
  try {
    const status = await invoke<MicroscopeStatus>("check_microscope");
    console.log("Microscope status:", status);
    
    if (status.connected) {
      console.log(`Connected to ${status.device_id}`);
    } else {
      console.log("No microscope found");
    }
  } catch (error) {
    console.error("Failed to check microscope:", error);
  }
};
```

**Internal Process:**
1. Execute Python script to call `lsusb` command
2. Search for `05e3:f12a` (Genesys Logic Digital Microscope) in USB device list
3. Set connection status to `true` if found
4. Include default resolution (640x480) and frame rate (30fps) information

**Possible Errors:**
- `"Failed to execute command"`: System command execution failed
- `"USB device not found"`: Microscope not connected

---

### capture_image()

Capture a single image from the microscope. Uses OpenCV to read frames from `/dev/video4`.

**Signature:**
```rust
#[tauri::command]
async fn capture_image() -> Result<CaptureResult, String>
```

**Frontend Usage:**
```typescript
const capturePhoto = async () => {
  try {
    const result = await invoke<CaptureResult>("capture_image");
    
    if (result.success && result.image_base64) {
      // Display image on screen
      const imageUrl = `data:image/jpeg;base64,${result.image_base64}`;
      setCurrentImage(imageUrl);
      
      console.log("Image captured successfully");
    } else {
      console.error("Capture failed:", result.error);
    }
  } catch (error) {
    console.error("Capture error:", error);
  }
};
```

**Internal Process:**
1. Execute Python OpenCV script
2. Open camera with `cv2.VideoCapture(4)`
3. Read single frame (`cap.read()`)
4. Save to temporary file (`/tmp/microscope_capture.jpg`)
5. Encode to Base64 and return
6. Release camera resources

**Possible Errors:**
- `"Cannot open camera"`: Camera device access failed
- `"Cannot capture frame"`: Frame reading failed
- `"Unknown error occurred"`: Other Python script errors

---

### start_streaming()

Start real-time video streaming. (Currently placeholder implementation)

**Signature:**
```rust
#[tauri::command]
async fn start_streaming() -> Result<bool, String>
```

**Frontend Usage:**
```typescript
const startStream = async () => {
  try {
    const success = await invoke<boolean>("start_streaming");
    if (success) {
      setIsStreaming(true);
      console.log("Streaming started");
    }
  } catch (error) {
    console.error("Failed to start streaming:", error);
  }
};
```

**Note:** Current version always returns `true`. Future implementation will include real-time streaming via WebRTC or WebSocket.

---

### stop_streaming()

Stop real-time video streaming.

**Signature:**
```rust
#[tauri::command]
async fn stop_streaming() -> Result<bool, String>
```

**Frontend Usage:**
```typescript
const stopStream = async () => {
  try {
    const success = await invoke<boolean>("stop_streaming");
    if (success) {
      setIsStreaming(false);
      console.log("Streaming stopped");
    }
  } catch (error) {
    console.error("Failed to stop streaming:", error);
  }
};
```

---

### save_image(image_base64, filename)

Save captured image with specified filename.

**Signature:**
```rust
#[tauri::command]
async fn save_image(image_base64: String, filename: String) -> Result<String, String>
```

**Parameters:**
- `image_base64`: Base64 encoded image data
- `filename`: Filename to save (including extension)

**Frontend Usage:**
```typescript
const saveCurrentImage = async () => {
  if (!currentImage) return;
  
  try {
    // Remove header from Base64 data
    const base64Data = currentImage.split(',')[1];
    
    // Generate timestamp-based filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `microscope_${timestamp}.jpg`;
    
    const savedPath = await invoke<string>("save_image", {
      imageBase64: base64Data,
      filename: filename
    });
    
    console.log(`Image saved to: ${savedPath}`);
  } catch (error) {
    console.error("Save failed:", error);
  }
};
```

**Internal Process:**
1. Decode Base64 data to binary
2. Check home directory path (`$HOME`)
3. Create file path (`$HOME/filename`)
4. Save binary data to file
5. Return full path of saved file

**Possible Errors:**
- `"Failed to decode base64"`: Base64 decoding failed
- `"Failed to save image"`: File save failed (permissions, disk space, etc.)

## 🔧 Error Handling

### Error Types

All commands return `Result<T, String>` type and provide string-format error messages when errors occur.

### Frontend Error Handling Pattern

```typescript
const handleApiCall = async () => {
  try {
    const result = await invoke<ResultType>("command_name", parameters);
    // Success handling
    handleSuccess(result);
  } catch (error) {
    // Error handling
    console.error("API call failed:", error);
    
    // Display error message to user
    addLog(`Error: ${error}`);
    
    // Retry logic if needed
    if (shouldRetry(error)) {
      setTimeout(handleApiCall, 1000);
    }
  }
};
```

### Common Error Scenarios

1. **Permission Error**: No camera access permission
   ```bash
   sudo usermod -a -G video $USER
   ```

2. **Device Error**: Microscope not connected
   ```bash
   lsusb | grep -i microscope
   ```

3. **Python Error**: OpenCV library issues
   ```bash
   pip3 install --upgrade opencv-python
   ```

## 🚀 Performance Considerations

### Async Operations

All commands execute asynchronously to avoid blocking the UI.

```typescript
// Execute multiple operations in parallel
const [status, image] = await Promise.all([
  invoke<MicroscopeStatus>("check_microscope"),
  invoke<CaptureResult>("capture_image")
]);
```

### Memory Management

- Base64 image data can use significant memory, so keep only when necessary
- Display captured images immediately and release when not needed
- Consider chunk-based processing for large images

### Rate Limiting

```typescript
// Debouncing to prevent continuous calls
const debouncedCapture = useMemo(
  () => debounce(captureImage, 1000),
  []
);
```

## 🔮 Future API Extensions

### Planned Commands

1. **`set_resolution(width, height)`**: Change resolution
2. **`adjust_brightness(level)`**: Adjust brightness
3. **`adjust_contrast(level)`**: Adjust contrast
4. **`get_device_info()`**: Detailed device information
5. **`start_recording()`**: Start video recording
6. **`stop_recording()`**: Stop video recording

### WebSocket Integration

WebSocket-based API for real-time streaming:

```typescript
// Future implementation
const streamSocket = new WebSocket('ws://localhost:8080/stream');
streamSocket.onmessage = (event) => {
  const frameData = JSON.parse(event.data);
  updateVideoFrame(frameData.image_base64);
};
```

This API reference enables developers to efficiently interact with the Tauri backend.