"""
Computer Vision Image Enhancement & Edge Detection Studio - ENHANCED VERSION
Main GUI Application with Advanced Features

Enhanced Features:
- Tabbed interface for better organization
- Real-time preview options
- Histogram visualization
- More CV operations (thresholding, morphological operations, etc.)
- Tooltips for guidance
- Undo/Redo functionality
- Batch processing options
- Better user feedback
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import image_processing as ip


class EnhancedImageProcessingStudio:
    """Enhanced main application class for Computer Vision Studio"""
    
    def __init__(self, root):
        """Initialize the enhanced application"""
        self.root = root
        self.root.title("Computer Vision Image Enhancement & Edge Detection Studio - Enhanced")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        
        # Image variables
        self.original_image = None
        self.processed_image = None
        self.current_image = None
        self.filename = ""
        
        # History for undo/redo
        self.history = []
        self.history_index = -1
        self.max_history = 20
        
        # Display size for images
        self.display_width = 450
        self.display_height = 350
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Upload an image to begin")
        
        # Create menu bar
        self.create_menu()
        
        # Create GUI elements
        self.create_widgets()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image (Ctrl+O)", command=self.upload_image)
        file_menu.add_command(label="Save Result (Ctrl+S)", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset (Ctrl+R)", command=self.reset_image)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Show Histogram", command=self.show_histogram_window)
        view_menu.add_command(label="Image Information", command=self.show_image_info)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Quick Start Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.upload_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-r>', lambda e: self.reset_image())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title Section
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎨 COMPUTER VISION IMAGE PROCESSING STUDIO - ENHANCED",
            font=('Arial', 22, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=18)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image Display Section
        image_frame = tk.Frame(main_frame, bg='#f0f0f0')
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Original Image Panel
        original_panel = tk.Frame(image_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        original_panel.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        original_label = tk.Label(
            original_panel,
            text="📷 ORIGINAL IMAGE",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        original_label.pack(pady=10)
        
        self.original_image_label = tk.Label(original_panel, bg='#ecf0f1', text="No image loaded")
        self.original_image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Processed Image Panel
        processed_panel = tk.Frame(image_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        processed_panel.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        processed_label = tk.Label(
            processed_panel,
            text="✨ PROCESSED IMAGE",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        processed_label.pack(pady=10)
        
        self.processed_image_label = tk.Label(processed_panel, bg='#ecf0f1', text="Apply operations to see results")
        self.processed_image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Control Buttons Section
        control_frame = tk.Frame(main_frame, bg='#f0f0f0')
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 15, 'height': 2}
        
        self.create_tooltip_button(
            control_frame, "📤 Upload Image", '#3498db', 'white',
            self.upload_image, "Load an image from your computer (Ctrl+O)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "↶ Undo", '#95a5a6', 'white',
            self.undo, "Undo last operation (Ctrl+Z)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "↷ Redo", '#95a5a6', 'white',
            self.redo, "Redo last undone operation (Ctrl+Y)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "🔄 Reset", '#e74c3c', 'white',
            self.reset_image, "Reset to original image (Ctrl+R)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "💾 Save Result", '#2ecc71', 'white',
            self.save_image, "Save processed image (Ctrl+S)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "📊 Histogram", '#9b59b6', 'white',
            self.show_histogram_window, "View image histogram", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            control_frame, "ℹ️ Image Info", '#34495e', 'white',
            self.show_image_info, "Display image information", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Tabbed Operations Section
        operations_frame = tk.Frame(main_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        operations_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(operations_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_basic_operations_tab()
        self.create_filters_tab()
        self.create_edge_detection_tab()
        self.create_thresholding_tab()
        self.create_morphological_tab()
        self.create_transform_tab()
        
        # Status Bar
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg='#34495e',
            fg='white',
            anchor=tk.W
        )
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def create_tooltip_button(self, parent, text, bg, fg, command, tooltip, style):
        """Create a button with tooltip"""
        btn = tk.Button(parent, text=text, bg=bg, fg=fg, command=command, **style)
        self.create_tooltip(btn, tooltip)
        return btn
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=('Arial', 9))
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def create_basic_operations_tab(self):
        """Create basic operations tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎨 Basic Operations")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        self.create_tooltip_button(
            row1, "⚫ Grayscale", '#34495e', 'white',
            self.apply_grayscale, "Convert image to black & white", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "🔆 Histogram Eq.", '#e67e22', 'white',
            self.apply_histogram_equalization, "Enhance contrast automatically", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "🔄 Invert", '#8e44ad', 'white',
            self.apply_invert, "Create negative image", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Sliders Section
        sliders_frame = tk.Frame(tab, bg='white')
        sliders_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Brightness Slider
        brightness_frame = tk.Frame(sliders_frame, bg='white')
        brightness_frame.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        tk.Label(
            brightness_frame,
            text="☀️ Brightness (-100 to +100):",
            font=('Arial', 10, 'bold'),
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
            length=300,
            command=self.on_brightness_change
        )
        self.brightness_slider.pack(fill=tk.X)
        
        self.brightness_value_label = tk.Label(brightness_frame, text="Value: 0", bg='white', font=('Arial', 9))
        self.brightness_value_label.pack()
        
        tk.Button(
            brightness_frame,
            text="Apply Brightness",
            bg='#3498db',
            fg='white',
            command=self.apply_brightness,
            font=('Arial', 9, 'bold'),
            width=18
        ).pack(pady=5)
        
        # Contrast Slider
        contrast_frame = tk.Frame(sliders_frame, bg='white')
        contrast_frame.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        tk.Label(
            contrast_frame,
            text="🔅 Contrast (0.5 to 2.0):",
            font=('Arial', 10, 'bold'),
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
            length=300,
            command=self.on_contrast_change
        )
        self.contrast_slider.pack(fill=tk.X)
        
        self.contrast_value_label = tk.Label(contrast_frame, text="Value: 1.0", bg='white', font=('Arial', 9))
        self.contrast_value_label.pack()
        
        tk.Button(
            contrast_frame,
            text="Apply Contrast",
            bg='#3498db',
            fg='white',
            command=self.apply_contrast,
            font=('Arial', 9, 'bold'),
            width=18
        ).pack(pady=5)
    
    def create_filters_tab(self):
        """Create filters tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Filters")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        self.create_tooltip_button(
            row1, "🌫️ Gaussian Blur", '#16a085', 'white',
            self.apply_gaussian_blur, "Smooth image and reduce noise", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "🔲 Median Filter", '#27ae60', 'white',
            self.apply_median_filter, "Remove salt-and-pepper noise", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "✨ Sharpen", '#f39c12', 'white',
            self.apply_sharpening, "Enhance edges and details", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Row 2
        row2 = tk.Frame(tab, bg='white')
        row2.pack(pady=10)
        
        self.create_tooltip_button(
            row2, "🎭 Bilateral Filter", '#3498db', 'white',
            self.apply_bilateral_filter, "Edge-preserving smoothing", btn_style
        ).pack(side=tk.LEFT, padx=5)
    
    def create_edge_detection_tab(self):
        """Create edge detection tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📐 Edge Detection")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        self.create_tooltip_button(
            row1, "📊 Sobel Edge", '#c0392b', 'white',
            self.apply_sobel_edge, "Gradient-based edge detection", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "🎯 Canny Edge", '#8e44ad', 'white',
            self.apply_canny_edge, "Advanced multi-stage edge detection", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "◆ Laplacian Edge", '#d35400', 'white',
            self.apply_laplacian_edge, "Second derivative edge detection", btn_style
        ).pack(side=tk.LEFT, padx=5)
    
    def create_thresholding_tab(self):
        """Create thresholding tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🎚️ Thresholding")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        self.create_tooltip_button(
            row1, "⬛⬜ Binary Threshold", '#2c3e50', 'white',
            self.apply_binary_threshold, "Simple binary thresholding", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "🔄 Adaptive Threshold", '#7f8c8d', 'white',
            self.apply_adaptive_threshold, "Adaptive thresholding for varying lighting", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Threshold value slider
        threshold_frame = tk.Frame(tab, bg='white')
        threshold_frame.pack(pady=20, padx=40, fill=tk.X)
        
        tk.Label(
            threshold_frame,
            text="🎚️ Threshold Value (for Binary Threshold):",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).pack(anchor=tk.W)
        
        self.threshold_var = tk.IntVar(value=127)
        self.threshold_slider = tk.Scale(
            threshold_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.threshold_var,
            bg='white',
            length=400
        )
        self.threshold_slider.pack(fill=tk.X, pady=5)
    
    def create_morphological_tab(self):
        """Create morphological operations tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔬 Morphological")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        self.create_tooltip_button(
            row1, "⊖ Erosion", '#e74c3c', 'white',
            self.apply_erosion, "Erode image (shrink bright regions)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "⊕ Dilation", '#27ae60', 'white',
            self.apply_dilation, "Dilate image (expand bright regions)", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Row 2
        row2 = tk.Frame(tab, bg='white')
        row2.pack(pady=10)
        
        self.create_tooltip_button(
            row2, "○ Opening", '#3498db', 'white',
            self.apply_opening, "Remove small objects/noise", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row2, "● Closing", '#9b59b6', 'white',
            self.apply_closing, "Fill small holes", btn_style
        ).pack(side=tk.LEFT, padx=5)
    
    def create_transform_tab(self):
        """Create transformation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔄 Transform")
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'height': 2}
        
        # Row 1 - Rotation
        row1 = tk.Frame(tab, bg='white')
        row1.pack(pady=10)
        
        tk.Label(row1, text="🔄 Rotation:", font=('Arial', 11, 'bold'), bg='white').pack(side=tk.LEFT, padx=10)
        
        self.create_tooltip_button(
            row1, "↻ 90° CW", '#3498db', 'white',
            lambda: self.apply_rotation(90), "Rotate 90 degrees clockwise", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "↻ 180°", '#3498db', 'white',
            lambda: self.apply_rotation(180), "Rotate 180 degrees", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row1, "↺ 270° CW", '#3498db', 'white',
            lambda: self.apply_rotation(270), "Rotate 270 degrees clockwise", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Row 2 - Flipping
        row2 = tk.Frame(tab, bg='white')
        row2.pack(pady=10)
        
        tk.Label(row2, text="↔️ Flip:", font=('Arial', 11, 'bold'), bg='white').pack(side=tk.LEFT, padx=10)
        
        self.create_tooltip_button(
            row2, "↔️ Horizontal", '#27ae60', 'white',
            lambda: self.apply_flip('horizontal'), "Flip image horizontally", btn_style
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_tooltip_button(
            row2, "↕️ Vertical", '#27ae60', 'white',
            lambda: self.apply_flip('vertical'), "Flip image vertically", btn_style
        ).pack(side=tk.LEFT, padx=5)
    
    def on_brightness_change(self, value):
        """Update brightness value label"""
        self.brightness_value_label.config(text=f"Value: {value}")
    
    def on_contrast_change(self, value):
        """Update contrast value label"""
        self.contrast_value_label.config(text=f"Value: {value}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def add_to_history(self, image):
        """Add current state to history for undo/redo"""
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(image.copy())
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
    
    def undo(self):
        """Undo last operation"""
        if not self.check_image_loaded():
            return
        
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.processed_image = self.current_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status("Undo: Reverted to previous state")
        else:
            messagebox.showinfo("Undo", "No more actions to undo")
    
    def redo(self):
        """Redo last undone operation"""
        if not self.check_image_loaded():
            return
        
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.processed_image = self.current_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status("Redo: Restored next state")
        else:
            messagebox.showinfo("Redo", "No more actions to redo")
    
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
                self.update_status("Loading image...")
                image = cv2.imread(file_path)
                
                if image is None:
                    messagebox.showerror("Error", "Failed to load image. Please select a valid image file.")
                    self.update_status("Error loading image")
                    return
                
                self.original_image = image.copy()
                self.current_image = image.copy()
                self.processed_image = image.copy()
                self.filename = os.path.basename(file_path)
                
                # Reset history
                self.history = [image.copy()]
                self.history_index = 0
                
                # Reset sliders
                self.brightness_var.set(0)
                self.contrast_var.set(1.0)
                
                # Display images
                self.display_image(self.original_image, self.original_image_label)
                self.display_image(self.processed_image, self.processed_image_label)
                
                self.update_status(f"✓ Image loaded: {self.filename}")
                messagebox.showinfo("Success", f"Image loaded successfully!\n{self.filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the image:\n{str(e)}")
                self.update_status("Error loading image")
    
    def display_image(self, image, label):
        """Display image in the GUI label with proper resizing"""
        if image is None:
            return
        
        try:
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
            label.config(image=photo, text="")
            label.image = photo
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def check_image_loaded(self):
        """Check if an image has been loaded"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            self.update_status("No image loaded")
            return False
        return True
    
    def process_and_display(self, operation_name, operation_func, *args):
        """Generic method to process image and display result"""
        if not self.check_image_loaded():
            return
        
        try:
            self.update_status(f"Applying {operation_name}...")
            self.processed_image = operation_func(self.current_image, *args)
            self.current_image = self.processed_image.copy()
            self.add_to_history(self.current_image)
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status(f"✓ {operation_name} applied successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply {operation_name}:\n{str(e)}")
            self.update_status(f"Error applying {operation_name}")
    
    # Operation methods
    def apply_grayscale(self):
        self.process_and_display("Grayscale", ip.convert_to_grayscale)
    
    def apply_brightness(self):
        brightness_value = self.brightness_var.get()
        self.process_and_display("Brightness", ip.adjust_brightness, brightness_value)
    
    def apply_contrast(self):
        contrast_value = self.contrast_var.get()
        self.process_and_display("Contrast", ip.adjust_contrast, contrast_value)
    
    def apply_gaussian_blur(self):
        self.process_and_display("Gaussian Blur", ip.apply_gaussian_blur)
    
    def apply_median_filter(self):
        self.process_and_display("Median Filter", ip.apply_median_filter)
    
    def apply_sharpening(self):
        self.process_and_display("Sharpening", ip.apply_sharpening)
    
    def apply_sobel_edge(self):
        self.process_and_display("Sobel Edge Detection", ip.apply_sobel_edge_detection)
    
    def apply_canny_edge(self):
        self.process_and_display("Canny Edge Detection", ip.apply_canny_edge_detection)
    
    def apply_laplacian_edge(self):
        self.process_and_display("Laplacian Edge Detection", ip.apply_laplacian_edge_detection)
    
    def apply_histogram_equalization(self):
        self.process_and_display("Histogram Equalization", ip.apply_histogram_equalization)
    
    def apply_binary_threshold(self):
        threshold_value = self.threshold_var.get()
        self.process_and_display("Binary Threshold", ip.apply_binary_threshold, threshold_value)
    
    def apply_adaptive_threshold(self):
        self.process_and_display("Adaptive Threshold", ip.apply_adaptive_threshold)
    
    def apply_erosion(self):
        self.process_and_display("Erosion", ip.apply_morphological_erosion)
    
    def apply_dilation(self):
        self.process_and_display("Dilation", ip.apply_morphological_dilation)
    
    def apply_opening(self):
        self.process_and_display("Opening", ip.apply_morphological_opening)
    
    def apply_closing(self):
        self.process_and_display("Closing", ip.apply_morphological_closing)
    
    def apply_invert(self):
        self.process_and_display("Invert", ip.invert_image)
    
    def apply_bilateral_filter(self):
        self.process_and_display("Bilateral Filter", ip.apply_bilateral_filter)
    
    def apply_rotation(self, angle):
        self.process_and_display(f"Rotation {angle}°", ip.rotate_image, angle)
    
    def apply_flip(self, direction):
        self.process_and_display(f"Flip {direction}", ip.flip_image, direction)
    
    def reset_image(self):
        """Reset to original image"""
        if not self.check_image_loaded():
            return
        
        try:
            self.current_image = self.original_image.copy()
            self.processed_image = self.original_image.copy()
            self.brightness_var.set(0)
            self.contrast_var.set(1.0)
            self.history = [self.original_image.copy()]
            self.history_index = 0
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status("✓ Image reset to original")
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
                self.update_status("Saving image...")
                cv2.imwrite(file_path, self.processed_image)
                self.update_status(f"✓ Image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Image saved successfully!\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
            self.update_status("Error saving image")
    
    def show_histogram_window(self):
        """Display histogram in new window"""
        if not self.check_image_loaded():
            return
        
        try:
            hist_window = tk.Toplevel(self.root)
            hist_window.title("Image Histogram")
            hist_window.geometry("800x600")
            
            fig = Figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            
            histograms = ip.get_image_histogram(self.processed_image)
            
            if 'gray' in histograms:
                ax.plot(histograms['gray'], color='black', label='Intensity')
                ax.set_title('Grayscale Histogram')
            else:
                colors = {'b': 'blue', 'g': 'green', 'r': 'red'}
                for key, color in colors.items():
                    if key in histograms:
                        ax.plot(histograms[key], color=color, label=color.upper(), alpha=0.7)
                ax.set_title('RGB Histogram')
            
            ax.set_xlabel('Pixel Intensity')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            canvas = FigureCanvasTkAgg(fig, master=hist_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.update_status("✓ Histogram displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display histogram:\n{str(e)}")
    
    def show_image_info(self):
        """Display image information"""
        if not self.check_image_loaded():
            return
        
        try:
            info = ip.get_image_info(self.processed_image, self.filename)
            
            info_text = f"""
IMAGE INFORMATION
{'='*50}

File Name: {info['filename']}
Width: {info['width']} pixels
Height: {info['height']} pixels
Channels: {info['channels']}
Image Type: {info['type']}
Data Type: {info['dtype']}
Total Pixels: {info['size']:,}

Resolution: {info['width']} x {info['height']}

History States: {len(self.history)}
Current Position: {self.history_index + 1}/{len(self.history)}
            """
            
            messagebox.showinfo("Image Information", info_text)
            self.update_status("✓ Image information displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get image information:\n{str(e)}")
    
    def show_help(self):
        """Show quick start guide"""
        help_text = """
QUICK START GUIDE
==================

1. UPLOAD IMAGE
   - Click "Upload Image" or press Ctrl+O
   - Select any JPG, PNG, BMP, or TIFF image

2. APPLY OPERATIONS
   - Use tabs to access different operations
   - Click any button to apply an operation
   - Use sliders for adjustable parameters

3. UNDO/REDO
   - Press Ctrl+Z to undo
   - Press Ctrl+Y to redo

4. SAVE RESULT
   - Click "Save Result" or press Ctrl+S
   - Choose location and format

5. TIPS
   - Hover over buttons for tooltips
   - View histogram for image analysis
   - Reset anytime with Ctrl+R

KEYBOARD SHORTCUTS
==================
Ctrl+O - Open Image
Ctrl+S - Save Result
Ctrl+R - Reset
Ctrl+Z - Undo
Ctrl+Y - Redo
        """
        messagebox.showinfo("Quick Start Guide", help_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
COMPUTER VISION IMAGE PROCESSING STUDIO
Enhanced Version
==========================================

A comprehensive desktop application for 
demonstrating Computer Vision and Image 
Processing concepts.

Features:
• 25+ Image Processing Operations
• Undo/Redo Functionality
• Histogram Visualization
• Keyboard Shortcuts
• Tooltips & User Guidance
• Professional Tabbed Interface

Developed for:
BTech Computer Science / AI-ML
Computer Vision Microproject

Version: 2.0 Enhanced
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main function to run the enhanced application"""
    root = tk.Tk()
    app = EnhancedImageProcessingStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
