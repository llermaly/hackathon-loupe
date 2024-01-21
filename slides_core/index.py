import json
import time

from .ai_requests import get_analysis, get_audio, get_image
from .google_requests import dup_slide, replace_slides_elements, upload_file_to_drive
from .utils import get_json_data, get_requests_arr


def get_slides_url(json_data, model):
    text_prompt = (
        "Based on the following information corresponding to the content of a web page:"
        + json_data["content"]
        + ", analyze the web page based on the text, which will have the following sections:\n\nIntroduction: An introduction of 200 to 300 words summarizing the content that will follow.\nCurrent State: What do you consider the current state of the page or product to be?\nProblems: What problems can you detect with the product or page? These problems should be in list form.\nConclusion: Brief conclusions about the page or product. \n\nProvide me with the following information in the JSON format: \n\n { 'intro_text': 'content','current_state_text': 'content','problems': ['problem1', 'problem2', 'problem3'],'conclusion': 'content'} \n\n The JSON format is absolutely necessary to respect its structure; The JSON format must be compatible with Python programming language; you must fill in each and every one of the required fields and the answers must be only the json data."
    )

    while True:
        try:
            start_time = time.time()

            ai_data = get_analysis(text_prompt, model)

            end_time = time.time()
            execution_time = end_time - start_time
            print("Web page analysis completed successfully!")
            print(f"Execute time: {execution_time} seconds")

            print(ai_data)

            ai_json_data = json.loads(ai_data.replace("'", '"'))

            break
        except json.JSONDecodeError as e:
            print(f"Error de decodificación JSON: {e}")
            print("Intentando de nuevo...")

    start_time = time.time()

    get_audio(
        "Hello "
        + json_data["company_name"]
        + ", after thoroughly analyzing your website, we've uncovered some information that may be of great interest to you. I've attached a detailed report for your review. Please take a moment to go through it. If you have any questions or would like further clarification, feel free to give me a call. Looking forward to discussing this with you. Thanks!"
    )

    end_time = time.time()
    execution_time = end_time - start_time
    print("Audio file generated successfully!")
    print(f"Execute time: {execution_time} seconds")

    start_time = time.time()

    get_image(json_data["content"])

    end_time = time.time()
    execution_time = end_time - start_time
    print("Image file generated successfully!")
    print(f"Execute time: {execution_time} seconds")

    image_url = upload_file_to_drive(
        "image.png", "tmp/image.png", "image/png", "1zbX95IyVbxQO3ynhUqp0EjG5SEDq8LEE"
    )

    print("Image file uploaded successfully!")

    requests_arr = get_requests_arr(
        json_data=json_data, ai_json_data=ai_json_data, image_url=image_url
    )

    new_slides = dup_slide(
        slides_id="14LonsLtskFIBW-unrhO6Olq3EU08oi_o-Ciie0mchXk",
        slides_name=f'delete-{json_data["company_name"]}',
        folder_id="15sY21eZwH8ycxHFzfAQZucbL7W5obdYm",
    )

    replace_slides_elements(reqs=requests_arr, new_slides_id=new_slides.get("id"))

    print("https://docs.google.com/presentation/d/" + new_slides.get("id"))

    return "https://docs.google.com/presentation/d/" + new_slides.get("id")
