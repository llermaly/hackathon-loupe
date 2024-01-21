import asyncio
import json
import os

import streamlit as st

from core.slides.ai_requests import get_analysis, get_audio, get_image
from core.slides.google_requests import (
    dup_slide,
    replace_slides_elements,
    upload_file_to_drive,
)
from core.slides.utils import get_audio_prompt, get_requests_arr, get_text_prompt

st.title("Slides page")

url = "https://www.k12.com/"
id = url.replace("http://", "").replace("https://", "")

if os.path.exists("./tmp/audio.wav"):
    os.remove("./tmp/audio.wav")

# initial_json = """{
#     "company_name": "Clarifai",
#     "website": "https://clarifai.com",
#     "content": "The LLM/GENERATIVE AI/FULL STACK/COMPUTER VISION Build on the fastest, production-grade deep learning platform for developers and ML engineers.",
#     "logo": "https://img.freepik.com/psd-gratis/logo-gradiente-abstracto_23-2150689648.jpg?w=740&t=st=1705693169~exp=1705693769~hmac=d5aec7d0900982211c119cfeccea92257d2a92ea2b91aa8243ac85168fa77278",
#     "main_screenshot": "https://i.ytimg.com/vi/AKnpqlVJ0Wg/0.jpg",
#     "features": {
#         "search": true,
#         "typo_tolerance": false,
#         "title_search": false,
#         "desc_search": false,
#         "autocomplete": true,
#         "highlighting": true,
#         "thumbnails": false,
#         "filters": false,
#         "sorting": false,
#         "pagination": false
#     }
# }

# """


initial_json = {
    "website": "https://www.k12.com",
    "company_name": "k12",
    "logo": "https://www.k12.com/wp-content/themes/pl-scaffold-theme/dist/images/logo_new.svg",
    "content": "The website offers online education programs for children from kindergarten through career. It provides a flexible and personalized approach to learning, with options for virtual public schools, one-on-one tutoring, private elementary schools, and individual courses for homeschoolers. The programs are designed to be safe, fun, and challenging, with opportunities for students to participate in esports, join clubs, and access learning resources. The website also includes information for parents, career and college prep, and business education. Enrollment is open, and the website offers resources to help families get started.",
    "main_screenshot": "tmp/k12_initial.png",
    "results_screenshot": "tmp/k12_results_screenshot_small.png",
    "features": {
        "search": False,
        "description": False,
        "highlighting": False,
        "thumbnails": False,
        "filters": False,
        "sorting": False,
        "pagination": False,
        "autocomplete": False,
    },
}


# Create a form to receive user input
with st.form(key="my_form"):
    text_area_data = st.text_area("Enter JSON data:", initial_json, height=300)
    model = st.selectbox("Select your model", ("GPT-3_5-turbo", "GPT-4"))
    submitted = st.form_submit_button("Generate Report")

    if submitted:
        try:
            json_data = json.loads(text_area_data)
            st_success_aux = st.success("JSON data successfully loaded.")

        except json.JSONDecodeError:
            st.error("Error: Invalid JSON format. Please enter valid JSON data.")

        try:
            ### GETTING TEXT ###
            with st.spinner("Generating analysis..."):
                while True:
                    try:
                        text_prompt = get_text_prompt(json_data)
                        ai_data = get_analysis(text_prompt, model)

                        print(ai_data)

                        ai_json_data = json.loads(ai_data.replace("'", '"'))

                        break
                    except json.JSONDecodeError as e:
                        print(f"Error de decodificación JSON: {e}")
                        print("Intentando de nuevo...")

                st_success_aux.empty()
                st_success_aux = st.success("Analysis successfully generated.")

            ### GETTING AUDIO ###
            with st.spinner("Generating audio..."):
                audio_prompt = get_audio_prompt(json_data)
                get_audio(audio_prompt)

                st_success_aux.empty()
                st_success_aux = st.success("Audio successfully generated.")

            ### GETTING IMAGES ###
            with st.spinner("Generating images..."):
                image_state_path = get_image(ai_json_data["current_state_text"])
                image_conclusion_path = get_image(ai_json_data["conclusion"])

                images_path_arr = [image_state_path, image_conclusion_path]

                st_success_aux.empty()
                st_success_aux = st.success("Images successfully generated.")

            ### GENERATING SLIDES ###
            with st.spinner("Generating slides..."):
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
                    json_data=json_data,
                    ai_json_data=ai_json_data,
                    images_url_arr=images_url_arr,
                )

                new_slides = dup_slide(
                    slides_id="14LonsLtskFIBW-unrhO6Olq3EU08oi_o-Ciie0mchXk",
                    slides_name=f'delete-{json_data["company_name"]}',
                    folder_id="15sY21eZwH8ycxHFzfAQZucbL7W5obdYm",
                )

                replace_slides_elements(
                    reqs=requests_arr, new_slides_id=new_slides.get("id")
                )

                slides_url = "https://docs.google.com/presentation/d/" + new_slides.get(
                    "id"
                )

                st_success_aux.empty()
                st_success_aux = st.success("Slides successfully generated.")

                if os.path.exists("./tmp/audio.wav"):
                    st.header("First, listen the following audio:")
                    audio_file = open("./tmp/audio.wav", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/wav")

                st.header("Now, see the slides generated:")
                st.write(slides_url)

        except Exception as e:
            st.error("Error: Generating slides failed.")
