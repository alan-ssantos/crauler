from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeWebDriver:
    def __init__(self, headless=True, log_level=3):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--log-level={log_level}")

        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def find_element(self, selector: str, timeout: int = 10):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return element

    def find_elements(self, selector: str, timeout: int = 10):
        elements = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return elements

    def close(self):
        self.driver.quit()
