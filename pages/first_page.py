import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2
import time
import pandas as pd

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)


# This must be within the display() function.
#auth = ClarifaiAuthHelper.from_streamlit(st)
#stub = create_stub(auth)
#userDataObject = auth.get_user_app_id_proto()

# Remove form border and padding styles
css = r"""
    <style>
        [data-testid="stForm"] {border: 0px;padding:0px}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("New analysis")

with st.form(key="analysis"):
    site_url = st.text_input(
        "Site URL", value="https://samples.clarifai.com/metro-north.jpg"
    )
    submitted = st.form_submit_button("Generate Report")

if submitted:
    with st.spinner("Extracting logo from site..."):
        time.sleep(3)
        st.image("./logo.png")
        st.write(site_url)

    with st.spinner("Generating site summary..."):
        time.sleep(3)
        st.image("./site.png", width=500)
        st.subheader("Site summary")
        st.write(
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque at ipsum vitae mi vestibulum convallis. Fusce scelerisque faucibus tellus a porta. Proin gravida, est vitae suscipit sodales, erat libero auctor quam, non porta mi urna eu risus. Maecenas est libero, vehicula laoreet massa eu, condimentum lobortis orci. Phasellus quam orci, accumsan vitae condimentum et, accumsan vel lectus. Aliquam non vulputate nisi, quis mattis odio. Nulla facilisi. Donec quis pellentesque neque. Curabitur sed maximus tortor, nec pulvinar nulla. Integer id odio blandit, elementum ex ac, efficitur nulla."""
        )

    with st.spinner("Analyzing current state..."):
        time.sleep(3)
        st.image("./site.png", width=500)
        st.subheader("Current state")
        st.write(
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque at ipsum vitae mi vestibulum convallis. Fusce scelerisque faucibus tellus a porta. Proin gravida, est vitae suscipit sodales, erat libero auctor quam, non porta mi urna eu risus. Maecenas est libero, vehicula laoreet massa eu, condimentum lobortis orci. Phasellus quam orci, accumsan vitae condimentum et, accumsan vel lectus. Aliquam non vulputate nisi, quis mattis odio. Nulla facilisi. Donec quis pellentesque neque. Curabitur sed maximus tortor, nec pulvinar nulla. Integer id odio blandit, elementum ex ac, efficitur nulla."""
        )

    with st.spinner("Generating results..."):
        time.sleep(3)
        df = pd.DataFrame(
            columns=["Item", "Pass"],
            data=[
                ["Item 1", "Yes"],
                ["Item 2", "Yes"],
                ["Item 3", "No"],
                ["Item 4", "No"],
            ],
        )
        st.subheader("Analysis results")
        st.table(df)

        st.subheader("Listen to cold call")
        st.audio("./audio.mp3", format="audio/wav", start_time=0, sample_rate=None)
        st.button("Download deck")
