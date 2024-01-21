import streamlit as st
from playwright.async_api import async_playwright
from tarsier import Tarsier, GoogleVisionOCRService
from core.navigation.llm import send_message, gen_element_finder_prompt, gen_inference_params, results_questions, json_schema
import json


async def navigate_website(url: str, id: str):
    ocr_service = GoogleVisionOCRService(st.secrets['gcp_service_account'])
    tarsier = Tarsier(ocr_service)
    tag_to_xpath = {}
    saved_screenshots = {}
    state = {}

    state['website'] = url
    state['id'] = id

    # TODO: Build function to extract logo
    state['logo'] = "https://www.k12.com/wp-content/themes/pl-scaffold-theme/dist/images/logo_new.svg"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def extract_content() -> str:
            """
            Use to read the current state of the page
            """
            text, _ = await tarsier.page_to_text(page)
            return text

        async def read_page() -> str:
            """
            Use to read the current state of the page
            """
            screenshot, inner_tag_to_xpath = await tarsier.page_to_image(page)
            tag_to_xpath.clear()
            tag_to_xpath.update(inner_tag_to_xpath)
            return screenshot

        async def click(element_id: int) -> str:
            """
            Click on an element based on element_id and return the new page state
            """
            x_path = tag_to_xpath[element_id]
            element = page.locator(x_path)
            await element.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            await element.click()
            await page.wait_for_timeout(2000)
            return await read_page()

        async def type_text(element_id: int, text: str, screenshot_name: str = "type_text") -> str:
            """
            Input text into a textbox based on element_id and return the new page state
            """
            x_path = tag_to_xpath[element_id]
            await page.locator(x_path).press_sequentially(text)
            await page.wait_for_timeout(3000)
            await take_screenshot(screenshot_name, full_page=False)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)
            return await read_page()

        async def take_screenshot(name: str, full_page=True) -> str:
            """
            Take a screenshot of the current page
            """
            path = f"tmp/{name}.png"
            screenshot = await page.screenshot(path=path, full_page=full_page)
            saved_screenshots[name] = path
            print("Saved screenshot")
            print(path)
            return screenshot

        await page.goto(url)

        # Extract content
        content = await extract_content()
        summary = send_message(
            f"Summarize this website content please: {content}", dict())

        # Take initial screenshot
        initial_state = await read_page()
        with open(f'tmp/{id}.png', 'wb') as file:
            file.write(initial_state)

        # Save intial_state screenshot to a file

        await take_screenshot(f"{id}_initial", full_page=False)

        # Find and click icon

        find_icon = send_message(gen_element_finder_prompt(
            "based on the image, which red box with white text is on top of the magnifier glass?", json_schema), gen_inference_params(initial_state))
        element = json.loads(find_icon.text.replace(
            "```", "").replace("json", ""))
        print("Icon found")
        print(element)

        # Find and click search bar

        bar_state = await click(int(element['element_id'].replace("@", "")))

        find_bar = send_message(gen_element_finder_prompt(
            "You must find the search bar and give me the element id", json_schema), gen_inference_params(bar_state))
        bar_element = json.loads(
            find_bar.text.replace("```", "").replace("json", ""))
        print("Bar found")
        print(bar_element)

        # Type in search bar

        await type_text(int(bar_element['element_id'].replace("#", "")), id, f"{id}_autocomplete")

        # Evaluate autocomplete

        with open(saved_screenshots[f'{id}_autocomplete'], 'rb') as file:
            image_bytes = file.read()

        autocomplete_response = send_message("Based on the image, are autocomplete suggestions displayed? answer with YES or NO, nothing else or additional text.",
                                             gen_inference_params(image_bytes))

        print(autocomplete_response)

        # Evaluate search results

        results_screenshot = await take_screenshot(f"{id}_results")
        await take_screenshot(f"{id}_results_screenshot_small", full_page=False)

        find_results = send_message(
            results_questions, gen_inference_params(results_screenshot))

        results_json = json.loads(
            find_results.text.replace("```", "").replace("json", ""))

        print(results_json)

        await browser.close()

        state['features'] = results_json
        state['content'] = summary.text

        if autocomplete_response.text == "YES":
            state['features']['autocomplete'] = True
        else:
            state['features']['autocomplete'] = False

        state['main_screenshot'] = saved_screenshots[f'{id}_initial']
        state['results_screenshot'] = saved_screenshots[f'{id}_results_screenshot_small']
        print(state)
        return state

# url = "https://www.k12.com"
# id = url.replace(".com", "").replace("https://", "").replace("www.", "")
# asyncio.run(navigate_website(
#     url, id, "davinci", "test"))
