# Computer Vision Image Enhancement & Edge Detection Studio

A beginner-friendly desktop application demonstrating fundamental Computer Vision and Image Processing concepts. This project is designed for BTech Computer Science / AI-ML students to understand and implement core CV operations.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Project Objectives](#project-objectives)
- [Features](#features)
- [Computer Vision Concepts](#computer-vision-concepts)
- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Academic Relevance](#academic-relevance)
- [Future Scope](#future-scope)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)

---

## 🎯 Introduction

**Computer Vision** is a field of artificial intelligence that enables computers to interpret and understand visual information from the world. This project provides a hands-on implementation of fundamental Computer Vision techniques through an interactive desktop application.

The **Computer Vision Image Enhancement & Edge Detection Studio** allows users to upload images and apply various image processing operations, including enhancement filters and edge detection algorithms. This project demonstrates concepts primarily from **Unit II** of a typical Computer Vision syllabus.

---

## 🎓 Project Objectives

The main objectives of this microproject are:

1. **Understand Digital Image Representation** - Learn how images are represented as matrices of pixel values
2. **Implement Point Processing Operations** - Apply brightness and contrast adjustments
3. **Explore Spatial Filtering** - Implement blur, noise reduction, and sharpening filters
4. **Demonstrate Edge Detection** - Apply Sobel and Canny edge detection algorithms
5. **Build a Functional GUI** - Create an interactive desktop application using Tkinter
6. **Practice OpenCV** - Gain hands-on experience with the OpenCV library

---

## ✨ Features

### Image Operations

- **📤 Upload Image** - Load images from your computer (supports JPG, JPEG, PNG, BMP, TIFF)
- **🔄 Reset** - Restore the image to its original state
- **💾 Save Result** - Download the processed image
- **ℹ️ Image Information** - View image metadata (dimensions, channels, format)

### Image Processing Operations

#### Basic Transformations
- **Grayscale Conversion** - Convert color images to grayscale

#### Point Processing
- **Brightness Adjustment** - Increase or decrease image brightness (-100 to +100)
- **Contrast Adjustment** - Modify image contrast (0.5 to 2.0)

#### Spatial Filtering
- **Gaussian Blur** - Smooth images and reduce noise using Gaussian filter
- **Median Filter** - Remove salt-and-pepper noise while preserving edges
- **Sharpening** - Enhance edges and fine details

#### Edge Detection
- **Sobel Edge Detection** - Detect edges using gradient-based method
- **Canny Edge Detection** - Advanced multi-stage edge detection algorithm

---

## 📚 Computer Vision Concepts

This project demonstrates the following key Computer Vision concepts:

### 1. Digital Image Representation

**What is it?**
- Digital images are represented as 2D or 3D arrays (matrices) of pixel values
- Each pixel stores intensity information
- Color images use 3 channels (Red, Green, Blue)
- Grayscale images use 1 channel (intensity values from 0-255)

**Implementation in Project:**
- Image loading and display
- RGB/BGR color space handling
- Grayscale conversion
- Multi-channel image processing

**Key Concepts:**
- **Pixels**: The smallest unit of a digital image
- **Resolution**: Width × Height (number of pixels)
- **Channels**: Color components (BGR for OpenCV)
- **Bit Depth**: Number of bits per pixel (8-bit = 0-255 range)

---

### 2. Point Processing Operations

**What is it?**
Point processing operations modify individual pixel values independently, without considering neighboring pixels.

**Implementation in Project:**

#### Brightness Adjustment
- **Formula**: `new_pixel = old_pixel + brightness_value`
- **Range**: -100 (darker) to +100 (brighter)
- **Effect**: Shifts all pixel values uniformly
- **Use Case**: Correct under-exposed or over-exposed images

#### Contrast Adjustment
- **Formula**: `new_pixel = old_pixel × contrast_multiplier`
- **Range**: 0.5 (low contrast) to 2.0 (high contrast)
- **Effect**: Expands or compresses the range of pixel intensities
- **Use Case**: Make images more vivid or subdued

**Key Concepts:**
- Pixel value transformation
- Histogram modification
- Value clipping (ensuring 0-255 range)
- Linear transformations

---

### 3. Spatial Filtering

**What is it?**
Spatial filtering involves modifying pixel values based on their neighboring pixels using convolution with a kernel (filter matrix).

**Implementation in Project:**

#### Gaussian Blur
- **Kernel**: 5×5 Gaussian kernel
- **Effect**: Smooths images by averaging pixels with a weighted Gaussian distribution
- **Use Case**: Noise reduction, preprocessing for edge detection
- **Mathematical Basis**: Gaussian function weights closer pixels more heavily

#### Median Filter
- **Kernel**: 5×5 window
- **Effect**: Replaces each pixel with the median value of surrounding pixels
- **Use Case**: Removes salt-and-pepper noise while preserving edges better than Gaussian blur
- **Advantage**: Non-linear filter, excellent for impulse noise

#### Sharpening
- **Kernel**: 
  ```
  [ 0 -1  0]
  [-1  5 -1]
  [ 0 -1  0]
  ```
- **Effect**: Enhances edges and fine details by amplifying high-frequency components
- **Use Case**: Make blurry images appear sharper
- **Mathematical Basis**: Subtracts blurred version from original (unsharp masking)

**Key Concepts:**
- Convolution operation
- Kernel/Filter design
- Frequency domain (low-pass vs high-pass filters)
- Spatial domain processing

---

### 4. Edge Detection

**What is it?**
Edge detection identifies boundaries between regions with different intensities, representing object boundaries, shadows, or texture changes.

**Implementation in Project:**

#### Sobel Edge Detection
- **Method**: Gradient-based edge detection
- **Process**:
  1. Compute X-direction gradient (vertical edges)
  2. Compute Y-direction gradient (horizontal edges)
  3. Combine: `magnitude = √(Gx² + Gy²)`
- **Kernels**:
  ```
  Sobel X:        Sobel Y:
  [-1  0  1]      [-1 -2 -1]
  [-2  0  2]      [ 0  0  0]
  [-1  0  1]      [ 1  2  1]
  ```
- **Use Case**: Basic edge detection, gradient computation

#### Canny Edge Detection
- **Method**: Multi-stage optimal edge detector
- **Process**:
  1. **Noise Reduction**: Apply Gaussian blur
  2. **Gradient Calculation**: Compute intensity gradients
  3. **Non-Maximum Suppression**: Thin edges to 1-pixel width
  4. **Double Threshold**: Classify edges as strong, weak, or non-edges
  5. **Edge Tracking by Hysteresis**: Connect weak edges to strong edges
- **Parameters**:
  - Lower threshold: 100
  - Upper threshold: 200
- **Advantage**: Produces clean, continuous edges with less noise
- **Use Case**: High-quality edge detection for object recognition and segmentation

**Key Concepts:**
- Image gradients
- Edge strength and direction
- Hysteresis thresholding
- Non-maximum suppression
- First and second derivatives

---

### 5. Image Enhancement

**What is it?**
Image enhancement improves the visual quality of images by adjusting intensity, contrast, sharpness, and reducing noise.

**Implementation in Project:**
- Brightness and contrast for intensity correction
- Sharpening for detail enhancement
- Blur filters for noise reduction
- Combined operations for comprehensive enhancement

**Use Cases:**
- Medical imaging
- Satellite image analysis
- Photography enhancement
- Preprocessing for machine learning

---

## 🛠️ Technologies Used

### Python 3
- **Version**: 3.8 or higher
- **Role**: Primary programming language
- **Why**: Easy to learn, extensive libraries, great for rapid prototyping

### OpenCV (cv2)
- **Version**: 4.8.1
- **Full Name**: Open Source Computer Vision Library
- **Role**: Core image processing operations
- **Features Used**:
  - Image I/O (reading and writing)
  - Color space conversions (BGR ↔ RGB ↔ Grayscale)
  - Filtering operations (Gaussian, Median, Convolution)
  - Edge detection algorithms (Sobel, Canny)
  - Image transformations
- **Why**: Industry-standard CV library with optimized algorithms

### NumPy
- **Version**: 1.24.3
- **Role**: Numerical operations on image arrays
- **Features Used**:
  - Array operations for pixel manipulation
  - Mathematical operations (addition, multiplication)
  - Value clipping and type conversion
- **Why**: Efficient array operations, foundation for OpenCV

### Pillow (PIL Fork)
- **Version**: 10.0.0
- **Role**: Image display in Tkinter GUI
- **Features Used**:
  - Convert NumPy arrays to displayable images
  - Image resizing for GUI display
  - PhotoImage creation for Tkinter
- **Why**: Seamless integration between OpenCV and Tkinter

### Tkinter
- **Version**: Built-in with Python
- **Role**: Graphical User Interface
- **Features Used**:
  - Windows and frames
  - Buttons and labels
  - Sliders (Scale widgets)
  - File dialogs
  - Message boxes
- **Why**: Standard Python GUI library, no extra installation needed

---

## 💻 System Requirements

### Hardware Requirements
- **Processor**: Any modern processor (Intel i3 or equivalent)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Display**: 1366×768 or higher resolution

### Software Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.8 or higher
- **pip**: Python package manager (usually comes with Python)

### No Special Requirements
- ✅ Works offline (after package installation)
- ✅ No GPU required
- ✅ No camera or sensors needed
- ✅ No Arduino or Raspberry Pi required
- ✅ No paid APIs or cloud services
- ✅ No external hardware

---

## 📥 Installation

Follow these steps to set up the project on your computer:

### Step 1: Install Python

If you don't have Python installed:

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Download the Project

Clone or download this repository to your computer.

### Step 3: Navigate to Project Directory

Open a terminal/command prompt and navigate to the project folder:

```bash
cd path/to/cv
```

### Step 4: Create Virtual Environment (Recommended)

Creating a virtual environment keeps project dependencies isolated:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### Step 5: Install Dependencies

Install required packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- opencv-python (4.8.1.78)
- numpy (1.24.3)
- Pillow (10.0.0)

### Step 6: Verify Installation

Check if packages are installed correctly:

```bash
pip list
```

You should see opencv-python, numpy, and Pillow in the list.

---

## 🚀 How to Run

### Starting the Application

1. Make sure your virtual environment is activated (if you created one)
2. Navigate to the project directory
3. Run the main application:

```bash
python main.py
```

### What to Expect

- A GUI window titled **"Computer Vision Image Enhancement & Edge Detection Studio"** will open
- The window displays two image panels: Original Image (left) and Processed Image (right)
- Control buttons and operation buttons are available below the image panels

### Stopping the Application

- Click the **X** button on the window
- Or press `Ctrl+C` in the terminal (if running from terminal)

---

## 📖 How to Use

Follow this step-by-step guide to use the application:

### 1. Upload an Image

1. Click the **"Upload Image"** button
2. Select an image file from your computer (JPG, PNG, BMP, or TIFF)
3. The image will appear in both panels
4. You'll see a success message with the filename

### 2. Apply Processing Operations

#### Grayscale Conversion
- Click **"Grayscale"** to convert the image to black and white
- Useful for: Simplifying images, reducing processing complexity

#### Brightness Adjustment
1. Move the **Brightness** slider (-100 to +100)
2. Click **"Apply Brightness"**
3. Negative values darken, positive values brighten

#### Contrast Adjustment
1. Move the **Contrast** slider (0.5 to 2.0)
2. Click **"Apply Contrast"**
3. Values < 1.0 reduce contrast, values > 1.0 increase contrast

#### Gaussian Blur
- Click **"Gaussian Blur"** to smooth the image
- Reduces noise and fine details
- Creates a soft, blurred effect

#### Median Filter
- Click **"Median Filter"** to remove salt-and-pepper noise
- Better at preserving edges than Gaussian blur
- Good for noisy images

#### Sharpening
- Click **"Sharpen"** to enhance edges and details
- Makes the image appear crisper
- Enhances high-frequency components

#### Sobel Edge Detection
- Click **"Sobel Edge"** to detect edges using gradients
- Shows edges as white lines on black background
- Detects both horizontal and vertical edges

#### Canny Edge Detection
- Click **"Canny Edge"** for advanced edge detection
- Produces cleaner, thinner edges than Sobel
- Best for precise edge detection

### 3. View Image Information

- Click **"Image Info"** to see:
  - Filename
  - Width and height (pixels)
  - Number of channels (1 for grayscale, 3 for color)
  - Image type (Color BGR or Grayscale)
  - Data type and total pixels

### 4. Reset the Image

- Click **"Reset"** to restore the original image
- All sliders return to default values
- Processed image becomes the original again

### 5. Save the Result

1. Click **"Save Result"**
2. Choose a location and filename
3. Select format (PNG or JPEG)
4. Click Save
5. You'll see a success confirmation

---

## 📁 Project Structure

```
cv/
│
├── main.py                     # Main GUI application (Tkinter)
├── image_processing.py         # Image processing functions (OpenCV)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── assets/                     # (Optional) Sample images folder
    └── sample_images.txt       # Instructions for sample images
```

### File Descriptions

#### `main.py`
- **Purpose**: Main application entry point
- **Contents**:
  - `ImageProcessingStudio` class: Main GUI application
  - Widget creation and layout
  - Event handlers for buttons and sliders
  - Image upload, display, and save functionality
  - Error handling and user messages
- **Key Functions**:
  - `upload_image()`: Load images from file system
  - `display_image()`: Show images in GUI with proper resizing
  - `apply_*()`: Wrapper functions for each processing operation
  - `reset_image()`: Restore original image
  - `save_image()`: Export processed image

#### `image_processing.py`
- **Purpose**: Core image processing algorithms
- **Contents**:
  - All Computer Vision operations
  - Pure OpenCV and NumPy implementations
  - Well-documented functions with docstrings
- **Key Functions**:
  - `convert_to_grayscale()`: BGR to grayscale conversion
  - `adjust_brightness()`: Point processing for brightness
  - `adjust_contrast()`: Point processing for contrast
  - `apply_gaussian_blur()`: Spatial filtering with Gaussian kernel
  - `apply_median_filter()`: Non-linear spatial filtering
  - `apply_sharpening()`: Edge enhancement with convolution
  - `apply_sobel_edge_detection()`: Gradient-based edge detection
  - `apply_canny_edge_detection()`: Multi-stage edge detection
  - `get_image_info()`: Extract image metadata

#### `requirements.txt`
- **Purpose**: List of Python dependencies
- **Contents**: Package names with version numbers
- **Usage**: `pip install -r requirements.txt`

---

## 🎓 Academic Relevance

This project covers the following topics from a typical Computer Vision syllabus:

| **Concept** | **Syllabus Unit** | **Implementation** |
|-------------|-------------------|-------------------|
| Digital Image Representation | Unit I/II | Image loading, channels, grayscale |
| Point Processing | Unit II | Brightness, contrast adjustment |
| Spatial Filtering | Unit II | Gaussian blur, median filter, sharpening |
| Edge Detection | Unit II | Sobel, Canny algorithms |
| Image Enhancement | Unit II | Combined filters and adjustments |
| Image I/O | Unit I | Upload and save functionality |

### Suitable For

- **BTech Computer Science** - Computer Vision course
- **BTech AI-ML** - Image Processing course
- **MCA** - Digital Image Processing
- **MSc Computer Science** - Computer Vision
- **Diploma Projects** - Image Processing

### Learning Outcomes

After completing this project, students will be able to:

1. ✅ Explain how digital images are represented in computer memory
2. ✅ Implement point processing operations (brightness, contrast)
3. ✅ Apply spatial filtering techniques (blur, median, sharpen)
4. ✅ Implement and compare edge detection algorithms
5. ✅ Use OpenCV library for image processing
6. ✅ Build GUI applications with Tkinter
7. ✅ Handle image files and formats
8. ✅ Explain the mathematical foundations of CV operations

### Viva Questions & Answers

**Q1: What is the difference between BGR and RGB?**
- OpenCV uses BGR (Blue-Green-Red) order by default, while most other libraries use RGB (Red-Green-Blue). We convert BGR to RGB for display in Tkinter.

**Q2: How does Gaussian blur reduce noise?**
- Gaussian blur uses weighted averaging based on a Gaussian distribution. Pixels closer to the center have more weight, creating smooth transitions and reducing random noise.

**Q3: Why is median filter better for salt-and-pepper noise?**
- Median filter replaces each pixel with the median value of neighbors. Unlike averaging, median is resistant to outliers, making it effective against impulse noise without blurring edges.

**Q4: What is the difference between Sobel and Canny edge detection?**
- Sobel: Gradient-based, simple, gives edge magnitude. Canny: Multi-stage, includes noise reduction, non-maximum suppression, and hysteresis thresholding, producing thinner and cleaner edges.

**Q5: What is a convolution kernel?**
- A convolution kernel is a small matrix used to apply filtering operations. It slides over the image, multiplying overlapping pixel values and summing them to produce a new pixel value.

**Q6: How does image sharpening work?**
- Sharpening enhances high-frequency components (edges, details) by applying a kernel that amplifies differences between pixels, making edges more pronounced.

---

## 🚀 Future Scope

This project can be extended with the following features:

### Image Analysis
- **Histogram Visualization** - Display RGB and grayscale histograms
- **Histogram Equalization** - Automatic contrast enhancement
- **Color Channel Separation** - Split and display R, G, B channels separately
- **Image Statistics** - Mean, median, standard deviation of pixel values

### Advanced Filters
- **Bilateral Filter** - Edge-preserving smoothing
- **Morphological Operations** - Erosion, dilation, opening, closing
- **Unsharp Masking** - Advanced sharpening technique
- **Custom Kernel Editor** - Allow users to define custom convolution kernels

### Edge Detection Enhancements
- **Adjustable Thresholds** - Sliders for Canny threshold parameters
- **Laplacian Edge Detection** - Second-derivative edge detection
- **Prewitt Operator** - Alternative gradient-based edge detection
- **Edge Linking** - Connect broken edges

### Feature Detection
- **Harris Corner Detection** - Identify corners and interest points
- **SIFT (Scale-Invariant Feature Transform)** - Detect and describe local features
- **ORB (Oriented FAST and Rotated BRIEF)** - Fast feature detection
- **HOG (Histogram of Oriented Gradients)** - Useful for object detection

### Real-Time Processing
- **Webcam Integration** - Apply filters to live camera feed
- **Video Processing** - Process video files frame by frame
- **Batch Processing** - Process multiple images at once

### Object Detection & Segmentation
- **Contour Detection** - Find and draw object boundaries
- **Thresholding** - Binary, adaptive, Otsu's thresholding
- **Watershed Segmentation** - Separate overlapping objects
- **Color-based Segmentation** - Segment regions by color

### Machine Learning Integration
- **Face Detection** - Using Haar Cascades or DNN
- **Object Recognition** - Pre-trained models (YOLO, SSD)
- **Image Classification** - Using CNN models
- **Style Transfer** - Artistic image transformation

### User Experience
- **Before/After Comparison** - Side-by-side comparison slider
- **Undo/Redo Functionality** - Step back through operations
- **Processing History** - List of applied operations
- **Preset Filters** - One-click enhancement presets
- **Drag-and-Drop Upload** - Easier image loading

### Performance
- **GPU Acceleration** - Use CUDA for faster processing
- **Multi-threading** - Parallel processing for multiple operations
- **Progress Bars** - Show processing status for slow operations

### Export & Sharing
- **Multiple Format Support** - TIFF, WebP, GIF support
- **Quality Settings** - Adjustable compression for JPEG
- **Batch Export** - Save multiple versions at once
- **PDF Report Generation** - Document processing steps

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "python: command not found"
**Solution**: Python is not installed or not in PATH
- Download Python from python.org
- During installation, check "Add Python to PATH"
- Restart terminal after installation

#### Issue 2: "No module named 'cv2'"
**Solution**: OpenCV is not installed
```bash
pip install opencv-python
```

#### Issue 3: "No module named 'PIL'"
**Solution**: Pillow is not installed
```bash
pip install Pillow
```

#### Issue 4: "No module named 'tkinter'"
**Solution**: Tkinter is not available

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**On macOS:**
```bash
brew install python-tk
```

**On Windows:**
- Tkinter should come with Python
- Try reinstalling Python with "tcl/tk" option checked

#### Issue 5: Image not displaying correctly
**Solution**: 
- Check image file is not corrupted
- Try a different image format
- Ensure image file size is reasonable (<20MB)

#### Issue 6: Application crashes when clicking buttons
**Solution**:
- Make sure you uploaded an image first
- Check terminal for error messages
- Restart the application

#### Issue 7: "ImportError: DLL load failed" (Windows)
**Solution**: Install Microsoft Visual C++ Redistributable
- Download from Microsoft website
- Install and restart computer

#### Issue 8: Sliders not working
**Solution**:
- Upload an image first
- After moving slider, click the corresponding "Apply" button
- Check that values are within valid range

---

## 👥 Contributors

**Project Type**: BTech Computer Science / AI-ML Microproject

**Course**: Computer Vision / Image Processing

**Semester**: [Your Semester]

**Academic Year**: [Your Year]

**Submitted By**:
- [Your Name]
- [Roll Number]
- [Department]

**Submitted To**:
- [Professor Name]
- [Department]
- [College Name]

---

## 📄 License

This project is created for educational purposes as part of a BTech Computer Vision microproject.

Feel free to use, modify, and distribute this code for learning and academic purposes.

---

## 📞 Contact

For questions, suggestions, or issues related to this project:

- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile]
- **LinkedIn**: [Your LinkedIn Profile]

---

## 🙏 Acknowledgments

- **OpenCV Community** - For the powerful computer vision library
- **Python Software Foundation** - For the Python programming language
- **NumPy Developers** - For efficient numerical computing
- **Course Instructor** - For guidance and support
- **College/University** - For providing the platform to learn

---

## 📚 References

1. **OpenCV Documentation** - https://docs.opencv.org/
2. **Digital Image Processing** - Rafael C. Gonzalez & Richard E. Woods
3. **Computer Vision: Algorithms and Applications** - Richard Szeliski
4. **Python Image Processing** - NumPy & OpenCV Official Tutorials
5. **Tkinter Documentation** - https://docs.python.org/3/library/tkinter.html

---

## ⭐ Key Takeaways

This project demonstrates:

✅ **Practical Computer Vision** - Real-world implementation of CV algorithms  
✅ **Clean Code** - Well-structured, documented, and maintainable  
✅ **User-Friendly** - Intuitive GUI with error handling  
✅ **Educational** - Perfect for learning and demonstrating CV concepts  
✅ **Offline-Ready** - No internet or external hardware required  
✅ **Extensible** - Easy to add new features and operations  

---

**Happy Learning! 🚀📸**

*This project is a stepping stone into the exciting world of Computer Vision and Image Processing. Keep exploring, keep coding!*
