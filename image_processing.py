"""
Image Processing Module for Computer Vision Studio
Contains all image processing and enhancement operations
"""

import cv2
import numpy as np


def convert_to_grayscale(image):
    """
    Convert RGB/BGR image to grayscale
    
    Args:
        image: Input BGR image (OpenCV format)
    
    Returns:
        Grayscale image
    """
    if len(image.shape) == 2:
        # Already grayscale
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def adjust_brightness(image, value):
    """
    Adjust image brightness using point processing
    
    Args:
        image: Input image
        value: Brightness adjustment value (-100 to +100)
    
    Returns:
        Brightness-adjusted image
    """
    # Convert to float to prevent overflow
    img_float = image.astype(np.float32)
    
    # Add brightness value
    img_float = img_float + value
    
    # Clip values to valid range [0, 255]
    img_float = np.clip(img_float, 0, 255)
    
    # Convert back to uint8
    return img_float.astype(np.uint8)


def adjust_contrast(image, value):
    """
    Adjust image contrast using point processing
    
    Args:
        image: Input image
        value: Contrast multiplier (0.5 to 2.0, where 1.0 = no change)
    
    Returns:
        Contrast-adjusted image
    """
    # Convert to float
    img_float = image.astype(np.float32)
    
    # Apply contrast formula: new_pixel = pixel * contrast
    img_float = img_float * value
    
    # Clip values to valid range
    img_float = np.clip(img_float, 0, 255)
    
    # Convert back to uint8
    return img_float.astype(np.uint8)


def apply_gaussian_blur(image, kernel_size=5):
    """
    Apply Gaussian blur filter for noise reduction
    This is a spatial filtering operation using a Gaussian kernel
    
    Args:
        image: Input image
        kernel_size: Size of Gaussian kernel (must be odd)
    
    Returns:
        Blurred image
    """
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def apply_median_filter(image, kernel_size=5):
    """
    Apply median filter for salt-and-pepper noise reduction
    Median filter preserves edges better than Gaussian blur
    
    Args:
        image: Input image
        kernel_size: Size of median kernel (must be odd)
    
    Returns:
        Filtered image
    """
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.medianBlur(image, kernel_size)


def apply_sharpening(image):
    """
    Apply sharpening filter to enhance edges and details
    Uses a sharpening kernel to enhance high-frequency components
    
    Sharpening kernel:
    [ 0 -1  0]
    [-1  5 -1]
    [ 0 -1  0]
    
    Args:
        image: Input image
    
    Returns:
        Sharpened image
    """
    # Define sharpening kernel
    # Center value = 5, surrounding values = -1
    # This enhances edges and fine details
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    
    # Apply the kernel using filter2D
    sharpened = cv2.filter2D(image, -1, kernel)
    
    return sharpened


def apply_sobel_edge_detection(image):
    """
    Apply Sobel edge detection
    Sobel operator computes gradients in X and Y directions
    
    Args:
        image: Input image
    
    Returns:
        Edge-detected image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Compute X and Y gradients
    # Sobel X detects vertical edges
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    
    # Sobel Y detects horizontal edges
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Compute magnitude of gradients
    # magnitude = sqrt(Gx^2 + Gy^2)
    sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
    
    # Normalize to 0-255 range
    sobel_combined = np.clip(sobel_combined, 0, 255)
    sobel_combined = sobel_combined.astype(np.uint8)
    
    return sobel_combined


def apply_canny_edge_detection(image, threshold1=100, threshold2=200):
    """
    Apply Canny edge detection
    Canny is a multi-stage edge detection algorithm:
    1. Noise reduction with Gaussian filter
    2. Gradient calculation
    3. Non-maximum suppression
    4. Double threshold
    5. Edge tracking by hysteresis
    
    Args:
        image: Input image
        threshold1: Lower threshold for hysteresis
        threshold2: Upper threshold for hysteresis
    
    Returns:
        Edge-detected image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, threshold1, threshold2)
    
    return edges


def apply_histogram_equalization(image):
    """
    Apply histogram equalization for contrast enhancement
    
    Args:
        image: Input image
    
    Returns:
        Equalized image
    """
    if len(image.shape) == 3:
        # Convert to YCrCb color space
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # Equalize the Y channel
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        # Convert back to BGR
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        return cv2.equalizeHist(image)


def apply_binary_threshold(image, threshold_value=127):
    """
    Apply binary thresholding
    
    Args:
        image: Input image
        threshold_value: Threshold value (0-255)
    
    Returns:
        Binary threshold image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return binary


def apply_adaptive_threshold(image):
    """
    Apply adaptive thresholding for better results with varying lighting
    
    Args:
        image: Input image
    
    Returns:
        Adaptive threshold image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    return adaptive


def apply_morphological_erosion(image, kernel_size=5):
    """
    Apply morphological erosion
    
    Args:
        image: Input image
        kernel_size: Size of structuring element
    
    Returns:
        Eroded image
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


def apply_morphological_dilation(image, kernel_size=5):
    """
    Apply morphological dilation
    
    Args:
        image: Input image
        kernel_size: Size of structuring element
    
    Returns:
        Dilated image
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


def apply_morphological_opening(image, kernel_size=5):
    """
    Apply morphological opening (erosion followed by dilation)
    Useful for removing small objects/noise
    
    Args:
        image: Input image
        kernel_size: Size of structuring element
    
    Returns:
        Opened image
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def apply_morphological_closing(image, kernel_size=5):
    """
    Apply morphological closing (dilation followed by erosion)
    Useful for filling small holes
    
    Args:
        image: Input image
        kernel_size: Size of structuring element
    
    Returns:
        Closed image
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def apply_laplacian_edge_detection(image):
    """
    Apply Laplacian edge detection (second derivative)
    
    Args:
        image: Input image
    
    Returns:
        Edge-detected image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    
    # Convert to absolute values and scale to 0-255
    laplacian = np.absolute(laplacian)
    laplacian = np.clip(laplacian, 0, 255)
    laplacian = laplacian.astype(np.uint8)
    
    return laplacian


def invert_image(image):
    """
    Invert image colors (negative)
    
    Args:
        image: Input image
    
    Returns:
        Inverted image
    """
    return cv2.bitwise_not(image)


def apply_bilateral_filter(image):
    """
    Apply bilateral filter - edge-preserving smoothing
    
    Args:
        image: Input image
    
    Returns:
        Filtered image
    """
    return cv2.bilateralFilter(image, 9, 75, 75)


def rotate_image(image, angle):
    """
    Rotate image by specified angle
    
    Args:
        image: Input image
        angle: Rotation angle in degrees (0, 90, 180, 270)
    
    Returns:
        Rotated image
    """
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return image


def flip_image(image, direction='horizontal'):
    """
    Flip image horizontally or vertically
    
    Args:
        image: Input image
        direction: 'horizontal' or 'vertical'
    
    Returns:
        Flipped image
    """
    if direction == 'horizontal':
        return cv2.flip(image, 1)
    elif direction == 'vertical':
        return cv2.flip(image, 0)
    else:
        return image


def get_image_histogram(image):
    """
    Calculate histogram for visualization
    
    Args:
        image: Input image
    
    Returns:
        Histogram data for each channel
    """
    histograms = {}
    
    if len(image.shape) == 3:
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            histograms[col] = hist.flatten()
    else:
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        histograms['gray'] = hist.flatten()
    
    return histograms


def get_image_info(image, filename=""):
    """
    Extract and return image information
    
    Args:
        image: Input image
        filename: Original filename
    
    Returns:
        Dictionary with image information
    """
    info = {}
    
    info['filename'] = filename
    info['height'], info['width'] = image.shape[:2]
    
    if len(image.shape) == 3:
        info['channels'] = image.shape[2]
        info['type'] = 'Color (BGR)'
    else:
        info['channels'] = 1
        info['type'] = 'Grayscale'
    
    info['dtype'] = str(image.dtype)
    info['size'] = image.size
    
    return info
