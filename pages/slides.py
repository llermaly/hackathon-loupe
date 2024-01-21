import asyncio
import json
import os

import streamlit as st

from slides_core.index import get_slides_url

st.title("Slides page")

url = "https://www.k12.com/"
id = url.replace("http://", "").replace("https://", "")

if os.path.exists("./tmp/audio.wav"):
    os.remove("./tmp/audio.wav")

initial_json = """{
    "company_name": "Clarifai",
    "website": "https://clarifai.com",
    "content": "So great knifes",
    "logo": "https://img.freepik.com/psd-gratis/logo-gradiente-abstracto_23-2150689648.jpg?w=740&t=st=1705693169~exp=1705693769~hmac=d5aec7d0900982211c119cfeccea92257d2a92ea2b91aa8243ac85168fa77278",
    "main_screenshot": "https://i.ytimg.com/vi/AKnpqlVJ0Wg/0.jpg",
    "features": {
        "search": true,
        "typo_tolerance": false,
        "title_search": false,
        "desc_search": false,
        "autocomplete": true,
        "highlighting": true,
        "thumbnails": false,
        "filters": false,
        "sorting": false,
        "pagination": false
    }
}

"""

# Create a form to receive user input
with st.form(key="my_form"):
    text_area_data = st.text_area("Enter JSON data:", initial_json, height=300)
    model = st.selectbox("Select your model", ("GPT-3_5-turbo", "GPT-4", "gpt-4-turbo"))
    submitted = st.form_submit_button("Generate Report")

    if submitted:
        try:
            json_data = json.loads(text_area_data)
            st.success("JSON data successfully loaded.")

        except json.JSONDecodeError:
            st.error("Error: Invalid JSON format. Please enter valid JSON data.")

        try:
            with st.spinner("Generating slides..."):
                slides_url = get_slides_url(json_data, model)
                st.success("Slides successfully generated.")

                if os.path.exists("./tmp/audio.wav"):
                    st.header("First, listen the following audio:")
                    audio_file = open("./tmp/audio.wav", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/wav")

                st.header("Now, see the slides generated:")
                st.write(slides_url)
        except Exception as e:
            st.error("Error: Generating slides failed.")


# st.image(images["results_screenshot"])
