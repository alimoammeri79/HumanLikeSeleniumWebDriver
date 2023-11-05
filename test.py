import time
import random
import pathlib
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class HumanLikeWebDriverOptions(webdriver.ChromeOptions):
    """Options to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self, proxy=None):
        super().__init__()
        self.add_argument("start-maximized")
        self.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.add_experimental_option('useAutomationExtension', False)
        if proxy is not None:
            self.add_argument(f'--proxy-server={proxy}')

        # creating a user-data profile
        script_directory = pathlib.Path().absolute()
        # self.add_argument(f"user-data-dir={script_directory}\\userdata")

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,]
        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        self.add_argument(f'user-agent={user_agent}')


class HumanLikeWebDriver(webdriver.Chrome):
    """A customized driver to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self, proxy=None) -> None:
        self.options = HumanLikeWebDriverOptions(proxy)
        super(HumanLikeWebDriver, self).__init__(options=self.options)
        # using selenium_stealth library
        stealth(self,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.action_chains = ActionChains(self)

    # def get(url):
    #     try:
    #         super.get(url)
    #     except WebDriverException:
    #         print("page down")

    def delay(self):
        # Introduce random delays between 1 to 3 seconds
        delay = random.uniform(1, 5)
        time.sleep(delay)

    def send_keys(self, element, text):
        """ Introduce small random delays between typing each character to mimick human behavior"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.08, 0.12))

    def scroll(self, count=1, direction=1):
        """Random single scrolling like human users"""

        current_scroll_position = self.execute_script(
            "return window.pageYOffset")

        for i in range(0, count):
            scroll_height = self.execute_script(
                "return document.body.scrollHeight")
            scroll_increment = random.randint(
                # Random scroll increment based on scroll direction (up or down)
                200, 800) * direction
            next_scroll = min(current_scroll_position +
                              scroll_increment, scroll_height)
            current_scroll_position = next_scroll

            self.execute_script(f"window.scrollTo(0, {next_scroll})")
            self.delay()

    def click(self, element):
        """Simulate human-like click on random links"""
        self.execute_script("arguments[0].scrollIntoView();", element)
        self.delay()
        self.execute_script("arguments[0].click();", element)
        self.delay()


def click_on_random_link(driver: webdriver):
    # Find all anchor elements on the page
    links = driver.find_elements(By.CSS_SELECTOR, "body a")

    # Select a random link from the list
    random_link = random.choice(links)
    driver.click(random_link)


def search_google(driver: HumanLikeWebDriver, query: str):
    human_like_driver.get("https://google.com?hl=gb")
    human_like_driver.delay()
    # check for google accept cookie policy prompt
    try:
        accpet_btn = driver.find_element(
            By.XPATH, '//button/div[text()="Accept all"]')
        accpet_btn.click()
        human_like_driver.delay()
    except NoSuchElementException:
        pass

    # find searchbar
    search_bar = driver.find_element(By.NAME, "q")
    # search google for given search query
    driver.send_keys(search_bar, query)
    driver.delay()
    # hit enter
    search_bar.send_keys(Keys.RETURN)

# url = "https://www.yellowpages.com.sg/listing-category/home-office/cleaning-services-tools/cleaning-services/"
# test_url = "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
# url = "https://www.charkhoneh.com/"
# url = "https://bot.incolumitas.com/"
# "https://antcpt.com/score_detector/"


if __name__ == "__main__":
    url = "https://blog.faradars.org/python-programming-language/"
    search_query = "پایتون"
    proxy = "127.0.0.1:5444"

    human_like_driver = HumanLikeWebDriver(proxy)
    # human_like_driver = HumanLikeWebDriver()
    human_like_driver.implicitly_wait(5)

    search_google(human_like_driver, search_query)
    human_like_driver.delay()
    human_like_driver.scroll(5)
    human_like_driver.delay()
    human_like_driver.click(human_like_driver.find_element(
        By.CSS_SELECTOR, f'a[href="{url}"]'))

    human_like_driver.delay()
    human_like_driver.scroll(3)
    human_like_driver.delay()
    human_like_driver.scroll(1, -1)
    human_like_driver.scroll(2)
    human_like_driver.delay()
    click_on_random_link(human_like_driver)
    human_like_driver.scroll(3)
    time.sleep(3)
    human_like_driver.quit()

# mouse movement
