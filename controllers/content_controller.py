import re
from datetime import datetime
from selenium.common.exceptions import TimeoutException

from adapters.chrome_web_driver import ChromeWebDriver
from utils.content_handler import content_images, format_date


def get_page_cover(chrome_driver: ChromeWebDriver, selector: str) -> str:
    try:
        page_cover = chrome_driver.find_element(selector).get_attribute("src").strip()

        # Remover os parâmetros de consulta na URL
        page_cover = re.sub(r"\?.*", "", page_cover)
    except TimeoutException:
        page_cover = "https://producao.mpitemporario.com.br/sig_site_base_full_beta/doutor/images/default.png"
        print("Cover not found (TimeoutException)")
    except Exception as exception:
        page_cover = "https://producao.mpitemporario.com.br/sig_site_base_full_beta/doutor/images/default.png"
        print(f"An unexpected error occurred: {exception}")

    return page_cover


def get_page_title(chrome_driver: ChromeWebDriver, selector: str) -> str:
    try:
        page_title = chrome_driver.find_element(selector).get_attribute("innerText").strip()
    except TimeoutException:
        print("Title not found (TimeoutException)")
    except Exception as exception:
        print(f"Title not found, an unexpected error occurred: {exception}")

    return page_title


def get_old_price(chrome_driver: ChromeWebDriver, selector: str) -> str:
    try:
        old_price = chrome_driver.find_element(selector).get_attribute("innerText").strip()
        old_price = str.replace(old_price, "R$ ", "")
        old_price = float(str.replace(old_price, ",", "."))
    except TimeoutException:
        print("Old price not found (TimeoutException)")
    except Exception as exception:
        print(f"Old price not found, an unexpected error occurred: {exception}")

    return old_price


def get_price(chrome_driver: ChromeWebDriver, selector: str) -> str:
    try:
        new_price = chrome_driver.find_element(selector).get_attribute("innerText").strip()
        new_price = str.replace(new_price, "R$ ", "")
        new_price = float(str.replace(new_price, ",", "."))
    except TimeoutException:
        print("Price not found (TimeoutException)")
    except Exception as exception:
        print(f"Price not found, an unexpected error occurred: {exception}")

    return new_price


def get_page_category(chrome_driver: ChromeWebDriver, categories: list[str], selector: str, step: int = 2):
    try:
        category = chrome_driver.find_element(selector).get_attribute("innerText").strip()
        category_id = categories.index(category) + step
    except TimeoutException:
        print("Category not found (TimeoutException)")
    except Exception as exception:
        print(f"Category not found, an unexpected error occurred: {exception}")

    return category_id


def get_publish_date(chrome_driver: ChromeWebDriver, selector: str | None = None, separator: str = "/") -> str:
    try:
        if not selector:
            now = datetime.now()
            publish_date = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            publish_date = chrome_driver.find_element(selector).get_attribute("innerText").strip()
            publish_date = publish_date.split(separator)
            publish_date = format_date(publish_date[2], publish_date[1], publish_date[0])
    except TimeoutException:
        print("Publish date not found (TimeoutException)")
    except Exception as exception:
        print(f"Publish date not found, an unexpected error occurred: {exception}")

    return publish_date


def get_page_content(chrome_driver: ChromeWebDriver, selector: str, page_slug: str, images_folder: str) -> str:
    try:
        page_content = chrome_driver.find_elements(selector)

        content_elements = []
        for image_element in page_content:
            content_elements.append(image_element.get_attribute("outerHTML"))

        page_content = "".join(content_elements)

        post_images = []
        image_elements = re.findall(r"<img\s+[^>]*>", page_content)

        for image_element in image_elements:
            source_match = re.search(r'src\s*=\s*["\'](.*?)["\']', image_element)
            if source_match:
                source = source_match.group(1)
                post_images.append(source)

        page_content = (
            page_content if not post_images else content_images(page_content, post_images, page_slug, images_folder)
        )
    except TimeoutException:
        print("Page content not found (TimeoutException)")
    except Exception as exception:
        print(f"Page content not found, an unexpected error occurred: {exception}")

    return page_content


def get_page_short_description(chrome_driver: ChromeWebDriver, selector: str) -> str:
    try:
        short_description = chrome_driver.find_elements(selector)

        content_elements = []
        for element in short_description:
            content_elements.append(element.get_attribute("outerHTML"))

        short_description = "".join(content_elements)
    except TimeoutException:
        print("Short description not found (TimeoutException)")
    except Exception as exception:
        print(f"Short description not found, an unexpected error occurred: {exception}")

    return short_description
