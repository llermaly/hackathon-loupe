import json

from google.oauth2 import service_account

from slides_core.ai_requests import get_analysis, get_audio, get_image
from slides_core.slides import dup_slide, replace_slides_elements
from slides_core.utils import get_json_data, get_requests_arr


def main():
    json_data = get_json_data()

    text_prompt = (
        "Based on the following information corresponding to the content of a web page:"
        + json_data["content"]
        + ", analyze the web page based on the text, which will have the following sections:\n\nIntroduction: An introduction of 200 to 300 words summarizing the content that will follow.\nCurrent State: What do you consider the current state of the page or product to be?\nProblems: What problems can you detect with the product or page? These problems should be in list form.\nConclusion: Brief conclusions about the page or product. \n\nProvide me with the following information in the JSON format: \n\n { 'intro_text': 'content','current_state_text': 'content','problems': ['problem1', 'problem2', 'problem3'],'conclusion': 'content'} \n\n The JSON format is absolutely necessary to respect its structure; The JSON format must be compatible with Python programming language; you must fill in each and every one of the required fields and the answers must be only the json data."
    )

    get_audio(
        "Hello "
        + json_data["website"]
        + ", after thoroughly analyzing your website, we've uncovered some information that may be of great interest to you. I've attached a detailed report for your review. Please take a moment to go through it. If you have any questions or would like further clarification, feel free to give me a call. Looking forward to discussing this with you. Thanks!"
    )

    get_image(json_data["content"])

    while True:
        try:
            ai_data = get_analysis(text_prompt)

            print(ai_data)

            ai_json_data = json.loads(ai_data.replace("'", '"'))

            break
        except json.JSONDecodeError as e:
            print(f"Error de decodificación JSON: {e}")
            print("Intentando de nuevo...")

    ### TEST_DATA ###
    # ai_json_data = {
    #     "intro_text": "This web page is dedicated to showcasing a variety of great knives. The content that follows will delve into the specifics of these knives, their unique features, and their potential uses. We aim to provide comprehensive information to help visitors make informed decisions about their knife purchases.",
    #     "current_state_text": "The current state of the page seems to be in its initial stages, focusing primarily on the promotion of great knives. The product appears to be of high quality, catering to a wide range of needs from kitchen use to outdoor activities.",
    #     "problems": [
    #         "Lack of detailed product descriptions",
    #         "Absence of customer reviews",
    #         "No information about the manufacturing process",
    #     ],
    #     "conclusion": "While the web page does a good job of promoting a variety of great knives, it could benefit from more detailed product descriptions, customer reviews, and information about the manufacturing process to enhance customer trust and satisfaction.",
    # }

    requests_arr = get_requests_arr(json_data=json_data, ai_json_data=ai_json_data)

    new_slides = dup_slide(
        slides_id="1Xjy7tjh8S5ap3TDOy33ZW8j2BNRnbPJwlbl0Lyc8KMM",
        slides_name="delete-this-slides",
        folder_id="15sY21eZwH8ycxHFzfAQZucbL7W5obdYm",
    )
    ### TEST_DATA ###
    # new_slides = {"id": "1U-Abl_ngAduSX-GqL9rUTffhTNVe3R-iH2j0MH_Al3o"}

    replace_slides_elements(reqs=requests_arr, new_slides_id=new_slides.get("id"))


if __name__ == "__main__":
    main()
