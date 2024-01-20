from datetime import datetime


def get_current_date():
    current_date = datetime.now()
    return current_date.strftime("%Y-%m-%d")


def get_yes_or_no(affirmation):
    if affirmation == True:
        return "YES"

    if affirmation == False:
        return "NO"


def get_requests_arr(ai_json_data, json_data):
    ### FIRST SLIDE ###
    company_name = {
        "replaceAllText": {
            "containsText": {"text": "{{COMPANY_NAME}}"},
            "replaceText": json_data["website"],
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

    table_autocomplete = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_AUTOCOMPLETE}}"},
            "replaceText": get_yes_or_no(json_data["features"]["autocomplete"]),
        }
    }

    table_typo_tolerance = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_TYPO_TOLERANCE}}"},
            "replaceText": get_yes_or_no(json_data["features"]["typo_tolerance"]),
        }
    }

    table_title_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_TITLE_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["title_search"]),
        }
    }

    table_desc_search = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_DESC_SEARCH}}"},
            "replaceText": get_yes_or_no(json_data["features"]["desc_search"]),
        }
    }

    table_highlighting = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_HIGHLIGHT}}"},
            "replaceText": get_yes_or_no(json_data["features"]["highlighting"]),
        }
    }

    table_thumbnails = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_THUMBNAIL}}"},
            "replaceText": get_yes_or_no(json_data["features"]["thumbnails"]),
        }
    }

    table_filters = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_FILTERS}}"},
            "replaceText": get_yes_or_no(json_data["features"]["filters"]),
        }
    }

    table_sorting = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_SORT}}"},
            "replaceText": get_yes_or_no(json_data["features"]["sorting"]),
        }
    }

    table_pagination = {
        "replaceAllText": {
            "containsText": {"text": "{{TABLE_PAGINATION}}"},
            "replaceText": get_yes_or_no(json_data["features"]["pagination"]),
        }
    }

    ### FIFTH SLIDE ###
    conclusion = {
        "replaceAllText": {
            "containsText": {"text": "{{CONCLUSION}}"},
            "replaceText": ai_json_data["conclusion"],
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
        conclusion,
        table_search,
        table_autocomplete,
        table_typo_tolerance,
        table_title_search,
        table_desc_search,
        table_highlighting,
        table_thumbnails,
        table_filters,
        table_sorting,
        table_pagination,
    ]


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
