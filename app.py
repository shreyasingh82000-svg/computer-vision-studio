"""
Computer Vision Image Enhancement & Edge Detection Studio
WEB APPLICATION VERSION - Streamlit

Student: Shreya Sanjay Singh Chauhan
PRN: 240105231010
Batch: A1 | Division: A | Year: TE | Branch: AIML
Academic Year: 2026-27

A modern web application for Computer Vision operations
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt
import image_processing as ip

# Page Configuration
st.set_page_config(
    page_title="CV Studio - Shreya Singh Chauhan",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --success: #00C9A7;
        --warning: #FFB800;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .student-info {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-item {
        color: #2C3E50;
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
    
    /* Card styling */
    .stCard {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Info box */
    .info-box {
        background: #E8F4FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Success box */
    .success-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'history_index' not in st.session_state:
    st.session_state.history_index = -1

# Team Information
TEAM_INFO = [
    {'name': 'Shreya Sanjay Singh Chauhan', 'prn': '240105231010'},
    {'name': 'Pranav Bansode', 'prn': '240105231033'},
    {'name': 'Yash Mali', 'prn': '240105231003'},
    {'name': 'Nidhi Sugandhi', 'prn': '240105231026'}
]

BATCH_INFO = {
    'batch': 'A1',
    'division': 'A',
    'year': 'TE',
    'branch': 'AIML',
    'academic_year': '2026-27'
}

def create_header():
    """Create beautiful header with team info"""
    team_members_html = "<br>".join([
        f"<div class='info-item'>👤 <strong>{member['name']}</strong> (PRN: {member['prn']})</div>"
        for member in TEAM_INFO
    ])
    
    st.markdown(f"""
        <div class="main-header">
            <div class="main-title">🎨 COMPUTER VISION STUDIO</div>
            <div class="subtitle">Image Enhancement & Edge Detection Platform</div>
            <div class="student-info">
                <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem; color: #2C3E50;">� Team Members</div>
                {team_members_html}
                <div class="info-item" style="margin-top: 0.5rem;">📚 {BATCH_INFO['year']} {BATCH_INFO['branch']} | Batch {BATCH_INFO['batch']} | Division {BATCH_INFO['division']}</div>
                <div class="info-item">📅 Academic Year: {BATCH_INFO['academic_year']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def add_to_history(image):
    """Add image to history"""
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history = st.session_state.history[:st.session_state.history_index + 1]
    
    st.session_state.history.append(image.copy())
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)
    else:
        st.session_state.history_index += 1

def undo():
    """Undo operation"""
    if st.session_state.history_index > 0:
        st.session_state.history_index -= 1
        st.session_state.processed_image = st.session_state.history[st.session_state.history_index].copy()
        st.success("✓ Undo successful")
        st.rerun()

def redo():
    """Redo operation"""
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history_index += 1
        st.session_state.processed_image = st.session_state.history[st.session_state.history_index].copy()
        st.success("✓ Redo successful")
        st.rerun()

def reset_image():
    """Reset to original"""
    if st.session_state.original_image is not None:
        st.session_state.processed_image = st.session_state.original_image.copy()
        st.session_state.history = [st.session_state.original_image.copy()]
        st.session_state.history_index = 0
        st.success("✓ Image reset to original")
        st.rerun()

def convert_image_for_display(image):
    """Convert OpenCV image to PIL for display"""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_download_link(image, filename="processed_image.png"):
    """Create download button for image"""
    is_success, buffer = cv2.imencode(".png", image)
    if is_success:
        return buffer.tobytes()
    return None

def main():
    """Main application"""
    
    # Header
    create_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📁 File Operations")
        
        # Upload
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Upload an image to begin processing"
        )
        
        if uploaded_file is not None:
            # Read image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if st.session_state.original_image is None or uploaded_file.name != getattr(st.session_state, 'filename', ''):
                st.session_state.original_image = image.copy()
                st.session_state.processed_image = image.copy()
                st.session_state.history = [image.copy()]
                st.session_state.history_index = 0
                st.session_state.filename = uploaded_file.name
                st.success(f"✓ Image loaded: {uploaded_file.name}")
        
        st.markdown("---")
        
        # History controls
        st.markdown("### ⏮️ History")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("↶ Undo", use_container_width=True):
                undo()
        
        with col2:
            if st.button("↷ Redo", use_container_width=True):
                redo()
        
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                reset_image()
        
        if st.session_state.history:
            st.caption(f"History: {st.session_state.history_index + 1}/{len(st.session_state.history)}")
        
        st.markdown("---")
        
        # Download
        if st.session_state.processed_image is not None:
            st.markdown("### 💾 Download")
            img_bytes = get_download_link(st.session_state.processed_image)
            if img_bytes:
                st.download_button(
                    label="📥 Download Processed Image",
                    data=img_bytes,
                    file_name=f"processed_{st.session_state.filename if hasattr(st.session_state, 'filename') else 'image.png'}",
                    mime="image/png",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        # Image Info
        if st.session_state.processed_image is not None:
            st.markdown("### ℹ️ Image Info")
            info = ip.get_image_info(st.session_state.processed_image, 
                                     getattr(st.session_state, 'filename', 'Unknown'))
            
            st.write(f"**Filename:** {info['filename']}")
            st.write(f"**Dimensions:** {info['width']} × {info['height']}")
            st.write(f"**Channels:** {info['channels']}")
            st.write(f"**Type:** {info['type']}")
        
        st.markdown("---")
        
        # About
        st.markdown("### � Team")
        team_text = "\n\n".join([
            f"**{member['name']}**  \nPRN: {member['prn']}"
            for member in TEAM_INFO
        ])
        st.info(f"""
        {team_text}
        
        **Course:** {BATCH_INFO['year']} {BATCH_INFO['branch']}
        
        **Batch:** {BATCH_INFO['batch']} | **Division:** {BATCH_INFO['division']}
        
        **Academic Year:** {BATCH_INFO['academic_year']}
        """)
    
    # Main content
    if st.session_state.original_image is None:
        st.markdown("""
            <div class="info-box">
                <h3>👋 Welcome to Computer Vision Studio!</h3>
                <p>Please upload an image using the sidebar to begin processing.</p>
                <p><strong>Supported formats:</strong> JPG, JPEG, PNG, BMP, TIFF</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show features
        st.markdown("###  Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎨 Basic Operations**
            - Grayscale Conversion
            - Brightness & Contrast
            - Histogram Equalization
            - Image Inversion
            """)
        
        with col2:
            st.markdown("""
            **🔧 Filters**
            - Gaussian Blur
            - Median Filter
            - Sharpening
            - Bilateral Filter
            """)
        
        with col3:
            st.markdown("""
            **📐 Advanced**
            - Edge Detection (Sobel, Canny, Laplacian)
            - Thresholding (Binary, Adaptive)
            - Morphological Operations
            - Transformations (Rotate, Flip)
            """)
    
    else:
        # Display images
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📷 Original Image")
            st.image(convert_image_for_display(st.session_state.original_image), 
                    use_container_width=True)
        
        with col2:
            st.markdown("### ✨ Processed Image")
            st.image(convert_image_for_display(st.session_state.processed_image), 
                    use_container_width=True)
        
        # Operations tabs
        st.markdown("---")
        st.markdown("### 🎨 Image Processing Operations")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎨 Basic",
            "🔧 Filters", 
            "📐 Edge Detection",
            "🎚️ Thresholding",
            "🔬 Morphological",
            "🔄 Transform"
        ])
        
        # Tab 1: Basic Operations
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⚫ Grayscale", use_container_width=True):
                    st.session_state.processed_image = ip.convert_to_grayscale(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Grayscale applied")
                    st.rerun()
                
                if st.button("🔆 Histogram Equalization", use_container_width=True):
                    st.session_state.processed_image = ip.apply_histogram_equalization(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Histogram equalization applied")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Invert", use_container_width=True):
                    st.session_state.processed_image = ip.invert_image(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Invert applied")
                    st.rerun()
            
            with col3:
                if st.button("📊 Show Histogram", use_container_width=True):
                    histograms = ip.get_image_histogram(st.session_state.processed_image)
                    
                    fig, ax = plt.subplots(figsize=(10, 4))
                    
                    if 'gray' in histograms:
                        ax.plot(histograms['gray'], color='black', label='Intensity')
                        ax.fill_between(range(256), histograms['gray'], alpha=0.3)
                    else:
                        colors = {'b': 'blue', 'g': 'green', 'r': 'red'}
                        for key, color in colors.items():
                            if key in histograms:
                                ax.plot(histograms[key], color=color, label=color.upper(), alpha=0.7)
                    
                    ax.set_xlabel('Pixel Intensity')
                    ax.set_ylabel('Frequency')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            
            st.markdown("---")
            
            # Sliders
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**☀️ Brightness**")
                brightness = st.slider("Adjust brightness", -100, 100, 0, key="brightness")
                if st.button("Apply Brightness", use_container_width=True):
                    st.session_state.processed_image = ip.adjust_brightness(st.session_state.processed_image, brightness)
                    add_to_history(st.session_state.processed_image)
                    st.success(f"✓ Brightness adjusted: {brightness}")
                    st.rerun()
            
            with col2:
                st.markdown("**🔅 Contrast**")
                contrast = st.slider("Adjust contrast", 0.5, 2.0, 1.0, 0.1, key="contrast")
                if st.button("Apply Contrast", use_container_width=True):
                    st.session_state.processed_image = ip.adjust_contrast(st.session_state.processed_image, contrast)
                    add_to_history(st.session_state.processed_image)
                    st.success(f"✓ Contrast adjusted: {contrast}")
                    st.rerun()
        
        # Tab 2: Filters
        with tab2:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🌫️ Gaussian Blur", use_container_width=True):
                    st.session_state.processed_image = ip.apply_gaussian_blur(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Gaussian blur applied")
                    st.rerun()
            
            with col2:
                if st.button("🔲 Median Filter", use_container_width=True):
                    st.session_state.processed_image = ip.apply_median_filter(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Median filter applied")
                    st.rerun()
            
            with col3:
                if st.button("✨ Sharpen", use_container_width=True):
                    st.session_state.processed_image = ip.apply_sharpening(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Sharpening applied")
                    st.rerun()
            
            with col4:
                if st.button("🎭 Bilateral Filter", use_container_width=True):
                    st.session_state.processed_image = ip.apply_bilateral_filter(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Bilateral filter applied")
                    st.rerun()
        
        # Tab 3: Edge Detection
        with tab3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Sobel Edge", use_container_width=True):
                    st.session_state.processed_image = ip.apply_sobel_edge_detection(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Sobel edge detection applied")
                    st.rerun()
            
            with col2:
                if st.button("🎯 Canny Edge", use_container_width=True):
                    st.session_state.processed_image = ip.apply_canny_edge_detection(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Canny edge detection applied")
                    st.rerun()
            
            with col3:
                if st.button("◆ Laplacian Edge", use_container_width=True):
                    st.session_state.processed_image = ip.apply_laplacian_edge_detection(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Laplacian edge detection applied")
                    st.rerun()
        
        # Tab 4: Thresholding
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                threshold_val = st.slider("Threshold Value", 0, 255, 127, key="threshold")
                if st.button("⬛⬜ Binary Threshold", use_container_width=True):
                    st.session_state.processed_image = ip.apply_binary_threshold(st.session_state.processed_image, threshold_val)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Binary threshold applied")
                    st.rerun()
            
            with col2:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if st.button("🔄 Adaptive Threshold", use_container_width=True):
                    st.session_state.processed_image = ip.apply_adaptive_threshold(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Adaptive threshold applied")
                    st.rerun()
        
        # Tab 5: Morphological
        with tab5:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("⊖ Erosion", use_container_width=True):
                    st.session_state.processed_image = ip.apply_morphological_erosion(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Erosion applied")
                    st.rerun()
            
            with col2:
                if st.button("⊕ Dilation", use_container_width=True):
                    st.session_state.processed_image = ip.apply_morphological_dilation(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Dilation applied")
                    st.rerun()
            
            with col3:
                if st.button("○ Opening", use_container_width=True):
                    st.session_state.processed_image = ip.apply_morphological_opening(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Opening applied")
                    st.rerun()
            
            with col4:
                if st.button("● Closing", use_container_width=True):
                    st.session_state.processed_image = ip.apply_morphological_closing(st.session_state.processed_image)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Closing applied")
                    st.rerun()
        
        # Tab 6: Transform
        with tab6:
            st.markdown("**🔄 Rotation**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("↻ 90° CW", use_container_width=True):
                    st.session_state.processed_image = ip.rotate_image(st.session_state.processed_image, 90)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Rotated 90°")
                    st.rerun()
            
            with col2:
                if st.button("↻ 180°", use_container_width=True):
                    st.session_state.processed_image = ip.rotate_image(st.session_state.processed_image, 180)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Rotated 180°")
                    st.rerun()
            
            with col3:
                if st.button("↺ 270° CW", use_container_width=True):
                    st.session_state.processed_image = ip.rotate_image(st.session_state.processed_image, 270)
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Rotated 270°")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**↔️ Flip**")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("↔️ Horizontal", use_container_width=True):
                    st.session_state.processed_image = ip.flip_image(st.session_state.processed_image, 'horizontal')
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Flipped horizontally")
                    st.rerun()
            
            with col2:
                if st.button("↕️ Vertical", use_container_width=True):
                    st.session_state.processed_image = ip.flip_image(st.session_state.processed_image, 'vertical')
                    add_to_history(st.session_state.processed_image)
                    st.success("✓ Flipped vertically")
                    st.rerun()
    
    # Footer
    st.markdown("---")
    team_names = ", ".join([member['name'] for member in TEAM_INFO])
    st.markdown(f"""
        <div class="footer">
            <p><strong>Computer Vision Image Processing Studio</strong></p>
            <p>Developed by: {team_names}</p>
            <p>{BATCH_INFO['year']} {BATCH_INFO['branch']} | Batch {BATCH_INFO['batch']} | Division {BATCH_INFO['division']} | Academic Year: {BATCH_INFO['academic_year']}</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
