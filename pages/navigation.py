import streamlit as st
import streamlit as st
from core.navigation_agent import navigate_website
import asyncio

st.title("Navigate page")

url = "https://www.k12.com/"
id = url.replace('http://', '').replace('https://', '')

prompt = """You are a search expert and. Your goal is to evaluate the search quality of the website provided.

Your tasks are: 

1. Take a screenshot of the initial state with the name web_screenshot
2. Find the search bar and type the name of the company 
3. Take another screenshot called search_bar
4. Press Enter 
5. Take a screenshot of the results page called results_screenshot
"""

# Create a form to receive user input
with st.form(key="my_form"):
    url = st.text_input("Enter URL:", url)
    id = st.text_input("Enter ID:", id)
    model = st.selectbox(
        'Select your model',
        ('gpt-3.5-turbo-1106', 'gpt-4-1106-preview', 'gpt-4'))
    prompt = st.text_area("Enter prompt:", prompt, height=300)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    with st.spinner("Loading"):
        images = asyncio.run(navigate_website(url, id, model, prompt))
        st.write(images)
        st.header("Website")
        st.image(images["web_screenshot"])
        st.header("Search bar")
        st.image(images["search_bar"])
        st.header("Results")
        st.image(images["results_screenshot"])
