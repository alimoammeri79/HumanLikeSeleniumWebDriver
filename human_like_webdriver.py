from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random


class HumanLikeWebDriverOptions(webdriver.ChromeOptions):
    """Options to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self):
        super().__init__()
        self.add_argument("start-maximized")
        self.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.add_experimental_option('useAutomationExtension', False)


class HumanLikeDriver(webdriver.Chrome):
    """A customized driver to mimic human behavior and avoid bot detection as much as possible."""

    def __init__(self) -> None:
        self.options = HumanLikeWebDriverOptions()
        super(HumanLikeDriver, self).__init__(options=self.options)
        # using selenium_stealth library
        stealth(self,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    # def set_proxy(self, proxy):
    #     PROXY = "127.0.0.1:10809"
    #     self.options.add_argument(f'--proxy-server={PROXY}')

    def delay(self):
        # Introduce random delays between 1 to 3 seconds
        delay = random.uniform(1, 3)
        time.sleep(delay)

    def send_keys(self, element, text):
        """ Introduce small random delays between typing each character to mimick human behavior"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 3))

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


if __name__ == "__main__":
    human_like_driver = HumanLikeDriver()
    human_like_driver.get("https://bot.incolumitas.com/")
    time.sleep(2)
    human_like_driver.scroll(7)
    human_like_driver.scroll(4, -1)
    time.sleep(1)
    human_like_driver.quit()
