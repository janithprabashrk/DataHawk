import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    extract_body_content,
    clean_body_content
)


st.title("DataHawk")

url = st.text_input("Enter Website URL : ")

if st.button("Fetch Data"):
    st.write(f"Fetching data from {url}...")

    result = scrape_website(url)

    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.write("DOM Content", cleaned_content, height=300)
