import streamlit as st
from scrape import scrape_website


st.title("DataHawk")

url = st.text_input("Enter Website URL : ")

if st.button("Fetch Data"):
    st.write(f"Fetching data from {url}...")
    result = scrape_website(url)
    print(result)
