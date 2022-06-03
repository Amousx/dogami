import time

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import traceback

RESOURCE_NAME = 'gleam.io'
USERNAME_OR_EMAIL_FIELD_ID = 'username_or_email'
PASSWORD_FIELD_ID = 'password'
PHONE_NUMBER_INPUT_ID = 'challenge_response'
MAIL_FIELD_NAME = 'text'

TWITTER_VATH_CSS_SELECTOR = 'input.Button.EdgeButton'

TWITTER_AUTH_XPATH = '/html/body/div[2]/div/form/fieldset/input[1]'


class TwitterLoginPage(BasePage):

    # MARK: - Init

    def __init__(self, browser):
        super().__init__(browser)

        self.browser.switch_to_window(-1)
        self.wait_until_found(By.ID, USERNAME_OR_EMAIL_FIELD_ID)

    # MARK: - Public methods

    def submit_credentials(self, credentials):
        username_field = self.__username_field()
        password_field = self.__password_field()

        username_field.send_keys(credentials['login'])
        password_field.send_keys(credentials['password'])
        password_field.send_keys(Keys.RETURN)
        button_list = self.__auth__button()
        self.browser.action_on_first_interactable(button_list, action_name='click')
        res = 0
        if not self.browser.wait_until_current_window_closed():
            time.sleep(2)
            if self.browser.driver.find_elements_by_name(MAIL_FIELD_NAME):
                self.__submit__username(credentials['login'])
                WebDriverWait(self.browser.driver, 20).until(
                    EC.presence_of_element_located((By.NAME, PASSWORD_FIELD_ID)))
                self.__submit__pwd(credentials['password'])

                res = 1
            elif "Login Complete" in self.browser.driver.page_source:
                self.browser.driver.close()
                res = 2
            else:
                self.__submit_phone_number(credentials['phone_number'])
                time.sleep(2)
                self.__auth__button2().send_keys(Keys.RETURN)
        self.browser.switch_to_window(0)
        return res

    def authoriazation(self):
        self.browser.switch_to_window(2)
        auth_button2 = self.__auth__button2()
        auth_button2.send_keys(Keys.RETURN)
        self.browser.switch_to_window(0)

    # MARK: - Private methods

    def __submit__username(self, login_mail):
        mail_field = self.__mail_field()
        mail_field[0].send_keys(login_mail)
        mail_field[0].send_keys(Keys.RETURN)

    def __submit__pwd(self, pwd):
        pwd_field = self.__pwd_field()
        pwd_field[0].send_keys(pwd)
        pwd_field[0].send_keys(Keys.RETURN)

    def __submit_phone_number(self, phone_number):
        phone_number_field = self.__phone_number_field()

        phone_number_field.send_keys(phone_number)
        phone_number_field.send_keys(Keys.RETURN)


    def __mail_field(self):
        return self.browser \
            .driver \
            .find_elements_by_name(MAIL_FIELD_NAME)

    def __pwd_field(self):
        return self.browser \
            .driver \
            .find_elements_by_name(PASSWORD_FIELD_ID)

    def __auth__button(self):
        return self.browser \
            .driver \
            .find_elements_by_css_selector(TWITTER_VATH_CSS_SELECTOR)

    # def __start__button(self):
    #     self.wait_until_found(
    #         By.XPATH, TWITTER_START_XPATH,
    #         timeout=10
    #     )
    #     return self.browser \
    #         .driver \
    #         .find_element_by_xpath(TWITTER_START_XPATH)
    #
    # def __continue__button(self):
    #     self.wait_until_found(
    #         By.XPATH, TWITTER_CONTINUE_XPATH,
    #         timeout=10
    #     )
    #     return self.browser \
    #         .driver \
    #         .find_element_by_xpath(TWITTER_CONTINUE_XPATH)

    def __auth__button2(self):
        self.wait_until_found(
            By.XPATH, TWITTER_AUTH_XPATH,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_element_by_xpath(TWITTER_AUTH_XPATH)

    def __username_field(self):
        return self.browser \
            .driver \
            .find_element_by_id(USERNAME_OR_EMAIL_FIELD_ID)

    def __password_field(self):
        return self.browser \
            .driver \
            .find_element_by_id(PASSWORD_FIELD_ID)

    def __phone_number_field(self):
        try:
            return self.browser \
                .driver \
                .find_element_by_id(PHONE_NUMBER_INPUT_ID)
        except exceptions.NoSuchElementException:
            return None

