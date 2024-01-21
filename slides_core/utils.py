from datetime import datetime


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


def get_requests_arr(ai_json_data, json_data, image_url):
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
            "imageUrl": json_data["logo"],
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
            "imageUrl": json_data["main_screenshot"],
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

    table_typo_tolerance = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_TYPO_TOLERANCE}}"},
            "replaceText": get_yes_or_no(json_data["features"]["typo_tolerance"]),
        }
    }

    point3 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["typo_tolerance"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT3}}"},
        }
    }

    table_title_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_TITLE_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["title_search"]),
        }
    }

    point4 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["title_search"]),
            "replaceMethod": "CENTER_INSIDE",
            "containsText": {"text": "{{POINT4}}"},
        }
    }

    table_desc_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_DESC_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["desc_search"]),
        }
    }

    point5 = {
        "replaceAllShapesWithImage": {
            "imageUrl": get_red_green(json_data["features"]["desc_search"]),
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
            "imageUrl": image_url,
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
        problem1,
        problem2,
        problem3,
        table_search,
        point1,
        table_autocomplete,
        point2,
        table_typo_tolerance,
        point3,
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


### METHOD FOR TESTING ###
def get_json_data():
    return {
        "company_name": "Clarifai",
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
