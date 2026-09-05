"""
Computer Vision Image Enhancement & Edge Detection Studio
PERSONALIZED VERSION with Enhanced UI/UX

Student: Shreya Sanjay Singh Chauhan
PRN: 240105231010
Batch: A1 | Division: A | Year: TE | Branch: AIML
Academic Year: 2026-27

A beautiful, modern desktop application demonstrating Computer Vision concepts
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import image_processing as ip


class PersonalizedCVStudio:
    """Personalized Computer Vision Studio with Enhanced UI/UX"""
    
    # Team Information
    TEAM_MEMBERS = [
        {'name': 'Shreya Sanjay Singh Chauhan', 'prn': '240105231010'},
        {'name': 'Pranav Bansode', 'prn': '240105231033'},
        {'name': 'Yash Mali', 'prn': '240105231003'},
        {'name': 'Nidhi Sugandhi', 'prn': '240105231026'}
    ]
    BATCH = "A1"
    DIVISION = "A"
    YEAR = "TE"
    BRANCH = "AIML"
    ACADEMIC_YEAR = "2026-27"
    COLLEGE = "Your College Name"  # Update if needed
    
    # Modern Color Palette
    COLORS = {
        'primary': '#6C63FF',      # Purple
        'secondary': '#FF6584',    # Pink
        'success': '#00C9A7',      # Teal
        'warning': '#FFB800',      # Gold
        'danger': '#FF4757',       # Red
        'info': '#00D4FF',         # Cyan
        'dark': '#2D3436',         # Dark Gray
        'light': '#F8F9FA',        # Light Gray
        'white': '#FFFFFF',
        'gradient_start': '#667EEA',
        'gradient_end': '#764BA2',
        'panel_bg': '#F5F7FA',
        'text_dark': '#2C3E50',
        'text_light': '#95A5A6',
        'border': '#E1E8ED',
        'hover': '#5B54E8',
        'card_bg': '#FFFFFF'
    }
    
    def __init__(self, root):
        """Initialize the personalized application"""
        self.root = root
        self.root.title(f"CV Studio - Team Project")
        
        # Set window size and position
        window_width = 1600
        window_height = 950
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.configure(bg=self.COLORS['panel_bg'])
        self.root.minsize(1400, 800)
        
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
        self.display_width = 500
        self.display_height = 380
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to process images")
        
        # Create custom styles
        self.setup_styles()
        
        # Create GUI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Show welcome message
        self.root.after(500, self.show_welcome)
        
    def setup_styles(self):
        """Setup custom ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('TNotebook', 
            background=self.COLORS['panel_bg'],
            borderwidth=0
        )
        style.configure('TNotebook.Tab', 
            background=self.COLORS['light'],
            foreground=self.COLORS['text_dark'],
            padding=[20, 10],
            font=('Segoe UI', 10, 'bold')
        )
        style.map('TNotebook.Tab',
            background=[('selected', self.COLORS['primary'])],
            foreground=[('selected', self.COLORS['white'])],
            expand=[('selected', [1, 1, 1, 0])]
        )
    
    def create_gradient_frame(self, parent, height):
        """Create a frame with gradient background"""
        canvas = tk.Canvas(parent, height=height, bg=self.COLORS['gradient_start'], 
                          highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        # Create gradient effect (simplified)
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = int(self.COLORS['gradient_start'][1:3], 16), \
                        int(self.COLORS['gradient_start'][3:5], 16), \
                        int(self.COLORS['gradient_start'][5:7], 16)
            r2, g2, b2 = int(self.COLORS['gradient_end'][1:3], 16), \
                        int(self.COLORS['gradient_end'][3:5], 16), \
                        int(self.COLORS['gradient_end'][5:7], 16)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 2000, i, fill=color, width=1)
        
        return canvas
    
    def create_header(self):
        """Create modern header with student info"""
        # Gradient header
        header_canvas = self.create_gradient_frame(self.root, 140)
        
        # Main title
        title_label = tk.Label(
            header_canvas,
            text="🎨 COMPUTER VISION STUDIO",
            font=('Segoe UI', 28, 'bold'),
            bg=self.COLORS['gradient_start'],
            fg=self.COLORS['white']
        )
        title_label.place(relx=0.5, rely=0.25, anchor='center')
        
        # Subtitle
        subtitle = tk.Label(
            header_canvas,
            text="Image Enhancement & Edge Detection Platform",
            font=('Segoe UI', 12),
            bg=self.COLORS['gradient_start'],
            fg=self.COLORS['white']
        )
        subtitle.place(relx=0.5, rely=0.5, anchor='center')
        
        # Student Info Card - Left Side
        info_frame = tk.Frame(header_canvas, bg=self.COLORS['white'], 
                             relief=tk.FLAT, bd=0)
        info_frame.place(relx=0.02, rely=0.5, anchor='w')
        
        # Shadow effect (simplified for Tkinter)
        # info_frame will appear raised due to white background against gradient
        
        # Team header
        tk.Label(
            info_frame,
            text="👥 TEAM MEMBERS",
            font=('Segoe UI', 10, 'bold'),
            bg=self.COLORS['white'],
            fg=self.COLORS['text_dark'],
            anchor='w'
        ).pack(padx=15, pady=(10, 5), anchor='w')
        
        # Team members
        for member in self.TEAM_MEMBERS:
            tk.Label(
                info_frame,
                text=f"• {member['name']} ({member['prn']})",
                font=('Segoe UI', 8),
                bg=self.COLORS['white'],
                fg=self.COLORS['text_light'],
                anchor='w'
            ).pack(padx=15, pady=2, anchor='w')
        
        # Course info
        tk.Label(
            info_frame,
            text=f"📚 {self.YEAR} {self.BRANCH} | Batch {self.BATCH} | Div {self.DIVISION}",
            font=('Segoe UI', 9),
            bg=self.COLORS['white'],
            fg=self.COLORS['text_light'],
            anchor='w'
        ).pack(padx=15, pady=(5, 2), anchor='w')
        
        tk.Label(
            info_frame,
            text=f"📅 Academic Year: {self.ACADEMIC_YEAR}",
            font=('Segoe UI', 9),
            bg=self.COLORS['white'],
            fg=self.COLORS['text_light'],
            anchor='w'
        ).pack(padx=15, pady=(2, 10), anchor='w')
        
    def create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=self.COLORS['panel_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section - Image display
        self.create_image_section(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
        # Operations tabs
        self.create_operations_tabs(main_frame)
    
    def create_image_section(self, parent):
        """Create image display section with cards"""
        image_frame = tk.Frame(parent, bg=self.COLORS['panel_bg'])
        image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Original Image Card
        original_card = self.create_card(image_frame, "📷 Original Image")
        original_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.original_image_label = tk.Label(
            original_card,
            bg=self.COLORS['light'],
            text="Click 'Upload Image' to begin\n\nSupported formats:\nJPG, PNG, BMP, TIFF",
            font=('Segoe UI', 11),
            fg=self.COLORS['text_light']
        )
        self.original_image_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Processed Image Card
        processed_card = self.create_card(image_frame, "✨ Processed Image")
        processed_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.processed_image_label = tk.Label(
            processed_card,
            bg=self.COLORS['light'],
            text="Processed images appear here\n\nApply operations from tabs below\nto see real-time results",
            font=('Segoe UI', 11),
            fg=self.COLORS['text_light']
        )
        self.processed_image_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_card(self, parent, title):
        """Create a modern card container"""
        card = tk.Frame(parent, bg=self.COLORS['card_bg'], relief=tk.FLAT, bd=0)
        
        # Card header
        header = tk.Frame(card, bg=self.COLORS['card_bg'], height=45)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=title,
            font=('Segoe UI', 13, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text_dark']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Separator line
        separator = tk.Frame(card, bg=self.COLORS['border'], height=1)
        separator.pack(fill=tk.X)
        
        return card
    
    def create_modern_button(self, parent, text, command, color, icon=""):
        """Create a modern styled button"""
        btn_frame = tk.Frame(parent, bg=color, relief=tk.FLAT, bd=0)
        
        btn = tk.Button(
            btn_frame,
            text=f"{icon} {text}" if icon else text,
            command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg=self.COLORS['white'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            activebackground=self.COLORS['hover'],
            activeforeground=self.COLORS['white']
        )
        btn.pack(fill=tk.BOTH, expand=True)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.COLORS['hover'])
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn_frame
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        control_frame = tk.Frame(parent, bg=self.COLORS['panel_bg'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons = [
            ("📤 Upload Image", self.upload_image, self.COLORS['primary'], "Ctrl+O"),
            ("↶ Undo", self.undo, self.COLORS['text_light'], "Ctrl+Z"),
            ("↷ Redo", self.redo, self.COLORS['text_light'], "Ctrl+Y"),
            ("🔄 Reset", self.COLORS['warning'], self.reset_image, "Ctrl+R"),
            ("💾 Save Result", self.save_image, self.COLORS['success'], "Ctrl+S"),
            ("📊 Histogram", self.show_histogram_window, self.COLORS['info'], ""),
            ("ℹ️ Info", self.show_image_info, self.COLORS['dark'], "")
        ]
        
        for i, (text, cmd, color, shortcut) in enumerate(buttons):
            if i == 3:  # Reset button needs special handling
                btn = self.create_modern_button(control_frame, text, color, cmd)
            else:
                btn = self.create_modern_button(control_frame, text, cmd, color)
            btn.pack(side=tk.LEFT, padx=5)
            
            # Add tooltip
            if shortcut:
                self.create_tooltip(btn, f"{text}\nShortcut: {shortcut}")
    
    def create_operations_tabs(self, parent):
        """Create operations tabs with modern styling"""
        tabs_card = self.create_card(parent, "🎨 Image Processing Operations")
        tabs_card.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook
        self.notebook = ttk.Notebook(tabs_card)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create tabs
        self.create_basic_tab()
        self.create_filters_tab()
        self.create_edge_tab()
        self.create_threshold_tab()
        self.create_morphological_tab()
        self.create_transform_tab()
    
    def create_tab_button(self, parent, text, command, color, row, col, tooltip=""):
        """Create a modern tab button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg=self.COLORS['white'],
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=15,
            cursor='hand2',
            activebackground=self.COLORS['hover'],
            activeforeground=self.COLORS['white'],
            width=20
        )
        btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self.COLORS['hover'])
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        if tooltip:
            self.create_tooltip(btn, tooltip)
        
        return btn
    
    def create_basic_tab(self):
        """Create basic operations tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  🎨 Basic  ')
        
        # Grid layout
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid
        for i in range(3):
            content.columnconfigure(i, weight=1)
        
        # Buttons
        self.create_tab_button(content, "⚫ Grayscale", self.apply_grayscale, 
            self.COLORS['dark'], 0, 0, "Convert to black & white")
        self.create_tab_button(content, "🔆 Histogram Eq.", self.apply_histogram_equalization,
            '#FF6B6B', 0, 1, "Auto-enhance contrast")
        self.create_tab_button(content, "🔄 Invert", self.apply_invert,
            '#4ECDC4', 0, 2, "Create negative image")
        
        # Sliders section
        slider_frame = tk.Frame(content, bg=self.COLORS['white'])
        slider_frame.grid(row=1, column=0, columnspan=3, pady=20, sticky='ew')
        
        # Brightness
        bright_frame = tk.Frame(slider_frame, bg=self.COLORS['white'])
        bright_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        tk.Label(bright_frame, text="☀️ Brightness", font=('Segoe UI', 11, 'bold'),
                bg=self.COLORS['white'], fg=self.COLORS['text_dark']).pack(anchor='w')
        
        self.brightness_var = tk.IntVar(value=0)
        self.brightness_slider = tk.Scale(
            bright_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
            variable=self.brightness_var, bg=self.COLORS['white'],
            fg=self.COLORS['text_dark'], troughcolor=self.COLORS['light'],
            highlightthickness=0, length=300, command=self.on_brightness_change
        )
        self.brightness_slider.pack(fill=tk.X, pady=5)
        
        self.brightness_label = tk.Label(bright_frame, text="Value: 0",
            font=('Segoe UI', 9), bg=self.COLORS['white'], fg=self.COLORS['text_light'])
        self.brightness_label.pack()
        
        tk.Button(bright_frame, text="Apply", command=self.apply_brightness,
                 bg=self.COLORS['primary'], fg=self.COLORS['white'],
                 font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=20, pady=8,
                 cursor='hand2').pack(pady=10)
        
        # Contrast
        contrast_frame = tk.Frame(slider_frame, bg=self.COLORS['white'])
        contrast_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        tk.Label(contrast_frame, text="🔅 Contrast", font=('Segoe UI', 11, 'bold'),
                bg=self.COLORS['white'], fg=self.COLORS['text_dark']).pack(anchor='w')
        
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.contrast_slider = tk.Scale(
            contrast_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
            variable=self.contrast_var, bg=self.COLORS['white'],
            fg=self.COLORS['text_dark'], troughcolor=self.COLORS['light'],
            highlightthickness=0, length=300, command=self.on_contrast_change
        )
        self.contrast_slider.pack(fill=tk.X, pady=5)
        
        self.contrast_label = tk.Label(contrast_frame, text="Value: 1.0",
            font=('Segoe UI', 9), bg=self.COLORS['white'], fg=self.COLORS['text_light'])
        self.contrast_label.pack()
        
        tk.Button(contrast_frame, text="Apply", command=self.apply_contrast,
                 bg=self.COLORS['primary'], fg=self.COLORS['white'],
                 font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=20, pady=8,
                 cursor='hand2').pack(pady=10)
    
    def create_filters_tab(self):
        """Create filters tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  🔧 Filters  ')
        
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i in range(3):
            content.columnconfigure(i, weight=1)
        
        self.create_tab_button(content, "🌫️ Gaussian Blur", self.apply_gaussian_blur,
            '#3498DB', 0, 0, "Smooth and reduce noise")
        self.create_tab_button(content, "🔲 Median Filter", self.apply_median_filter,
            '#2ECC71', 0, 1, "Remove salt-and-pepper noise")
        self.create_tab_button(content, "✨ Sharpen", self.apply_sharpening,
            '#F39C12', 0, 2, "Enhance edges and details")
        self.create_tab_button(content, "🎭 Bilateral Filter", self.apply_bilateral_filter,
            '#9B59B6', 1, 0, "Edge-preserving smoothing")
    
    def create_edge_tab(self):
        """Create edge detection tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  📐 Edge Detection  ')
        
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i in range(3):
            content.columnconfigure(i, weight=1)
        
        self.create_tab_button(content, "📊 Sobel Edge", self.apply_sobel_edge,
            '#E74C3C', 0, 0, "Gradient-based detection")
        self.create_tab_button(content, "🎯 Canny Edge", self.apply_canny_edge,
            '#8E44AD', 0, 1, "Multi-stage detection")
        self.create_tab_button(content, "◆ Laplacian Edge", self.apply_laplacian_edge,
            '#D35400', 0, 2, "Second derivative detection")
    
    def create_threshold_tab(self):
        """Create thresholding tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  🎚️ Threshold  ')
        
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i in range(2):
            content.columnconfigure(i, weight=1)
        
        self.create_tab_button(content, "⬛⬜ Binary", self.apply_binary_threshold,
            '#2C3E50', 0, 0, "Simple binary conversion")
        self.create_tab_button(content, "🔄 Adaptive", self.apply_adaptive_threshold,
            '#7F8C8D', 0, 1, "Adaptive thresholding")
        
        # Threshold slider
        slider_frame = tk.Frame(content, bg=self.COLORS['white'])
        slider_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        tk.Label(slider_frame, text="🎚️ Threshold Value (for Binary)",
                font=('Segoe UI', 11, 'bold'), bg=self.COLORS['white'],
                fg=self.COLORS['text_dark']).pack()
        
        self.threshold_var = tk.IntVar(value=127)
        tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                variable=self.threshold_var, bg=self.COLORS['white'],
                fg=self.COLORS['text_dark'], troughcolor=self.COLORS['light'],
                highlightthickness=0, length=400).pack(pady=10)
    
    def create_morphological_tab(self):
        """Create morphological operations tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  🔬 Morphological  ')
        
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i in range(2):
            content.columnconfigure(i, weight=1)
        
        self.create_tab_button(content, "⊖ Erosion", self.apply_erosion,
            '#E74C3C', 0, 0, "Shrink bright regions")
        self.create_tab_button(content, "⊕ Dilation", self.apply_dilation,
            '#27AE60', 0, 1, "Expand bright regions")
        self.create_tab_button(content, "○ Opening", self.apply_opening,
            '#3498DB', 1, 0, "Remove small objects")
        self.create_tab_button(content, "● Closing", self.apply_closing,
            '#9B59B6', 1, 1, "Fill small holes")
    
    def create_transform_tab(self):
        """Create transformation tab"""
        tab = tk.Frame(self.notebook, bg=self.COLORS['white'])
        self.notebook.add(tab, text='  🔄 Transform  ')
        
        content = tk.Frame(tab, bg=self.COLORS['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i in range(3):
            content.columnconfigure(i, weight=1)
        
        tk.Label(content, text="🔄 Rotation", font=('Segoe UI', 12, 'bold'),
                bg=self.COLORS['white'], fg=self.COLORS['text_dark']).grid(
                row=0, column=0, columnspan=3, pady=(0, 10))
        
        self.create_tab_button(content, "↻ 90° CW", lambda: self.apply_rotation(90),
            '#3498DB', 1, 0, "Rotate 90° clockwise")
        self.create_tab_button(content, "↻ 180°", lambda: self.apply_rotation(180),
            '#3498DB', 1, 1, "Rotate 180°")
        self.create_tab_button(content, "↺ 270° CW", lambda: self.apply_rotation(270),
            '#3498DB', 1, 2, "Rotate 270° clockwise")
        
        tk.Label(content, text="↔️ Flip", font=('Segoe UI', 12, 'bold'),
                bg=self.COLORS['white'], fg=self.COLORS['text_dark']).grid(
                row=2, column=0, columnspan=3, pady=(20, 10))
        
        self.create_tab_button(content, "↔️ Horizontal", lambda: self.apply_flip('horizontal'),
            '#27AE60', 3, 0, "Flip horizontally")
        self.create_tab_button(content, "↕️ Vertical", lambda: self.apply_flip('vertical'),
            '#27AE60', 3, 1, "Flip vertically")
    
    def create_footer(self):
        """Create footer with status bar"""
        footer = tk.Frame(self.root, bg=self.COLORS['dark'], height=40)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        # Status label
        status_label = tk.Label(
            footer,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            bg=self.COLORS['dark'],
            fg=self.COLORS['white'],
            anchor='w'
        )
        status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Credits
        team_names = ", ".join([m['name'] for m in self.TEAM_MEMBERS])
        credit = tk.Label(
            footer,
            text=f"Developed by: {team_names} | {self.BRANCH} {self.YEAR}",
            font=('Segoe UI', 9),
            bg=self.COLORS['dark'],
            fg=self.COLORS['text_light'],
            anchor='e'
        )
        credit.pack(side=tk.RIGHT, padx=20)
    
    def create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip, text=text, background='#2C3E50',
                foreground='white', relief=tk.FLAT, borderwidth=0,
                font=('Segoe UI', 9), padx=10, pady=5
            )
            label.pack()
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.upload_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-r>', lambda e: self.reset_image())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
    
    def show_welcome(self):
        """Show welcome message"""
        team_list = "\n".join([f"• {m['name']} (PRN: {m['prn']})" for m in self.TEAM_MEMBERS])
        welcome_msg = f"""Welcome to Computer Vision Studio!

👥 TEAM MEMBERS:
{team_list}

📚 Course: {self.YEAR} {self.BRANCH}
🎓 Batch {self.BATCH} | Division {self.DIVISION}
📅 Academic Year: {self.ACADEMIC_YEAR}

Computer Vision Image Processing Studio is ready!

Click 'Upload Image' (Ctrl+O) to begin processing images.
"""
        messagebox.showinfo("Welcome to CV Studio", welcome_msg)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def on_brightness_change(self, value):
        """Update brightness label"""
        self.brightness_label.config(text=f"Value: {value}")
    
    def on_contrast_change(self, value):
        """Update contrast label"""
        self.contrast_label.config(text=f"Value: {value}")
    
    # History management
    def add_to_history(self, image):
        """Add to history"""
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(image.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
    
    def undo(self):
        """Undo operation"""
        if not self.check_image_loaded():
            return
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.processed_image = self.current_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status("✓ Undo successful")
        else:
            messagebox.showinfo("Undo", "No more actions to undo")
    
    def redo(self):
        """Redo operation"""
        if not self.check_image_loaded():
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.processed_image = self.current_image.copy()
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status("✓ Redo successful")
        else:
            messagebox.showinfo("Redo", "No more actions to redo")
    
    # File operations
    def upload_image(self):
        """Upload image"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.update_status("Loading image...")
                image = cv2.imread(file_path)
                
                if image is None:
                    messagebox.showerror("Error", "Failed to load image.")
                    self.update_status("Error loading image")
                    return
                
                self.original_image = image.copy()
                self.current_image = image.copy()
                self.processed_image = image.copy()
                self.filename = os.path.basename(file_path)
                
                self.history = [image.copy()]
                self.history_index = 0
                
                self.brightness_var.set(0)
                self.contrast_var.set(1.0)
                
                self.display_image(self.original_image, self.original_image_label)
                self.display_image(self.processed_image, self.processed_image_label)
                
                self.update_status(f"✓ Image loaded: {self.filename}")
                messagebox.showinfo("Success", f"Image loaded successfully!\n{self.filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image:\n{str(e)}")
                self.update_status("Error loading image")
    
    def display_image(self, image, label):
        """Display image"""
        if image is None:
            return
        
        try:
            if len(image.shape) == 3:
                display_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                display_img = image
            
            pil_image = Image.fromarray(display_img)
            pil_image.thumbnail((self.display_width, self.display_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(pil_image)
            label.config(image=photo, text="")
            label.image = photo
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def check_image_loaded(self):
        """Check if image loaded"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            self.update_status("No image loaded")
            return False
        return True
    
    def process_and_display(self, operation_name, operation_func, *args):
        """Process and display"""
        if not self.check_image_loaded():
            return
        
        try:
            self.update_status(f"Applying {operation_name}...")
            self.processed_image = operation_func(self.current_image, *args)
            self.current_image = self.processed_image.copy()
            self.add_to_history(self.current_image)
            self.display_image(self.processed_image, self.processed_image_label)
            self.update_status(f"✓ {operation_name} applied")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply {operation_name}:\n{str(e)}")
            self.update_status(f"Error: {operation_name}")
    
    # Operations
    def apply_grayscale(self):
        self.process_and_display("Grayscale", ip.convert_to_grayscale)
    
    def apply_brightness(self):
        self.process_and_display("Brightness", ip.adjust_brightness, self.brightness_var.get())
    
    def apply_contrast(self):
        self.process_and_display("Contrast", ip.adjust_contrast, self.contrast_var.get())
    
    def apply_gaussian_blur(self):
        self.process_and_display("Gaussian Blur", ip.apply_gaussian_blur)
    
    def apply_median_filter(self):
        self.process_and_display("Median Filter", ip.apply_median_filter)
    
    def apply_sharpening(self):
        self.process_and_display("Sharpening", ip.apply_sharpening)
    
    def apply_sobel_edge(self):
        self.process_and_display("Sobel Edge", ip.apply_sobel_edge_detection)
    
    def apply_canny_edge(self):
        self.process_and_display("Canny Edge", ip.apply_canny_edge_detection)
    
    def apply_laplacian_edge(self):
        self.process_and_display("Laplacian Edge", ip.apply_laplacian_edge_detection)
    
    def apply_histogram_equalization(self):
        self.process_and_display("Histogram Equalization", ip.apply_histogram_equalization)
    
    def apply_binary_threshold(self):
        self.process_and_display("Binary Threshold", ip.apply_binary_threshold, self.threshold_var.get())
    
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
        """Reset to original"""
        if not self.check_image_loaded():
            return
        
        self.current_image = self.original_image.copy()
        self.processed_image = self.original_image.copy()
        self.brightness_var.set(0)
        self.contrast_var.set(1.0)
        self.history = [self.original_image.copy()]
        self.history_index = 0
        self.display_image(self.processed_image, self.processed_image_label)
        self.update_status("✓ Image reset to original")
    
    def save_image(self):
        """Save image"""
        if not self.check_image_loaded():
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Processed Image",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
            )
            
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                self.update_status(f"✓ Image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{str(e)}")
    
    def show_histogram_window(self):
        """Show histogram"""
        if not self.check_image_loaded():
            return
        
        try:
            hist_window = tk.Toplevel(self.root)
            hist_window.title("Image Histogram")
            hist_window.geometry("900x700")
            hist_window.configure(bg=self.COLORS['white'])
            
            # Header
            header = tk.Frame(hist_window, bg=self.COLORS['primary'], height=60)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            tk.Label(header, text="📊 Image Histogram Analysis",
                    font=('Segoe UI', 16, 'bold'), bg=self.COLORS['primary'],
                    fg=self.COLORS['white']).pack(pady=15)
            
            fig = Figure(figsize=(9, 6), facecolor='white')
            ax = fig.add_subplot(111)
            
            histograms = ip.get_image_histogram(self.processed_image)
            
            if 'gray' in histograms:
                ax.plot(histograms['gray'], color='black', linewidth=2, label='Intensity')
                ax.fill_between(range(256), histograms['gray'], alpha=0.3, color='gray')
                ax.set_title('Grayscale Histogram', fontsize=14, fontweight='bold')
            else:
                colors = {'b': 'blue', 'g': 'green', 'r': 'red'}
                for key, color in colors.items():
                    if key in histograms:
                        ax.plot(histograms[key], color=color, linewidth=2,
                               label=color.upper(), alpha=0.8)
                        ax.fill_between(range(256), histograms[key], alpha=0.2, color=color)
                ax.set_title('RGB Histogram', fontsize=14, fontweight='bold')
            
            ax.set_xlabel('Pixel Intensity', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_xlim([0, 255])
            
            canvas = FigureCanvasTkAgg(fig, master=hist_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            self.update_status("✓ Histogram displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show histogram:\n{str(e)}")
    
    def show_image_info(self):
        """Show image info"""
        if not self.check_image_loaded():
            return
        
        try:
            info = ip.get_image_info(self.processed_image, self.filename)
            
            team_list = "\n".join([f"{m['name']} (PRN: {m['prn']})" for m in self.TEAM_MEMBERS])
            
            info_text = f"""
╔══════════════════════════════════════════╗
           IMAGE INFORMATION
╚══════════════════════════════════════════╝

📁 File Name: {info['filename']}
📏 Dimensions: {info['width']} × {info['height']} pixels
🎨 Channels: {info['channels']}
🖼️ Type: {info['type']}
💾 Data Type: {info['dtype']}
📊 Total Pixels: {info['size']:,}

📈 History: {len(self.history)} states saved
📍 Current Position: {self.history_index + 1}/{len(self.history)}

╔══════════════════════════════════════════╗
               TEAM MEMBERS
╚══════════════════════════════════════════╝

{team_list}

📚 Course: {self.YEAR} {self.BRANCH}
🎓 Batch {self.BATCH} | Division {self.DIVISION}
📅 Academic Year: {self.ACADEMIC_YEAR}
            """
            
            messagebox.showinfo("Image Information", info_text)
            self.update_status("✓ Image information displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get info:\n{str(e)}")


def main():
    """Main function"""
    root = tk.Tk()
    app = PersonalizedCVStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
