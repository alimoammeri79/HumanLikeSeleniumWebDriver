import re
import time
import random
import pathlib
from urllib.parse import urlparse
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HumanLikeWebDriverOptions(webdriver.ChromeOptions):
    """Options to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self, proxy=None):
        super().__init__()
        self.add_argument("start-maximized")
        self.add_argument('--disable-blink-features=AutomationControlled')
        self.add_argument("--disable-extensions")
        self.add_experimental_option('useAutomationExtension', False)
        self.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        if proxy is not None:
            self.add_argument(f'--proxy-server={proxy}')
        # self.add_argument('--headless')

        # creating a user-data profile
        script_directory = pathlib.Path().absolute()

        # if pathlib.Path(script_directory).is_dir():
        #     pathlib.Path(script_directory).rmdir()

        self.add_argument(f"user-data-dir={script_directory}\\userdata")

        user_agent = UserAgent(browsers=["chrome"], os="windows")
        u = user_agent.getRandom
        self.add_argument(f'user-agent={u}')


class HumanLikeWebDriver(webdriver.Chrome):
    """A customized driver to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self, proxy=None) -> None:
        self.options = HumanLikeWebDriverOptions(proxy)
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        super(HumanLikeWebDriver, self).__init__(
            options=self.options, desired_capabilities=caps)
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
        self.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # def get(url):
    #     try:
    #         super.get(url)
    #     except WebDriverException:
    #         print("page down")

    def delay(self, min=1, max=5):
        # Introduce random delays between 1 to 5 seconds
        delay = random.uniform(min, max)
        print(f"delay: {delay}")
        self.action_chains.pause(delay).perform()

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
        self.action_chains.scroll_to_element(
            element).pause(random.uniform(1, 3))
        self.action_chains.move_to_element(
            element).pause(random.uniform(0.5, 2))
        self.action_chains.click_and_hold().pause(
            random.uniform(0.09, 1)).release()
        try:
            self.action_chains.perform()
        except ElementNotInteractableException:
            pass


def click_on_random_link(driver: HumanLikeWebDriver):
    print("Click on random link")
    # Find all anchor elements on the page
    links = driver.find_elements(By.CSS_SELECTOR, "body a")

    # Select a random link from the list
    random_link = random.choice(links)
    print(f'clicking on: {random_link.get_attribute("href")}')
    try:
        driver.click(random_link)
        driver.delay(5, 10)
    except TimeoutException:
        pass
    driver.back()


def random_scroll(driver: HumanLikeWebDriver):
    print("Random scroll")
    direction = random.choice([1, -1])
    count = random.randint(1, 5)
    driver.scroll(count, direction)


def stay(driver: HumanLikeWebDriver):
    driver.delay(5, 10)


def do_random_action(driver: HumanLikeWebDriver):
    actions = [random_scroll, click_on_random_link, stay]
    random.choice(actions)(driver)


def search_google(driver: HumanLikeWebDriver, query: str) -> bool:
    query = query.replace('+', ' ')

    depth = 20
    try:
        human_like_driver.get(
            "https://google.com/search?q={q}&hl=en-GB&num={d}&sourceid=chrome&ie=UTF-8".format(q=query, d=depth))
    except WebDriverException:
        return False

    human_like_driver.delay(1, 3)

    # check for google accept cookie policy prompt
    try:
        accpet_btn = driver.find_element(
            By.XPATH, '//button/div[text()="Accept all"]')
        accpet_btn.click()
        human_like_driver.delay(1, 2)
    except NoSuchElementException:
        pass

    return True


def extract_url_keywords(url: str):
    host_name = urlparse(url).hostname
    host_name = host_name.split('.')[0:-1]
    host_name = " ".join(host_name)
    host_name = host_name.replace("-", " ")
    return host_name


def get_random_intervals(total_sum: int) -> list:
    a = 0
    b = random.randint(a, total_sum)
    c = random.randint(b, total_sum)
    d = random.randint(c, total_sum)
    e = random.randint(d, total_sum)

    return [0, b, c, d, e, total_sum]


if __name__ == "__main__":
    page_url = r"https://git.ir/udemy-build-a-data-analysis-library-from-scratch-in-python/"
    query = "دوره کتابخانه تحلیل داده پایتون"
    proxy = "socks5://127.0.0.1:5443"
    view_time_in_seconds = 60
    repeat_amount = 2

    intervals = get_random_intervals(view_time_in_seconds)

    query_helper_prefix = extract_url_keywords(page_url)
    search_query = query_helper_prefix + " " + query

    for i in range(0, repeat_amount):
        human_like_driver = HumanLikeWebDriver(proxy)

        if not search_google(human_like_driver, search_query):
            print("Connection Error: can't connect to google.")
            human_like_driver.quit()
            exit(1)

        human_like_driver.delay()
        do_random_action(human_like_driver)
        human_like_driver.delay(0.5, 1.5)
        do_random_action(human_like_driver)
        human_like_driver.delay(0.5, 1)
        do_random_action(human_like_driver)

        try:
            e = human_like_driver.find_element(
                By.CSS_SELECTOR, f"a[href='{page_url}']")
            print(e.get_attribute("href"))
            human_like_driver.click(e)
            human_like_driver.delay(view_time_in_seconds, view_time_in_seconds)
        except NoSuchElementException:
            print("can't find given url in search results")
            human_like_driver.quit()
            exit(1)

        except TimeoutError:
            pass

        do_random_action(human_like_driver)
        do_random_action(human_like_driver)
        human_like_driver.delay(0.1, 0.5)
        do_random_action(human_like_driver)
        do_random_action(human_like_driver)
        human_like_driver.delay(0.5, 1.5)
        do_random_action(human_like_driver)
        human_like_driver.delay(0.5, 1)
        do_random_action(human_like_driver)

        human_like_driver.quit()
        time.sleep(random.uniform(5, 10))
