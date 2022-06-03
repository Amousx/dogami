import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys

AUTH_BUTTON = "//button[contains(., '授权')]"


class DiscordAuthPage(BasePage):

    # MARK: - Init

    def __init__(self, browser):
        super().__init__(browser)

        self.browser.switch_to_window(-1)

    def click_auth_btns(self):
        auth_btns = self.__auth_btns()
        auth_btns.send_keys(Keys.RETURN)
        self.browser.switch_to_window(0)


    def __auth_btns(self):
        self.wait_until_found(
            By.XPATH, AUTH_BUTTON,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_element_by_xpath(AUTH_BUTTON)
