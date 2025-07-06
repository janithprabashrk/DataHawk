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


if "dom_content" in st.session_state:
    parse_description = st.text_area(
        "Describe what you want to pars?"
    )

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(
                st.session_state.dom_content
            )