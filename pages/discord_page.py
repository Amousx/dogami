import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

from selenium.webdriver.support import expected_conditions as EC
import time

JOIN_CSS_SELECTOR = "username"
DISCORD_JOIN_CSS_SELECTOR = 'div.centeringWrapper-dGnJPQ button'


class DiscordPage(BasePage):

    # MARK: - Init

    def __init__(self, browser):
        super().__init__(browser)

        self.browser.switch_to_window(-1)
        self.wait_until_found(
            By.NAME, JOIN_CSS_SELECTOR,
            timeout=5
        )

    # MARK: - Public methods
    def open_discord_login_page(self):
        links = self.__discord_login_links()

        self.browser.action_on_first_interactable(links, action_name='click')

    def login(self, token):
        fuction = f'let token = \'{token}\';' + '''function login(token) {
                     setInterval(() => {
                       document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                     }, 50);
                     setTimeout(() => {
                       location.reload();
                     }, 2500);
                     }
                     login(token);'''
        self.browser.driver.execute_script(fuction)
        time.sleep(3)
        print("discord login success")

    def click_join(self):
        join_btns = self.__join_btns()
        self.wait_until_found(
            By.CSS_SELECTOR, DISCORD_JOIN_CSS_SELECTOR,
            timeout=10
        )

        self.browser.action_on_first_interactable(
            join_btns,
            action_name='click'
        )
        window_handle_list = self.browser.get_window_handle()
        if len(window_handle_list) == 2:
            self.browser.driver.close()

    def __discord_login_links(self):
        return self.browser \
            .driver \
            .find_elements_by_css_selector(DISCORD_LOGIN_CSS_SELECTOR)

    def __join_btns(self):
        self.wait_until_found(
            By.CSS_SELECTOR, DISCORD_JOIN_CSS_SELECTOR,
            timeout=100
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(DISCORD_JOIN_CSS_SELECTOR)
