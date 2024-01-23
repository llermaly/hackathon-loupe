import os
from datetime import datetime

import cairosvg
import requests


def get_current_date():
    current_date = datetime.now()
    return current_date.strftime("%Y-%m-%d")


def get_yes_or_no(affirmation):
    if affirmation == True:
        return "YES"

    if affirmation == False:
        return "NO"


def get_red_green(affirmation):
    if affirmation == True:
        return "https://drive.google.com/uc?export=download&id=1sQrhETFfOoRtSt5DzkrcwJDhTIGsmY73"

    if affirmation == False:
        return "https://drive.google.com/uc?export=download&id=154tYFve8p8lhVOPkKN3_GEJ3Zha7Ai1e"


def get_requests_arr(ai_json_data, json_data, images_urls):
    ### FIRST SLIDE ###
    company_name = {
        "replaceAllText": {
            "containsText": {"text": "{{COMPANY_NAME}}"},
            "replaceText": json_data["company_name"],
        }
    }

    date = {
        "replaceAllText": {
            "containsText": {"text": "{{DATE}}"},
            "replaceText": get_current_date(),
        }
    }

    logo = {
        "replaceAllShapesWithImage": {
            "imageUrl": images_urls["logo_image"],
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{LOGO}}"},
        }
    }

    ### SECOND SLIDE ###
    intro_text = {
        "replaceAllText": {
            "containsText": {"text": "{{INTRO_TEXT}}"},
            "replaceText": ai_json_data["intro_text"],
        }
    }

    image_intro = {
        "replaceAllShapesWithImage": {
            "imageUrl": images_urls["results_screenshot"],
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{IMAGE_INTRO}}"},
        }
    }

    ### THIRD SLIDE ###
    current_state = {
        "replaceAllText": {
            "containsText": {"text": "{{CURRENT_STATE_TEXT}}"},
            "replaceText": ai_json_data["current_state_text"],
        }
    }

    image_state = {
        "replaceAllShapesWithImage": {
            "imageUrl": images_urls["current_state_image"],
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{IMAGE_STATE}}"},
        }
    }

    problem1 = {
        "replaceAllText": {
            "containsText": {"text": "{{PROBLEM1}}"},
            "replaceText": ai_json_data["problems"][0],
        }
    }

    problem2 = {
        "replaceAllText": {
            "containsText": {"text": "{{PROBLEM2}}"},
            "replaceText": ai_json_data["problems"][1],
        }
    }

    problem3 = {
        "replaceAllText": {
            "containsText": {"text": "{{PROBLEM3}}"},
            "replaceText": ai_json_data["problems"][2],
        }
    }

    ### FOURTH SLIDE ###
    table_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["search"]),
        }
    }

    point1 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["search"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT1}}"},
        }
    }

    table_autocomplete = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_AUTOCOMPLETE}}"},
            "replaceText": get_yes_or_no(json_data["features"]["autocomplete"]),
        }
    }

    point2 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["autocomplete"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT2}}"},
        }
    }

    # table_typo_tolerance = {
    #     "replaceAllText": {
    #         "containsText": {"text": "{{TABLE_TYPO_TOLERANCE}}"},
    #         "replaceText": get_yes_or_no(json_data["features"]["typo_tolerance"]),
    #     }
    # }

    # point3 = {
    #     "replaceAllShapesWithImage": {
    #         "imageUrl": get_red_green(json_data["features"]["typo_tolerance"]),
    #         "replaceMethod": "CENTER_INSIDE",
    #         "containsText": {"text": "{{POINT3}}"},
    #     }
    # }

    table_title_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_TITLE_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["search"]),
        }
    }

    point4 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["search"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT4}}"},
        }
    }

    table_desc_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_DESC_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["description"]),
        }
    }

    point5 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["description"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT5}}"},
        }
    }

    table_highlighting = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_HIGHLIGHT}}"},
            "replaceText": get_yes_or_no(json_data["features"]["highlighting"]),
        }
    }

    point6 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["highlighting"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT6}}"},
        }
    }

    table_thumbnails = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_THUMBNAIL}}"},
            "replaceText": get_yes_or_no(json_data["features"]["thumbnails"]),
        }
    }

    point7 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["thumbnails"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT7}}"},
        }
    }

    table_filters = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_FILTERS}}"},
            "replaceText": get_yes_or_no(json_data["features"]["filters"]),
        }
    }

    point8 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["filters"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT8}}"},
        }
    }

    table_sorting = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_SORT}}"},
            "replaceText": get_yes_or_no(json_data["features"]["sorting"]),
        }
    }

    point9 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["sorting"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT9}}"},
        }
    }

    table_pagination = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_PAGINATION}}"},
            "replaceText": get_yes_or_no(json_data["features"]["pagination"]),
        }
    }

    point10 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["pagination"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT10}}"},
        }
    }

    ### FIFTH SLIDE ###
    conclusion = {
        "replaceAllText": {
            "containsText": {"text": "{{CONCLUSION}}"},
            "replaceText": ai_json_data["conclusion"],
        }
    }

    image_conclusion = {
        "replaceAllShapesWithImage": {
            "imageUrl": images_urls["conclusion_image"],
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{IMAGE_CONCLUSION}}"},
        }
    }

    return [
        company_name,
        date,
        logo,
        intro_text,
        image_intro,
        current_state,
        image_state,
        problem1,
        problem2,
        problem3,
        table_search,
        point1,
        table_autocomplete,
        point2,
        # table_typo_tolerance,
        # point3,
        table_title_search,
        point4,
        table_desc_search,
        point5,
        table_highlighting,
        point6,
        table_thumbnails,
        point7,
        table_filters,
        point8,
        table_sorting,
        point9,
        table_pagination,
        point10,
        conclusion,
        image_conclusion,
    ]


def get_text_prompt_arr(json_data):
    aux = (
        "With the following information corresponding to the content of a web page:"
        + json_data["content"]
        + " Have search? "
        + str(json_data["features"]["search"])
        + " Have autocomplete? "
        + str(json_data["features"]["autocomplete"])
        + "Have description? "
        + str(json_data["features"]["description"])
        + "Have highlighting? "
        + str(json_data["features"]["highlighting"])
        + "Have thumbnails? "
        + str(json_data["features"]["thumbnails"])
        + "Have filters? "
        + str(json_data["features"]["filters"])
        + "Have sorting? "
        + str(json_data["features"]["sorting"])
        + "Have pagination? "
        + str(json_data["features"]["pagination"])
        + ", analyze the search bar of the web page based on the text. "
        + ", analyze the search bar of the web page based on the text. "
    )

    intro_text_prompt = (
        aux
        + " Give me an introduction of 75 to 100 words summarizing the content of the website."
    )

    current_state_text_prompt = (
        aux
        + " Does it have a search bar? If it does, what do you consider the current state of the search bar on the analyzed site? If it doesn't, report that it does not have a search bar."
    )

    problems_prompt = (
        aux
        + " What problems can you detect with the search bar if it exists? If it doesn't exist, also highlight the problems associated with not having one. These problems must be in python array form with 3 positions like this: ['problem1','problem2','problem3']. The response must be only the data on array format, please, don't include any other text."
    )

    conclusion_prompt = " Brief conclusions highlighting important analyzed elements about search bar. Should have 75 to 100 words."

    return [
        intro_text_prompt,
        current_state_text_prompt,
        problems_prompt,
        conclusion_prompt,
    ]


def get_audio_prompt(json_data):
    return (
        "Hello "
        + json_data["company_name"]
        + ", after thoroughly analyzing your website, we've uncovered some information that may be of great interest to you. I've attached a detailed report for your review. Please take a moment to go through it. If you have any questions or would like further clarification, feel free to give me a call. Looking forward to discussing this with you. Thanks!"
    )


def download_logo(url):
    try:
        response = requests.head(url)

        if response.status_code == 200:
            logo_type = response.headers.get("Content-Type", "").lower()

            if not os.path.exists("tmp"):
                os.makedirs("tmp")

            location_path = "tmp/client_logo.png"

            if "image/png" in logo_type:
                download_png_logo(url, location_path)

                return location_path
            elif "image/svg" in logo_type:
                download_svg_logo(url, location_path)

                return location_path
            else:
                print(f"Type of content no compatible {url}: {logo_type}")

                return None
        else:
            print(
                f"Cannot get type of content {url}. Status code: {response.status_code}"
            )
    except Exception as e:
        print(f"Request error: {e}")


def download_png_logo(url, location_path):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(location_path, "wb") as file:
                file.write(response.content)
                print("PNG logo downloaded")
        else:
            print(f"Cannot download logo. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PNG logo: {e}")


def download_svg_logo(url, location_path):
    try:
        cairosvg.svg2png(url=url, write_to=location_path)
        print("SVG logo downloaded and converted to PNG")
    except Exception as e:
        print(f"Error downloading or converting SVG logo to PNG: {e}")
