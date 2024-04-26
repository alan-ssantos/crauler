from adapters.chrome_web_driver import ChromeWebDriver
from utils.file_handler import get_file
from utils.slug import slug
from selenium.common.exceptions import TimeoutException, InvalidSelectorException


def get_downloads(
    chrome_driver: ChromeWebDriver,
    selector: str,
    user_id: int,
    current_download_id: int,
    download_category_id: int,
    downloads_folder: str,
    page_title: str,
    publish_date: str,
):
    try:
        download_list = []

        file_elements = chrome_driver.find_elements(selector)
        file_urls = []

        for file in file_elements:
            file_urls.append(file.get_attribute("href").strip())

        downloads_query = ""
        if len(file_urls) > 0:
            for url in range(len(file_urls)):
                current_file = get_file(file_urls[url], slug(page_title), user_id, downloads_folder)
                if current_file:
                    current_download_id += 1
                    download_list.append(current_download_id)
                    downloads_query += f"""INSERT INTO `dr_downloads` (`dow_id`,`user_empresa`,`cat_parent`,`dow_name`,`dow_title`,`dow_description`,`dow_file`,`dow_date`,`dow_status`) VALUES ({current_download_id}, {user_id}, {download_category_id}, '{slug('Manual: '+page_title)}','{'Manual: '+page_title}','{'Manual: '+page_title}','{current_file}','{publish_date}',2);\n"""

        download_list_str = ",".join(map(str, download_list))
        return downloads_query, current_download_id, download_list_str
    except InvalidSelectorException:
        print("Downloads not found (Invalid Selector)")
    except TimeoutException:
        print("Downloads not found (Timeout Exception)")
    except Exception as exception:
        print(f"Downloads not found, an unexpected error occurred: {exception}")
