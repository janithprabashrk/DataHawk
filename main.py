import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    extract_body_content,
    clean_body_content
)
from parse import parse_with_gemini
import re

# Page configuration
st.set_page_config(
    page_title="DataHawk - AI Web Scraper",
    page_icon="🦅",
    layout="wide"
)


st.title("🦅 DataHawk - AI-Powered Web Scraper")
st.markdown("Extract and parse data from any website using AI intelligence.")

# URL Input with validation
url = st.text_input("Enter Website URL:", placeholder="https://example.com")

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

if st.button("🚀 Fetch Data", type="primary"):
    if not url:
        st.error("Please enter a website URL.")
    elif not is_valid_url(url) and not url.startswith(('http://', 'https://')):
        # Try to fix URL by adding https://
        url = 'https://' + url
        if not is_valid_url(url):
            st.error("Please enter a valid URL (e.g., https://example.com)")
        else:
            st.info(f"Fixed URL: {url}")
    
    if url:
        with st.spinner("Fetching data from website..."):
            result = scrape_website(url)

            if result.startswith("Error:"):
                st.error(result)
            else:
                body_content = extract_body_content(result)
                
                if body_content.startswith("Error:"):
                    st.error(body_content)
                else:
                    cleaned_content = clean_body_content(body_content)
                    
                    if cleaned_content.startswith("Error:"):
                        st.error(cleaned_content)
                    else:
                        st.session_state.dom_content = cleaned_content
                        st.success(f"✅ Successfully fetched data from {url}")

                        with st.expander("📄 View DOM Content"):
                            st.text_area("DOM Content", cleaned_content, height=300)


# Parsing Section
if "dom_content" in st.session_state:
    st.markdown("---")
    st.subheader("🤖 AI-Powered Data Parsing")
    
    parse_description = st.text_area(
        "Describe what you want to parse:",
        placeholder="e.g., Extract all product names and prices, Get all email addresses, Find contact information...",
        height=100
    )

    col1, col2 = st.columns([1, 4])
    
    with col1:
        parse_button = st.button("🧠 Parse Content", type="primary")
    
    with col2:
        if st.button("🗑️ Clear Data"):
            if "dom_content" in st.session_state:
                del st.session_state.dom_content
            st.rerun()

    if parse_button:
        if not parse_description.strip():
            st.warning("⚠️ Please provide a description of what you want to parse.")
        else:
            with st.spinner("🤖 AI is analyzing and parsing the content..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    result = parse_with_gemini(dom_chunks, parse_description)
                    progress_bar.progress(100)
                    status_text.text("✅ Parsing completed!")
                    
                    st.markdown("### 📊 Parsed Results:")
                    if result.strip():
                        st.success("Data extracted successfully!")
                        st.text_area("Extracted Data:", result, height=300)
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Results",
                            data=result,
                            file_name="datahawk_results.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("No data found matching your description. Try a different description.")
                        
                except Exception as e:
                    st.error(f"❌ Error during parsing: {str(e)}")
                    
                finally:
                    progress_bar.empty()
                    status_text.empty()

# Sidebar with information
with st.sidebar:
    st.markdown("### 🦅 About DataHawk")
    st.markdown("""
    DataHawk is an AI-powered web scraping tool that can extract and parse data from any website.
    
    **Features:**
    - ✅ AI-powered extraction
    - ✅ Handles dynamic content
    - ✅ CAPTCHA solving
    - ✅ Custom data parsing
    
    **How to use:**
    1. Enter a website URL
    2. Click "Fetch Data" to scrape
    3. Describe what to extract
    4. Click "Parse Content" for AI analysis
    """)
    
    st.markdown("### 🔧 Settings")
    st.info("Using Google Gemini AI for parsing")
    
    if st.button("ℹ️ Show Help"):
        st.markdown("""
        **Parsing Examples:**
        - "Extract all product names and prices"
        - "Get all email addresses and phone numbers" 
        - "Find all article titles and authors"
        - "Extract company information and addresses"
        """)