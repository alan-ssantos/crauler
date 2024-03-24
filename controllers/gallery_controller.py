from adapters.chrome_web_driver import ChromeWebDriver
from selenium.common.exceptions import TimeoutException, InvalidSelectorException

from utils.file_handler import get_image


def get_gallery_images(
    chrome_driver: ChromeWebDriver,
    selector: str,
    category_id: int,
    product_id: int,
    page_slug: str,
    page_cover: str,
    save_folder: str,
):
    try:
        if not selector:
            raise InvalidSelectorException

        page_gallery = chrome_driver.find_elements(selector)
        page_gallery.pop(0)

        print(f"Images on gallery: {len(page_gallery)}")
        if len(page_gallery) == 0:
            images = [page_cover]
        else:
            images = []

        for image in page_gallery:
            images.append(image.get_attribute("href").strip())

        gallery_query = ""
        if len(images) > 0:
            for i in range(len(images)):
                current_image = get_image(images[i], page_slug, save_folder)
                if current_image:
                    gallery_query += f"INSERT INTO app_gallery (user_empresa, cat_parent,gallery_rel, gallery_file) VALUES (2, {category_id}, {product_id}, '{current_image}');\n"

        return gallery_query
    except InvalidSelectorException:
        print("Gallery not found (Invalid Selector)")
    except TimeoutException:
        print("Gallery not found (Timeout Exception)")
    except Exception as exception:
        print(f"Gallery not found, An unexpected error occurred: {exception}")
