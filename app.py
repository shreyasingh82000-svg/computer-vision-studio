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

# Custom CSS - Cyberpunk AI Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Cyberpunk Color System */
    :root {
        --cyber-black: #020207;
        --cyber-dark: #05050B;
        --neon-magenta: #FF00C8;
        --neon-cyan: #00E5FF;
        --cyber-purple: #7A2CFF;
        --text-primary: #F5F5FF;
        --text-secondary: #A7A7BB;
        --text-muted: #66667A;
    }
    
    /* Main Background */
    .stApp {
        background: #020207 !important;
        color: #F5F5FF !important;
    }
    
    /* Animated Background Grid */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: -1;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Scanlines */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.1),
            rgba(0, 0, 0, 0.1) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 9999;
        animation: scanline 8s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateY(0); }
        100% { transform: translateY(100%); }
    }
    
    /* Header - Futuristic Style */
    .main-header {
        background: rgba(5, 5, 11, 0.8);
        backdrop-filter: blur(12px);
        border: 2px solid transparent;
        border-image: linear-gradient(90deg, #00E5FF, #FF00C8) 1;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 229, 255, 0.1), transparent);
        animation: headerScan 3s linear infinite;
    }
    
    @keyframes headerScan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-title {
        color: #F5F5FF;
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        color: #A7A7BB;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .subtitle::before {
        content: '> ';
        color: #00E5FF;
    }
    
    .student-info {
        background: rgba(5, 5, 11, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 1rem;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .info-item {
        color: #A7A7BB;
        margin: 0.3rem 0;
        font-size: 0.9rem;
        font-family: 'Orbitron', monospace;
    }
    
    /* Sidebar - HUD Style */
    section[data-testid="stSidebar"] {
        background: rgba(2, 2, 7, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h3 {
        color: #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 1px solid rgba(0, 229, 255, 0.3);
        padding-bottom: 0.5rem;
    }
    
    section[data-testid="stSidebar"] h3::before {
        content: '[ ';
        color: #FF00C8;
    }
    
    section[data-testid="stSidebar"] h3::after {
        content: ' ]';
        color: #FF00C8;
    }
    
    /* Buttons - Cyberpunk Style */
    .stButton>button {
        background: rgba(5, 5, 11, 0.8) !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2) !important;
    }
    
    .stButton>button:hover {
        background: rgba(0, 229, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4) !important;
        transform: translateY(-2px) !important;
        border-color: #00E5FF !important;
    }
    
    /* Download Button - Magenta Style */
    .stDownloadButton>button {
        background: rgba(255, 0, 200, 0.1) !important;
        color: #FF00C8 !important;
        border: 1px solid #FF00C8 !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 0 0 10px rgba(255, 0, 200, 0.2) !important;
    }
    
    .stDownloadButton>button:hover {
        background: rgba(255, 0, 200, 0.2) !important;
        box-shadow: 0 0 20px rgba(255, 0, 200, 0.4) !important;
    }
    
    /* File Uploader - Enhanced Visibility */
    .stFileUploader {
        background: rgba(0, 229, 255, 0.05) !important;
        border: 2px dashed rgba(0, 229, 255, 0.5) !important;
        border-radius: 0 !important;
        padding: 2rem 1rem !important;
    }
    
    .stFileUploader:hover {
        background: rgba(0, 229, 255, 0.1) !important;
        border-color: #00E5FF !important;
    }
    
    .stFileUploader label {
        color: #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: rgba(5, 5, 11, 0.8) !important;
        border: 2px dashed rgba(0, 229, 255, 0.3) !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #00E5FF !important;
        background: rgba(0, 229, 255, 0.05) !important;
    }
    
    .stFileUploader button {
        background: rgba(0, 229, 255, 0.1) !important;
        border: 1px solid #00E5FF !important;
        color: #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Tabs - Neural Interface Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(5, 5, 11, 0.6);
        padding: 10px;
        border: 1px solid rgba(0, 229, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #A7A7BB !important;
        border: 1px solid transparent !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.5rem 1rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 229, 255, 0.05) !important;
        border-color: rgba(0, 229, 255, 0.3) !important;
        color: #00E5FF !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 229, 255, 0.1) !important;
        border-color: #00E5FF !important;
        color: #00E5FF !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
    }
    
    /* Sliders - Neon Style */
    .stSlider > div > div > div {
        background: rgba(0, 229, 255, 0.2) !important;
    }
    
    .stSlider > div > div > div > div {
        background: #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.5) !important;
    }
    
    /* Text Inputs */
    .stTextInput input {
        background: rgba(5, 5, 11, 0.8) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        color: #F5F5FF !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTextInput input:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.3) !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        background: rgba(5, 5, 11, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        border-left: 3px solid #00E5FF !important;
        color: #F5F5FF !important;
    }
    
    /* Info box - Cyan */
    .info-box {
        background: rgba(0, 229, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-left: 3px solid #00E5FF;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(12px);
    }
    
    .info-box h3 {
        color: #00E5FF;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 0.5rem;
    }
    
    .info-box p {
        color: #A7A7BB;
    }
    
    /* Success box - Magenta */
    .success-box {
        background: rgba(255, 0, 200, 0.05);
        border: 1px solid rgba(255, 0, 200, 0.3);
        border-left: 3px solid #FF00C8;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(12px);
    }
    
    /* Column dividers */
    [data-testid="column"] {
        border-right: 1px solid rgba(0, 229, 255, 0.1);
        padding: 1rem !important;
    }
    
    [data-testid="column"]:last-child {
        border-right: none;
    }
    
    /* Markdown styling */
    .stMarkdown {
        color: #A7A7BB !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #F5F5FF !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    }
    
    .stMarkdown strong {
        color: #00E5FF !important;
    }
    
    /* Captions */
    .stCaptionContainer {
        color: #66667A !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 0.75rem !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(5, 5, 11, 0.6) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        color: #F5F5FF !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 229, 255, 0.5) !important;
    }
    
    /* Image containers */
    img {
        border: 1px solid rgba(0, 229, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);
    }
    
    /* Metric */
    [data-testid="stMetric"] {
        background: rgba(5, 5, 11, 0.6);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 1rem;
        backdrop-filter: blur(12px);
    }
    
    [data-testid="stMetricLabel"] {
        color: #A7A7BB !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        color: #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(5, 5, 11, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00E5FF, #FF00C8);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #FF00C8, #00E5FF);
    }
    
    /* Selection */
    ::selection {
        background: rgba(0, 229, 255, 0.3);
        color: #F5F5FF;
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
        st.markdown("""
            <div style='background: rgba(0, 229, 255, 0.1); border: 2px solid #00E5FF; padding: 1rem; margin-bottom: 1.5rem; backdrop-filter: blur(12px);'>
                <div style='color: #00E5FF; font-family: Orbitron, sans-serif; font-size: 0.9rem; text-align: center; letter-spacing: 2px; margin-bottom: 0.5rem;'>
                    [ INPUT MODULE ]
                </div>
                <div style='color: #A7A7BB; font-size: 0.75rem; text-align: center; font-family: Orbitron, monospace;'>
                    // UPLOAD IMAGE TO BEGIN
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Upload
        uploaded_file = st.file_uploader(
            "◉ UPLOAD IMAGE",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Upload an image to begin neural processing"
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
        st.markdown("""
            <div style='color: #FF00C8; font-family: Orbitron, sans-serif; font-size: 0.85rem; text-align: center; letter-spacing: 2px; margin: 1rem 0 0.5rem 0;'>
                [ HISTORY CONTROL ]
            </div>
        """, unsafe_allow_html=True)
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
            st.markdown("""
                <div style='color: #FF00C8; font-family: Orbitron, sans-serif; font-size: 0.85rem; text-align: center; letter-spacing: 2px; margin: 1rem 0 0.5rem 0;'>
                    [ DATA EXPORT ]
                </div>
            """, unsafe_allow_html=True)
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
            st.markdown("""
                <div style='color: #00E5FF; font-family: Orbitron, sans-serif; font-size: 0.85rem; text-align: center; letter-spacing: 2px; margin: 1rem 0 0.5rem 0;'>
                    [ IMAGE DATA ]
                </div>
            """, unsafe_allow_html=True)
            info = ip.get_image_info(st.session_state.processed_image, 
                                     getattr(st.session_state, 'filename', 'Unknown'))
            
            st.write(f"**Filename:** {info['filename']}")
            st.write(f"**Dimensions:** {info['width']} × {info['height']}")
            st.write(f"**Channels:** {info['channels']}")
            st.write(f"**Type:** {info['type']}")
        
        st.markdown("---")
        
        # About
        st.markdown("""
            <div style='color: #FF00C8; font-family: Orbitron, sans-serif; font-size: 0.85rem; text-align: center; letter-spacing: 2px; margin: 1rem 0 0.5rem 0;'>
                [ SYSTEM OPERATORS ]
            </div>
        """, unsafe_allow_html=True)
        team_text = "\n\n".join([
            f"**{member['name']}**  \nID: {member['prn']}"
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
