import os
import uuid

import streamlit as st
from clarifai.client.model import Model
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
PAT = os.environ["CLARIFAI_PAT"]


def get_analysis(prompt, model):
    try:
        inference_params = dict(temperature=0.2)

        model_prediction = Model(
            f"https://clarifai.com/openai/chat-completion/models/{model}"
        ).predict_by_bytes(
            prompt.encode(), input_type="text", inference_params=inference_params
        )

        print("Analysis generated!")

        return model_prediction.outputs[0].data.text.raw
    except Exception as e:
        print("Error getting analysis: " + e)


def get_image(prompt):
    try:
        inference_params = dict(quality="standard", size="1024x1024")

        model_prediction = Model(
            "https://clarifai.com/openai/dall-e/models/dall-e-3"
        ).predict_by_bytes(
            prompt.encode(), input_type="text", inference_params=inference_params
        )

        output_base64 = model_prediction.outputs[0].data.image.base64

        directory = "tmp"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = "image_" + str(uuid.uuid4()) + ".png"
        path = os.path.join(directory, filename)

        with open(path, "wb") as f:
            f.write(output_base64)

        print("Image generated!")

        return path
    except Exception as e:
        print("Error getting image: " + e)


def get_audio(prompt):
    try:
        USER_ID = "openai"
        APP_ID = "tts"
        MODEL_ID = "openai-tts-1"

        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (("authorization", "Key " + PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(text=resources_pb2.Text(raw=prompt))
                    )
                ],
            ),
            metadata=metadata,
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception(
                "Post model outputs failed, status: "
                + post_model_outputs_response.status.description
            )

        output_base64 = post_model_outputs_response.outputs[0].data.audio.base64

        directory = "tmp"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"{directory}/audio.wav", "wb") as f:
            f.write(output_base64)

        print("Audio generated!")

    except Exception as e:
        print("Error getting audio: " + e)
