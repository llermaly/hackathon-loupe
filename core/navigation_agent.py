import streamlit as st
from playwright.async_api import async_playwright
from tarsier import Tarsier, GoogleVisionOCRService
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_index.tools import FunctionTool

async def navigate_website(url: str, id: str, model: str, prompt: str):
    ocr_service = GoogleVisionOCRService(st.secrets['gcp_service_account'])
    tarsier = Tarsier(ocr_service)
    tag_to_xpath = {}
    saved_screenshots = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def read_page() -> str:
            """
            Use to read the current state of the page
            """
            page_text, inner_tag_to_xpath = await tarsier.page_to_text(page)
            tag_to_xpath.clear()
            tag_to_xpath.update(inner_tag_to_xpath)
            return page_text

        read_page_tool = FunctionTool.from_defaults(
            fn=read_page, async_fn=read_page)

        async def click(element_id: int) -> str:
            """
            Click on an element based on element_id and return the new page state
            """
            x_path = tag_to_xpath[element_id]
            print(x_path)
            element = page.locator(x_path)
            await element.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            await element.click()
            await page.wait_for_timeout(2000)
            return await read_page()

        click_tool = FunctionTool.from_defaults(fn=click, async_fn=click)

        async def type_text(element_id: int, text: str) -> str:
            """
            Input text into a textbox based on element_id and return the new page state
            """
            x_path = tag_to_xpath[element_id]
            print(x_path)
            await page.locator(x_path).press_sequentially(text)
            return await read_page()

        type_text_tool = FunctionTool.from_defaults(
            fn=type_text, async_fn=type_text)

        async def press_key(key: str) -> str:
            """
            Press a key on the keyboard and return the new page state
            """
            await page.keyboard.press(key)
            await page.wait_for_timeout(2000)
            return await read_page()

        press_key_tool = FunctionTool.from_defaults(
            fn=press_key, async_fn=press_key)

        async def take_screenshot(name: str) -> str:
            """
            Take a screenshot of the current page
            """
            path = path = f"data/{id}/screenshots/{name}.png"
            await page.screenshot(path=path)
            saved_screenshots[name] = path
            return

        take_screenshot_tool = FunctionTool.from_defaults(
            fn=take_screenshot, async_fn=take_screenshot)

        llm = OpenAI(model=model)
        tarsier_agent = OpenAIAgent.from_tools(
            [read_page_tool, click_tool, type_text_tool,
                press_key_tool, take_screenshot_tool],
            llm=llm,
            verbose=True,
            system_prompt="You are a web interaction agent. Start first by using the read page tool to understand where you currently are. You will be passed in OCR text of a web page where element ids are to the left of elements.",
        )

        await page.goto(url)
        await tarsier_agent.achat(prompt)
        await browser.close()

        return saved_screenshots
