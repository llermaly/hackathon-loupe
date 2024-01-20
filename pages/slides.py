import asyncio

import streamlit as st

# from core.navigation_agent import navigate_website
from slides_core.ai_requests import get_analysis, get_audio, get_image
from slides_core.slides import dup_slide, replace_slides_elements
from slides_core.utils import get_json_data, get_requests_arr

st.title("Slides page")

url = "https://www.k12.com/"
id = url.replace("http://", "").replace("https://", "")

initial_json = """{
        "complany_name": "Clarifai",
        "website": "https://clarifai.com",
        "content": "So great knifes",
        "logo": "https://img.freepik.com/psd-gratis/logo-gradiente-abstracto_23-2150689648.jpg?w=740&t=st=1705693169~exp=1705693769~hmac=d5aec7d0900982211c119cfeccea92257d2a92ea2b91aa8243ac85168fa77278",
        "main_screenshot": "https://i.ytimg.com/vi/AKnpqlVJ0Wg/0.jpg",
        "features": {
            "search": True,
            "typo_tolerance": False,
            "title_search": False,
            "desc_search": False,
            "autocomplete": True,
            "highlighting": True,
            "thumbnails": False,
            "filters": False,
            "sorting": False,
            "pagination": False,
        },
    }
"""

# Create a form to receive user input
with st.form(key="my_form"):
    json_form_data = st.text_area("Enter JSON data:", initial_json, height=300)
    model = st.selectbox(
        "Select your model", ("gpt-3.5-turbo-1106", "gpt-4-1106-preview", "gpt-4")
    )
    submitted = st.form_submit_button("Generate Report")

# if submitted:
# with st.spinner("Loading"):
# images = asyncio.run(navigate_website(url, id, model, prompt))
# st.write(images)
# st.header("Website")
# st.image(images["web_screenshot"])
# st.header("Search bar")
# st.image(images["search_bar"])
# st.header("Results")
# st.image(images["results_screenshot"])
