"""
Computer Vision Image Enhancement & Edge Detection Studio
Main GUI Application

A desktop application for demonstrating Computer Vision concepts including:
- Digital Image Representation
- Point Processing Operations
- Spatial Filtering
- Edge Detection
- Image Enhancement
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import image_processing as ip


class ImageProcessingStudio:
    """Main application class for Computer Vision Studio"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Computer Vision Image Enhancement & Edge Detection Studio")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Image variables
        self.original_image = None
        self.processed_image = None
        self.current_image = None
        self.filename = ""
        
        # Display size for images
        self.display_width = 500
        self.display_height = 400
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title Section
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="COMPUTER VISION IMAGE PROCESSING STUDIO",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image Display Section
        image_frame = tk.Frame(main_frame, bg='#f0f0f0')
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Original Image Panel
        original_panel = tk.Frame(image_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        original_panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        original_label = tk.Label(
            original_panel,
            text="ORIGINAL IMAGE",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        original_label.pack(pady=10)
        
        self.original_image_label = tk.Label(original_panel, bg='#ecf0f1')
        self.original_image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Processed Image Panel
        processed_panel = tk.Frame(image_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        processed_panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        processed_label = tk.Label(
            processed_panel,
            text="PROCESSED IMAGE",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        processed_label.pack(pady=10)
        
        self.processed_image_label = tk.Label(processed_panel, bg='#ecf0f1')
        self.processed_image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Control Buttons Section
        control_frame = tk.Frame(main_frame, bg='#f0f0f0')
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # File operation buttons
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 15, 'height': 2}
        
        tk.Button(
            control_frame,
            text="Upload Image",
            bg='#3498db',
            fg='white',
            command=self.upload_image,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Reset",
            bg='#e74c3c',
            fg='white',
            command=self.reset_image,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Save Result",
            bg='#2ecc71',
            fg='white',
            command=self.save_image,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Image Info",
            bg='#9b59b6',
            fg='white',
            command=self.show_image_info,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Processing Operations Section
        operations_frame = tk.Frame(main_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        operations_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        operations_title = tk.Label(
            operations_frame,
            text="IMAGE PROCESSING OPERATIONS",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        operations_title.pack(pady=10)
        
        # Basic Operations Row
        basic_ops_frame = tk.Frame(operations_frame, bg='white')
        basic_ops_frame.pack(pady=5)
        
        btn_op_style = {'font': ('Arial', 9, 'bold'), 'width': 15, 'height': 2}
        
        tk.Button(
            basic_ops_frame,
            text="Grayscale",
            bg='#34495e',
            fg='white',
            command=self.apply_grayscale,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            basic_ops_frame,
            text="Gaussian Blur",
            bg='#16a085',
            fg='white',
            command=self.apply_gaussian_blur,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            basic_ops_frame,
            text="Median Filter",
            bg='#27ae60',
            fg='white',
            command=self.apply_median_filter,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            basic_ops_frame,
            text="Sharpen",
            bg='#f39c12',
            fg='white',
            command=self.apply_sharpening,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Edge Detection Row
        edge_ops_frame = tk.Frame(operations_frame, bg='white')
        edge_ops_frame.pack(pady=5)
        
        tk.Button(
            edge_ops_frame,
            text="Sobel Edge",
            bg='#c0392b',
            fg='white',
            command=self.apply_sobel_edge,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            edge_ops_frame,
            text="Canny Edge",
            bg='#8e44ad',
            fg='white',
            command=self.apply_canny_edge,
            **btn_op_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Sliders Section
        sliders_frame = tk.Frame(operations_frame, bg='white')
        sliders_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Brightness Slider
        brightness_frame = tk.Frame(sliders_frame, bg='white')
        brightness_frame.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        tk.Label(
            brightness_frame,
            text="Brightness (-100 to +100):",
            font=('Arial', 10),
            bg='white'
        ).pack(anchor=tk.W)
        
        self.brightness_var = tk.IntVar(value=0)
        self.brightness_slider = tk.Scale(
            brightness_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.brightness_var,
            bg='white',
            length=300
        )
        self.brightness_slider.pack(fill=tk.X)
        
        tk.Button(
            brightness_frame,
            text="Apply Brightness",
            bg='#3498db',
            fg='white',
            command=self.apply_brightness,
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
        
        # Contrast Slider
        contrast_frame = tk.Frame(sliders_frame, bg='white')
        contrast_frame.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        tk.Label(
            contrast_frame,
            text="Contrast (0.5 to 2.0):",
            font=('Arial', 10),
            bg='white'
        ).pack(anchor=tk.W)
        
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.contrast_slider = tk.Scale(
            contrast_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.contrast_var,
            bg='white',
            length=300
        )
        self.contrast_slider.pack(fill=tk.X)
        
        tk.Button(
            contrast_frame,
            text="Apply Contrast",
            bg='#3498db',
            fg='white',
            command=self.apply_contrast,
            font=('Arial', 9, 'bold')
        ).pack(pady=5)
    
    def upload_image(self):
        """Handle image upload from file system"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Read image using OpenCV
                image = cv2.imread(file_path)
                
                if image is None:
                    messagebox.showerror("Error", "Failed to load image. Please select a valid image file.")
                    return
                
                # Store the original image and filename
                self.original_image = image.copy()
                self.current_image = image.copy()
                self.processed_image = image.copy()
                self.filename = os.path.basename(file_path)
                
                # Reset sliders
                self.brightness_var.set(0)
                self.contrast_var.set(1.0)
                
                # Display images
                self.display_image(self.original_image, self.original_image_label)
                self.display_image(self.processed_image, self.processed_image_label)
                
                messagebox.showinfo("Success", f"Image loaded successfully!\n{self.filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the image:\n{str(e)}")
    
    def display_image(self, image, label):
        """Display image in the GUI label with proper resizing"""
        if image is None:
            return
        
        # Convert from BGR to RGB for display
        if len(image.shape) == 3:
            display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            display_img = image
        
        # Convert to PIL Image
        pil_image = Image.fromarray(display_img)
        
        # Resize to fit display area while maintaining aspect ratio
        pil_image.thumbnail((self.display_width, self.display_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update label
        label.config(image=photo)
        label.image = photo  # Keep a reference
    
    def check_image_loaded(self):
        """Check if an image has been loaded"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return False
        return True
    
    def apply_grayscale(self):
        """Convert current image to grayscale"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.convert_to_grayscale(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply grayscale:\n{str(e)}")
    
    def apply_brightness(self):
        """Apply brightness adjustment"""
        if not self.check_image_loaded():
            return
        
        try:
            brightness_value = self.brightness_var.get()
            self.processed_image = ip.adjust_brightness(self.current_image, brightness_value)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply brightness:\n{str(e)}")
    
    def apply_contrast(self):
        """Apply contrast adjustment"""
        if not self.check_image_loaded():
            return
        
        try:
            contrast_value = self.contrast_var.get()
            self.processed_image = ip.adjust_contrast(self.current_image, contrast_value)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply contrast:\n{str(e)}")
    
    def apply_gaussian_blur(self):
        """Apply Gaussian blur filter"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.apply_gaussian_blur(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply Gaussian blur:\n{str(e)}")
    
    def apply_median_filter(self):
        """Apply median filter"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.apply_median_filter(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply median filter:\n{str(e)}")
    
    def apply_sharpening(self):
        """Apply sharpening filter"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.apply_sharpening(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply sharpening:\n{str(e)}")
    
    def apply_sobel_edge(self):
        """Apply Sobel edge detection"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.apply_sobel_edge_detection(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply Sobel edge detection:\n{str(e)}")
    
    def apply_canny_edge(self):
        """Apply Canny edge detection"""
        if not self.check_image_loaded():
            return
        
        try:
            self.processed_image = ip.apply_canny_edge_detection(self.current_image)
            self.current_image = self.processed_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply Canny edge detection:\n{str(e)}")
    
    def reset_image(self):
        """Reset to original image"""
        if not self.check_image_loaded():
            return
        
        try:
            self.current_image = self.original_image.copy()
            self.processed_image = self.original_image.copy()
            self.brightness_var.set(0)
            self.contrast_var.set(1.0)
            self.display_image(self.processed_image, self.processed_image_label)
            messagebox.showinfo("Reset", "Image has been reset to original!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset image:\n{str(e)}")
    
    def save_image(self):
        """Save the processed image"""
        if not self.check_image_loaded():
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Processed Image",
                defaultextension=".png",
                filetypes=[
                    ("PNG Files", "*.png"),
                    ("JPEG Files", "*.jpg *.jpeg"),
                    ("All Files", "*.*")
                ]
            )
            
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Success", f"Image saved successfully!\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
    
    def show_image_info(self):
        """Display image information"""
        if not self.check_image_loaded():
            return
        
        try:
            info = ip.get_image_info(self.processed_image, self.filename)
            
            info_text = f"""
IMAGE INFORMATION
{'='*40}

File Name: {info['filename']}
Width: {info['width']} pixels
Height: {info['height']} pixels
Channels: {info['channels']}
Image Type: {info['type']}
Data Type: {info['dtype']}
Total Pixels: {info['size']}

Resolution: {info['width']} x {info['height']}
            """
            
            messagebox.showinfo("Image Information", info_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get image information:\n{str(e)}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ImageProcessingStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
