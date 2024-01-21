from llama_index.llms.clarifai import Clarifai
from core.navigation.utils import encode_and_resize

TEXT_MODEL = "https://clarifai.com/openai/chat-completion/models/gpt-4-turbo"
VISION_MODEL = "https://clarifai.com/openai/chat-completion/models/gpt-4-vision"

json_schema = """
    {
        "type": "bar",
        "element_id": "@2"
    }
    """

features_schema = """
{
        "search": true,
        "description": false,
        "highlighting": true,
        "thumbnails": false,
        "filters": false,
        "sorting": false,
        "pagination": false
    }
"""


def gen_element_finder_prompt(instruction: str, json_schema: str):
    return f"""You are a search engine evaluator.
    You were provided with a screenshot of the current state of a website.
    Element ids are texts on red boxes to identify the elements.
    I need you to tell me which element id to select now based on the instructions:
    hint: The magnifying glass icon is commonly used to represent a search function
    hint: Element ids can only contain numbers and $ , # , or @ symbols. NOT letters.

    {instruction} 

    You must answer using JSON and following this schema: {json_schema}.
    ONLY return a valid JSON object (no other text is necessary)
    Remember the only valid values for type property are bar, icon, or none.
    Do not invent more properties.
"""


results_questions = f""" 
Based on the image, answer the following questions only answering true or false.

Do the search results have a search bar?
Do the search results have description after the title (this doesn't count the URL)?   
Do the search results have highlighting based on the search term?
Do the search results have thumbnails?
Do the search results have filters?
Do the search results have sorting?
Do the search results have pagination? 

Use JSON to answer the questions, following this schema: 

{features_schema}

ONLY return a valid JSON object (no other text is necessary)
"""


def gen_inference_params(img):
    """
    Generate inference params for the LLM, prepare image for gpt-vision
    """
    base64image = encode_and_resize(img)

    inference_params = dict(temperature=0.1,
                            image_base64=base64image)
    return inference_params


def send_message(prompt: str, inference_params, model_url=VISION_MODEL):
    """
    Send a instruction to the chatbot and return the response
    """

    llm_model = Clarifai(
        model_url=model_url)

    llm_response = llm_model.complete(
        prompt=prompt,
        inference_params=inference_params
    )
    return llm_response
