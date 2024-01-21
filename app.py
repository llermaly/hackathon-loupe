import asyncio
import json
import os

import pandas as pd
import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

from core.navigation.agent import navigate_website
from core.slides.ai_requests import get_analysis, get_audio, get_image
from core.slides.google_requests import (
    dup_slide,
    replace_slides_elements,
    upload_file_to_drive,
)
from core.slides.utils import get_audio_prompt, get_requests_arr, get_text_prompt

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

css = r"""
    <style>
        [data-testid="stForm"] {border: 0px;padding:0px}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("Welcome to Loupe🔎")

st.markdown(
    """👋🏻 Loupe🔎 is an end-to-end leads hunter. It will do the following:
- Analyze the website of your choice
- Understand the strenghs and weaknesses of the website's search experience
- Generate a cold call script
- Generate a sales deck
"""
)

with st.form(key="analysis"):
    site_url = st.text_input("Site URL", value="https://www.k12.com")
    submitted = st.form_submit_button("Start Analysis")
    headless = st.checkbox("Headless mode", value=True)

# state = {
#     "website": "https://www.k12.com",
#     "company_name": "k12",
#     "logo": "https://www.k12.com/wp-content/themes/pl-scaffold-theme/dist/images/logo_new.svg",
#     "features": {
#         "search": True,
#         "typo_tolerance": False,
#         "title_search": False,
#         "desc_search": False,
#         "autocomplete": True,
#         "highlighting": True,
#         "thumbnails": False,
#         "filters": False,
#         "sorting": False,
#         "pagination": False
#     },
#     "content": "The website offers online learning programs for students from kindergarten through career prep. It provides a flexible and personalized approach to education for parents and students seeking a safer and more engaging learning experience. The programs include virtual public schools, one-on-one tutoring, private elementary schools, esports, and individual courses for homeschoolers. K12 also offers resources like the Strider Activity Hub and K12 Zone for interactive learning and social activities. The website emphasizes the importance of choice, flexibility, and personalized learning in education and offers enrollment options, FAQs, and contact information for those interested in learning more.",
#     "main_screenshot": "tmp/k12_initial.png",
#     "results_screenshot": "tmp/k12_results_screenshot_small.png"
# }

if submitted:
    with st.spinner("Analyzing website"):
        id = site_url.split(".")[1]
        state = asyncio.run(navigate_website(site_url, id, headless))
        st.header(f"🔍😎 Analysis of {state['website']}")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏠 Main pag")
            with st.container(height=350):
                st.image(state["main_screenshot"], width=550)

        with col2:
            st.subheader("📋 Summar")
            with st.container(height=350):
                st.write(state["content"])

        # Restructure the features dictionary to have one row per feature
        features_data = [
            {"Feature": key, "Value": value} for key, value in state["features"].items()
        ]

        df = pd.DataFrame(features_data)

        # Apply conditional formatting with lighter shades of red and green
        def highlight_rows(row):
            if row["Value"] is True:
                return ["background-color: lightgreen"] * len(row)
            elif row["Value"] is False:
                return ["background-color: lightsalmon"] * len(row)
            else:
                return [""] * len(row)

        # Set the width of the table
        table_width = 500  # Adjust as needed

        styled_df = df.style.apply(highlight_rows, axis=1)

        with col1:
            st.subheader("🚀 Search Result")
            with st.container(height=350):
                st.image(state["results_screenshot"], width=500)

        with col2:
            st.subheader("✅ Current search features")
            with st.container(height=350):
                # Display the styled DataFrame
                st.dataframe(styled_df, height=300, width=table_width)

    with st.spinner("Generating multimedia"):
        audio_prompt = get_audio_prompt(state)
        get_audio(audio_prompt)

        if os.path.exists("./tmp/audio.wav"):
            st.subheader("📞 Listen the cold call")
            st.markdown(
                f"👇🏻 Just send this cold message to the **{state['company_name']}** representative and prepare for the meeting"
            )
            audio_file = open("./tmp/audio.wav", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav")
            st.markdown(f"***Transcript:*** *{audio_prompt}*")

    with st.spinner("Generating slides"):
        # Text
        while True:
            try:
                text_prompt = get_text_prompt(state)
                ai_data = get_analysis(text_prompt, "GPT-3_5-turbo")

                ai_json_data = json.loads(ai_data.replace("'", '"'))

                break
            except json.JSONDecodeError as e:
                print(f"Error de decodificación JSON: {e}")
                print("Intentando de nuevo...")

        # Images
        image_state_path = get_image(ai_json_data["current_state_text"])
        image_conclusion_path = get_image(ai_json_data["conclusion"])

        images_path_arr = [
            image_state_path,
            image_conclusion_path,
            state["main_screenshot"],
            state["results_screenshot"],
        ]

        images_url_arr = []

        for index, image_path in enumerate(images_path_arr):
            image_url = upload_file_to_drive(
                "image_" + str(index) + ".png",
                image_path,
                "image/png",
                "1zbX95IyVbxQO3ynhUqp0EjG5SEDq8LEE",
            )

            images_url_arr.append(image_url)

        requests_arr = get_requests_arr(
            json_data=state,
            ai_json_data=ai_json_data,
            images_url_arr=images_url_arr,
        )

        new_slides = dup_slide(
            slides_id="14LonsLtskFIBW-unrhO6Olq3EU08oi_o-Ciie0mchXk",
            slides_name=f"delete-{state['company_name']}",
            folder_id="15sY21eZwH8ycxHFzfAQZucbL7W5obdYm",
        )

        replace_slides_elements(reqs=requests_arr, new_slides_id=new_slides.get("id"))

        slides_url = "https://docs.google.com/presentation/d/" + new_slides.get("id")
        st.subheader(f"🔥 Your customized sales deck for {state['company_name']}")
        st.write("Your deck is ready! 🎉, let's close the deal")
        st.link_button(
            "👀 Go to deck", slides_url, use_container_width=True, type="primary"
        )
