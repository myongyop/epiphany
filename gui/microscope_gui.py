#!/usr/bin/env python3
"""
USB Microscope GUI Application
Microscope control interface using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import sys
import os

# Import driver module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from driver.microscope_driver import MicroscopeDriver

class MicroscopeGUI:
    """Microscope GUI class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("USB Microscope Control")
        self.root.geometry("800x600")
        
        self.driver = MicroscopeDriver()
        self.is_streaming = False
        self.current_frame = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Connection frame
        connection_frame = ttk.LabelFrame(main_frame, text="Connection", padding="5")
        connection_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.connect_btn = ttk.Button(connection_frame, text="Connect", command=self.connect_microscope)
        self.connect_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.disconnect_btn = ttk.Button(connection_frame, text="Disconnect", command=self.disconnect_microscope, state="disabled")
        self.disconnect_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.status_label = ttk.Label(connection_frame, text="Not connected")
        self.status_label.grid(row=0, column=2, padx=(10, 0))
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="5")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # LED brightness control
        ttk.Label(control_frame, text="LED Brightness:").grid(row=0, column=0, sticky=tk.W)
        self.brightness_var = tk.IntVar(value=128)
        self.brightness_scale = ttk.Scale(
            control_frame, 
            from_=0, 
            to=255, 
            variable=self.brightness_var,
            command=self.on_brightness_change
        )
        self.brightness_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Video control
        ttk.Label(control_frame, text="Video:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.start_video_btn = ttk.Button(control_frame, text="Start Stream", command=self.start_video, state="disabled")
        self.start_video_btn.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        self.stop_video_btn = ttk.Button(control_frame, text="Stop Stream", command=self.stop_video, state="disabled")
        self.stop_video_btn.grid(row=1, column=1, sticky=tk.W, padx=(85, 0), pady=(10, 0))
        
        # Capture button
        self.capture_btn = ttk.Button(control_frame, text="Take Photo", command=self.capture_image, state="disabled")
        self.capture_btn.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        
        # Video frame
        video_frame = ttk.LabelFrame(main_frame, text="Video", padding="5")
        video_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.video_label = ttk.Label(video_frame, text="No video", background="black", foreground="white")
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Device Information", padding="5")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=6, width=70)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar
        info_scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        # Grid weight configuration
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        
    def connect_microscope(self):
        """Connect microscope"""
        if self.driver.connect():
            self.status_label.config(text="Connected")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            self.start_video_btn.config(state="normal")
            self.capture_btn.config(state="normal")
            
            # Display device information
            info = self.driver.get_device_info()
            self.info_text.delete(1.0, tk.END)
            for key, value in info.items():
                self.info_text.insert(tk.END, f"{key}: {value}\n")
        else:
            messagebox.showerror("Error", "Failed to connect to microscope.")
    
    def disconnect_microscope(self):
        """Disconnect microscope"""
        if self.is_streaming:
            self.stop_video()
        
        self.driver.disconnect()
        self.status_label.config(text="Not connected")
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.start_video_btn.config(state="disabled")
        self.stop_video_btn.config(state="disabled")
        self.capture_btn.config(state="disabled")
        
        self.info_text.delete(1.0, tk.END)
        self.video_label.config(image="", text="No video")
    
    def on_brightness_change(self, value):
        """LED brightness change"""
        if self.driver.is_connected:
            brightness = int(float(value))
            self.driver.set_led_brightness(brightness)
    
    def start_video(self):
        """Start video stream"""
        if not self.is_streaming:
            self.is_streaming = True
            self.driver.start_video_stream()
            self.start_video_btn.config(state="disabled")
            self.stop_video_btn.config(state="normal")
            
            # Start video stream thread (for actual implementation)
            # self.video_thread = threading.Thread(target=self.video_loop)
            # self.video_thread.daemon = True
            # self.video_thread.start()
            
            # Currently show dummy image
            self.show_dummy_video()
    
    def stop_video(self):
        """Stop video stream"""
        if self.is_streaming:
            self.is_streaming = False
            self.driver.stop_video_stream()
            self.start_video_btn.config(state="normal")
            self.stop_video_btn.config(state="disabled")
            self.video_label.config(image="", text="Video stopped")
    
    def show_dummy_video(self):
        """Show actual microscope video"""
        if not self.driver.is_connected:
            return
        
        # Capture actual frame
        frame = self.driver.capture_frame()
        
        if frame is not None:
            # Convert OpenCV BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL image
            pil_image = Image.fromarray(frame_rgb)
            pil_image = pil_image.resize((400, 300))
            
            # Convert to tkinter image
            tk_image = ImageTk.PhotoImage(pil_image)
            
            self.video_label.config(image=tk_image, text="")
            self.video_label.image = tk_image  # Keep reference
            
            self.current_frame = frame
        else:
            # Connected but cannot get frame
            self.video_label.config(image="", text="No frame\n(Check lighting)")
            
        # Update again after 1 second (real-time effect)
        if self.is_streaming:
            self.root.after(1000, self.show_dummy_video)
    
    def video_loop(self):
        """Video loop (for actual implementation)"""
        while self.is_streaming:
            frame = self.driver.capture_frame()
            if frame is not None:
                # Display frame in GUI
                self.display_frame(frame)
            time.sleep(0.033)  # ~30 FPS
    
    def display_frame(self, frame):
        """Display frame in GUI"""
        # Convert OpenCV BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL image
        pil_image = Image.fromarray(frame_rgb)
        pil_image = pil_image.resize((400, 300))
        
        # Convert to tkinter image
        tk_image = ImageTk.PhotoImage(pil_image)
        
        self.video_label.config(image=tk_image)
        self.video_label.image = tk_image  # Keep reference
        
        self.current_frame = frame
    
    def capture_image(self):
        """Capture image"""
        if self.current_frame is not None:
            filename = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                cv2.imwrite(filename, self.current_frame)
                messagebox.showinfo("Success", f"Image saved: {filename}")
        else:
            # Save dummy image
            filename = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                dummy_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                cv2.imwrite(filename, dummy_image)
                messagebox.showinfo("Success", f"Test image saved: {filename}")

def main():
    """Main function"""
    root = tk.Tk()
    app = MicroscopeGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application terminated")

if __name__ == "__main__":
    main()