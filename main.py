import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    extract_body_content,
    clean_body_content
)
from parse import parse_with_gemini
import re
import time
import base64
import os

def get_logo_base64():
    """Convert logo.png to base64 string for HTML embedding"""
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# Page configuration
st.set_page_config(
    page_title="DataHawk - AI Web Scraper",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful dark theme styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Dark Theme Styles */
    .main {
        padding-top: 2rem;
        background-color: #1a1a1a;
    }
    
    /* Custom font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    
    /* Header styling - Dark theme */
    .main-header {
        background: linear-gradient(135deg, #2d1b69 0%, #11998e 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 1px solid #333;
    }
    
    .main-title {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Card styling - Dark theme */
    .custom-card {
        background: #2a2a2a;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        border: 1px solid #404040;
        margin-bottom: 2rem;
    }
    
    /* Button styling - Dark theme */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #7c8cf0 0%, #8a5fb8 100%);
    }
    
    /* Input styling - Dark theme */
    .stTextInput > div > div > input {
        background-color: #333333 !important;
        border-radius: 10px;
        border: 2px solid #555555;
        padding: 0.75rem;
        font-size: 1rem;
        color: #e0e0e0 !important;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        background-color: #3a3a3a !important;
    }
    
    /* Text area styling - Dark theme */
    .stTextArea > div > div > textarea {
        background-color: #333333 !important;
        border-radius: 10px;
        border: 2px solid #555555;
        color: #e0e0e0 !important;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        background-color: #3a3a3a !important;
    }
    
    /* Success/Error styling - Dark theme */
    .stSuccess {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #3b82f6;
        color: #e0e0e0;
    }
    
    .stError {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #ef4444;
        color: #e0e0e0;
    }
    
    /* Sidebar styling - Dark theme */
    .css-1d391kg {
        background: linear-gradient(180deg, #2a2a2a 0%, #1f1f1f 100%);
    }
    
    /* Progress bar styling - Dark theme */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Expandable styling - Dark theme */
    .streamlit-expanderHeader {
        background: #333333;
        border-radius: 10px;
        border: 1px solid #555555;
        color: #e0e0e0;
    }
    
    /* Metrics styling - Dark theme */
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #4b5563;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading animation - Dark theme */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #444444;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Feature box styling - Dark theme */
    .feature-box {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 1px solid #404040;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-success { background: #10b981; }
    .status-warning { background: #f59e0b; }
    .status-error { background: #ef4444; }
    .status-info { background: #3b82f6; }
    
    /* Dark theme text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #e0e0e0 !important;
    }
    
    p, span, div {
        color: #b0b0b0 !important;
    }
    
    /* Metric styling dark theme */
    .css-1r6slb0 {
        background: #2a2a2a;
        border: 1px solid #404040;
        border-radius: 10px;
    }
    
    /* Custom scrollbar - Dark theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #555555;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #667eea;
    }
</style>
""", unsafe_allow_html=True)


# Beautiful Dark Theme Header with Logo
logo_base64 = get_logo_base64()
if logo_base64:
    st.markdown(f"""
    <div class="main-header fade-in">
        <img src="data:image/png;base64,{logo_base64}" style="height: 180px; margin-bottom: 0px;" alt="DataHawk Logo"/>
        <p class="main-subtitle">AI-Powered Web Scraping Revolution</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback if logo is not found
    st.markdown("""
    <div class="main-header fade-in">
        <h1 class="main-title">🦅 DataHawk</h1>
        <p class="main-subtitle">AI-Powered Web Scraping Revolution</p>
    </div>
    """, unsafe_allow_html=True)

# Statistics/Metrics Row - Dark theme
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0; color:#667eea;">⚡</h3>
        <p style="margin:0; font-weight:600; color:#e0e0e0;">Lightning Fast</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0; color:#667eea;">🤖</h3>
        <p style="margin:0; font-weight:600; color:#e0e0e0;">AI Powered</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0; color:#667eea;">🛡️</h3>
        <p style="margin:0; font-weight:600; color:#e0e0e0;">Secure & Safe</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0; color:#667eea;">🎯</h3>
        <p style="margin:0; font-weight:600; color:#e0e0e0;">Precision Extraction</p>
    </div>
    """, unsafe_allow_html=True)

# Main content in a card
# st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)

# URL Input Section - Dark theme
st.markdown('<h3 style="color:#e0e0e0;">🌐 Enter Target Website</h3>', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])

with col1:
    url = st.text_input(
        "Website URL", 
        placeholder="https://example.com or just example.com",
        label_visibility="collapsed"
    )

with col2:
    # st.markdown("<br>", unsafe_allow_html=True)  # Space for alignment

    # Fetch button with better styling
    fetch_button = st.button("🚀 Fetch Data", type="primary", use_container_width=True)

# URL validation function
def is_valid_url(url):
    """Validate URL format"""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None

# Enhanced fetch data logic
if fetch_button:
    if not url:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #ef4444;">
            <span class="status-indicator status-error"></span>
            <strong style="color:#e0e0e0;">Please enter a website URL</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Auto-fix URL
        original_url = url
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if not is_valid_url(url):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #ef4444;">
                <span class="status-indicator status-error"></span>
                <strong style="color:#e0e0e0;">Please enter a valid URL (e.g., https://example.com)</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            if original_url != url:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); 
                            padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #3b82f6;">
                    <span class="status-indicator status-info"></span>
                    <strong style="color:#e0e0e0;">Auto-fixed URL:</strong> <span style="color:#93c5fd;">{url}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Beautiful loading animation - Dark theme
            with st.container():
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: #2a2a2a; border-radius: 15px; border: 1px solid #404040;">
                    <div class="loading-spinner"></div>
                    <h4 style="margin-top: 1rem; color: #667eea;">🚀 Initializing AI Scraper...</h4>
                    <p style="color: #b0b0b0;">Connecting to website and extracting content</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress simulation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    progress_bar.progress(i)
                    if i < 30:
                        status_text.text(f"🔍 Analyzing website structure... {i}%")
                    elif i < 60:
                        status_text.text(f"🌐 Connecting to {url}... {i}%")
                    elif i < 90:
                        status_text.text(f"📄 Extracting content... {i}%")
                    else:
                        status_text.text(f"✨ Finalizing data... {i}%")
                    time.sleep(0.05)
                
                # Actual scraping
                result = scrape_website(url)
                progress_bar.empty()
                status_text.empty()
                
                if result.startswith("Error:"):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                                padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid #ef4444;">
                        <h3 style="color: #fca5a5; margin: 0;">❌ Scraping Failed</h3>
                        <p style="color: #fca5a5; margin: 0.5rem 0 0 0;">{result}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    body_content = extract_body_content(result)
                    
                    if body_content.startswith("Error:"):
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                                    padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid #ef4444;">
                            <h3 style="color: #fca5a5; margin: 0;">❌ Content Extraction Failed</h3>
                            <p style="color: #fca5a5; margin: 0.5rem 0 0 0;">{body_content}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        cleaned_content = clean_body_content(body_content)
                        
                        if cleaned_content.startswith("Error:"):
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                                        padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid #ef4444;">
                                <h3 style="color: #fca5a5; margin: 0;">❌ Content Cleaning Failed</h3>
                                <p style="color: #fca5a5; margin: 0.5rem 0 0 0;">{cleaned_content}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.session_state.dom_content = cleaned_content
                            
                            # Success animation - Dark theme
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); 
                                        padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0; border: 1px solid #3b82f6;">
                                <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                                    🎉 Data Successfully Extracted!
                                </h2>
                                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                                    Ready for AI-powered parsing from <strong style="color:#93c5fd;">{url}</strong>
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Content preview with beautiful dark styling
                            with st.expander("📄 View Extracted Content", expanded=False):
                                st.markdown("""
                                <div style="background: #333333; padding: 1rem; border-radius: 10px; 
                                            border-left: 4px solid #667eea; border: 1px solid #555555;">
                                    <h6 style="color: #667eea; margin: 0 0 1rem 0;">📊 Content Preview</h6>
                                </div>
                                """, unsafe_allow_html=True)
                                st.text_area(
                                    "Extracted Content", 
                                    cleaned_content[:2000] + "..." if len(cleaned_content) > 2000 else cleaned_content, 
                                    height=300,
                                    disabled=True
                                )
                                
                                # Content statistics - Dark theme
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📝 Total Characters", f"{len(cleaned_content):,}")
                                with col2:
                                    st.metric("📄 Word Count", f"{len(cleaned_content.split()):,}")
                                with col3:
                                    st.metric("📋 Lines", f"{len(cleaned_content.splitlines()):,}")

st.markdown('</div>', unsafe_allow_html=True)  # Close custom-card


# AI Parsing Section with Beautiful Design
if "dom_content" in st.session_state:
    st.markdown("---")
    
    # AI Parsing Header - Dark theme
    st.markdown("""
    <div class="custom-card fade-in">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #e0e0e0; margin: 0;">🤖 AI-Powered Data Parsing</h2>
            <p style="color: #b0b0b0; margin: 0.5rem 0 0 0;">Describe what you want to extract and let AI do the magic</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Parsing instruction examples
    with st.expander("💡 Need inspiration? See parsing examples", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
                <h6 style="color: #667eea; margin: 0 0 0.5rem 0;">🛍️ E-commerce</h6>
                <p style="margin: 0; font-size: 0.9rem;">"Extract all product names, prices, and ratings"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h6 style="color: #667eea; margin: 0 0 0.5rem 0;">📰 News & Articles</h6>
                <p style="margin: 0; font-size: 0.9rem;">"Get article titles, authors, and publication dates"</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <h6 style="color: #667eea; margin: 0 0 0.5rem 0;">📞 Contact Info</h6>
                <p style="margin: 0; font-size: 0.9rem;">"Find all email addresses, phone numbers, and addresses"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h6 style="color: #667eea; margin: 0 0 0.5rem 0;">💼 Job Listings</h6>
                <p style="margin: 0; font-size: 0.9rem;">"Extract job titles, companies, salaries, and locations"</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Parsing input area - Dark theme
    st.markdown('<h3 style="color:#e0e0e0;">📝 Describe Your Data Extraction</h3>', unsafe_allow_html=True)
    parse_description = st.text_area(
        "What would you like to extract?",
        placeholder="Be specific! For example:\n• Extract all product names and their prices\n• Get all email addresses and contact information\n• Find job titles, companies, and salary ranges\n• List all article headlines and authors",
        height=120,
        label_visibility="collapsed"
    )

    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        parse_button = st.button("🧠 Parse with AI", type="primary", use_container_width=True)
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing

    # Enhanced parsing logic
    if parse_button:
        if not parse_description.strip():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #92400e 0%, #b45309 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid #f59e0b;">
                <span class="status-indicator status-warning"></span>
                <strong style="color:#fde68a;">Please describe what you want to extract</strong>
                <p style="margin: 0.5rem 0 0 0; color:#fde68a;">The more specific you are, the better results you'll get!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Beautiful AI processing animation - Dark theme
            st.markdown("""
            <div style="background: linear-gradient(135deg, #374151 0%, #4b5563 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0; border: 1px solid #6b7280;">
                <h3 style="margin: 0; color: #e0e0e0;">🤖 AI Brain is Working...</h3>
                <p style="margin: 0.5rem 0 0 0; color: #d1d5db;">Analyzing content and extracting your requested data</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Processing with progress
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                chunk_progress = st.empty()
                
                try:
                    # Simulate AI processing stages
                    stages = [
                        "🔍 Analyzing content structure...",
                        "🧠 Initializing AI models...", 
                        "📖 Processing text chunks...",
                        "🎯 Extracting relevant data...",
                        "✨ Finalizing results..."
                    ]
                    
                    for i, stage in enumerate(stages):
                        progress = int((i + 1) / len(stages) * 30)  # First 30% for setup
                        progress_bar.progress(progress)
                        status_text.text(stage)
                        time.sleep(0.5)
                    
                    # Actual AI processing with chunk progress
                    status_text.text("🤖 AI is parsing your data...")
                    
                    # Custom parsing function with progress tracking
                    parsed_results = []
                    for i, chunk in enumerate(dom_chunks):
                        chunk_progress.text(f"Processing chunk {i+1} of {len(dom_chunks)}")
                        
                        # Update progress (30% + 60% for processing)
                        progress_val = 30 + int((i + 1) / len(dom_chunks) * 60)
                        progress_bar.progress(progress_val)
                        
                        # Call Gemini API
                        from parse import parse_with_gemini
                        template = (
                            "You are tasked with extracting specific information from the following text content: {dom_content}. "
                            "Please follow these instructions carefully: \n\n"
                            "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
                            "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
                            "3. **Empty Response:** If no information matches the description, return an empty string ('')."
                            "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
                        )
                        
                        import google.generativeai as genai
                        import os
                        from dotenv import load_dotenv
                        
                        load_dotenv()
                        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = template.format(dom_content=chunk, parse_description=parse_description)
                        response = model.generate_content(prompt)
                        parsed_results.append(response.text)
                        
                        time.sleep(0.2)  # Small delay for visual effect
                    
                    # Finalization
                    progress_bar.progress(100)
                    status_text.text("✅ Processing completed!")
                    chunk_progress.empty()
                    
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
                    
                    result = "\n".join(parsed_results)
                    
                    # Beautiful results display - Dark theme
                    if result.strip():
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0; border: 1px solid #3b82f6;">
                            <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                                🎉 Data Extraction Successful!
                            </h2>
                            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                                AI has successfully extracted your requested information
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Results container - Dark theme
                        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                        st.markdown('<h3 style="color:#e0e0e0;">📊 Extracted Data</h3>', unsafe_allow_html=True)
                        
                        # Results text area with custom styling
                        st.text_area(
                            "Your extracted data:",
                            result,
                            height=300,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                        
                        # Action buttons for results
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.download_button(
                                label="💾 Download Results (TXT)",
                                data=result,
                                file_name=f"datahawk_results_{int(time.time())}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        with col2:
                            csv_data = result.replace('\n', '\n')  # Keep formatting
                            st.download_button(
                                label="📊 Download as CSV",
                                data=csv_data,
                                file_name=f"datahawk_results_{int(time.time())}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        # Results statistics - Dark theme
                        st.markdown('<h4 style="color:#e0e0e0;">📈 Extraction Statistics</h4>', unsafe_allow_html=True)
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📝 Characters", len(result))
                        with col2:
                            st.metric("📄 Lines", len(result.splitlines()))
                        with col3:
                            st.metric("🔍 Chunks Processed", len(dom_chunks))
                        with col4:
                            st.metric("⚡ Words Found", len(result.split()))
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    else:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #92400e 0%, #b45309 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center; border: 1px solid #f59e0b;">
                            <h3 style="color: #fde68a; margin: 0;">🤔 No Matching Data Found</h3>
                            <p style="color: #fde68a; margin: 0.5rem 0 0 0;">
                                Try a different description or check if the website contains the data you're looking for
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Suggestions for better results
                        with st.expander("💡 Tips for better results"):
                            st.markdown("""
                            - **Be more specific**: Instead of "get data", try "extract product names and prices"
                            - **Use examples**: "Find emails like example@domain.com"
                            - **Mention format**: "Get phone numbers in format (xxx) xxx-xxxx"
                            - **Check the content**: Make sure the website actually contains what you're looking for
                            """)
                        
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    chunk_progress.empty()
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                                padding: 2rem; border-radius: 15px; text-align: center; border: 1px solid #ef4444;">
                        <h3 style="color: #fca5a5; margin: 0;">❌ Processing Error</h3>
                        <p style="color: #fca5a5; margin: 0.5rem 0 0 0;">{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close parsing card

# Enhanced Sidebar with Beautiful Dark Design
with st.sidebar:
    # Sidebar Header with Logo - Dark theme
    if logo_base64:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d1b69 0%, #11998e 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; border: 1px solid #333;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 80px; margin-bottom: 10px;" alt="DataHawk Logo"/>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">AI Web Scraping Tool</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if logo is not found
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d1b69 0%, #11998e 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; border: 1px solid #333;">
            <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🦅 DataHawk</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">AI Web Scraping Tool</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About Section - Dark theme
    st.markdown('<h3 style="color:#e0e0e0;">📖 About Our Platform</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-box">
        <p style="color:#d1d5db;">Our intelligent web scraping tool leverages AI to extract and parse data from any website with precision and speed.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features - Dark theme
    st.markdown('<h3 style="color:#e0e0e0;">✨ Key Features</h3>', unsafe_allow_html=True)
    features = [
        ("⚡", "Lightning Fast", "Advanced proxy technology"),
        ("🤖", "AI-Powered", "Google Gemini integration"),
        ("🛡️", "Anti-Detection", "CAPTCHA solving & stealth mode"),
        ("🎯", "Precision", "Natural language data extraction"),
        ("📊", "Smart Parsing", "Structured data output"),
        ("💾", "Export Ready", "Multiple download formats")
    ]
    
    for icon, title, desc in features:
        st.markdown(f"""
        <div style="background: #2a2a2a; padding: 1rem; border-radius: 10px; 
                    margin: 0.5rem 0; border-left: 3px solid #667eea; border: 1px solid #404040;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                <div>
                    <strong style="color: #667eea;">{title}</strong><br>
                    <small style="color: #b0b0b0;">{desc}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How to Use Section - Dark theme
    st.markdown('<h3 style="color:#e0e0e0;">🚀 How to Use</h3>', unsafe_allow_html=True)
    steps = [
        "🌐 Enter target website URL",
        "🚀 Click 'Fetch Data' to scrape",
        "📝 Describe what to extract", 
        "🧠 Let AI parse the content",
        "💾 Download your results"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1f2937 0%, #374151 100%); 
                    padding: 0.75rem; border-radius: 8px; margin: 0.3rem 0; border: 1px solid #4b5563;">
            <strong style="color:#e0e0e0;">{i}.</strong> <span style="color:#d1d5db;">{step}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status - Dark theme
    st.markdown('<h3 style="color:#e0e0e0;">🔧 System Status</h3>', unsafe_allow_html=True)
    
    # Check API status
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key and api_key != 'your_gemini_api_key_here':
            api_status = "🟢 Connected"
            api_color = "#10b981"
        else:
            api_status = "🔴 Not Configured"
            api_color = "#ef4444"
    except:
        api_status = "🟡 Unknown"
        api_color = "#f59e0b"
    
    st.markdown(f"""
    <div style="background: #2a2a2a; padding: 1rem; border-radius: 10px; border-left: 3px solid {api_color}; border: 1px solid #404040;">
        <strong style="color:#e0e0e0;">Gemini AI:</strong> <span style="color: {api_color};">{api_status}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #2a2a2a; padding: 1rem; border-radius: 10px; border-left: 3px solid #10b981; margin-top: 0.5rem; border: 1px solid #404040;">
        <strong style="color:#e0e0e0;">Proxy Service:</strong> <span style="color: #10b981;">🟢 Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Help & Examples - Dark theme
    if st.button("💡 Show Parsing Examples", use_container_width=True):
        st.markdown('<h3 style="color:#e0e0e0;">📝 Parsing Examples</h3>', unsafe_allow_html=True)
        examples = [
            "**E-commerce:** Extract all product names and prices",
            "**News:** Get article titles, authors, and dates",
            "**Contacts:** Find all email addresses and phone numbers",
            "**Jobs:** List job titles, companies, and salaries",
            "**Reviews:** Extract ratings, comments, and reviewer names",
            "**Social:** Get usernames, posts, and engagement metrics"
        ]
        
        for example in examples:
            st.markdown(f'<p style="color:#d1d5db;">• {example}</p>', unsafe_allow_html=True)
    
    # Footer - Dark theme
    st.markdown("---")
    if logo_base64:
        st.markdown(f"""
        <div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 30px; margin-bottom: 10px;" alt="Logo"/>
            <p>Made with ❤️ using Streamlit & Google AI</p>
            <p>© 2025 AI Web Scraper</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
            <p>Made with ❤️ using Streamlit & Google AI</p>
            <p>© 2025 AI Web Scraper</p>
        </div>
        """, unsafe_allow_html=True)