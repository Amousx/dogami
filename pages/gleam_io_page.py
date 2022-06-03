from importlib.metadata import entry_points
from os import link
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.discord_auth_page import DiscordAuthPage
from pages.discord_page import DiscordPage

TWITTER_LOGIN_CSS_SELECTOR = "a.twitter-background.popup-window"
FOLLOW_ON_TWITTER_CSS_SELECTOR = 'a.enter-link.twitter_follow-border'
TWITTER_FOLLOW_BTN_CSS_SELECTOR = 'div.entry_details span.twitter-label'
RETWEET_ON_TWITTER_CSS_SELECTOR = 'a.enter-link.twitter_retweet-border'
TWITTER_RETWEET_BTN_CSS_SELECTOR = 'a.xl.twitter-button'
JOIN_DISCORD_BTN_CSS_SELECTOR = 'a.btn.btn-info'
ADDRESS_CSS_SELECTOR = 'a.no-underline.enter-link.custom-border.custom_action-border.clearfix.default'
JOIN_IN_DISCORD_XPATH_SELECTOR = '//*[@id="em6403470"]'

BSC_ADDRESS_INPUT_NAME = 'data'
FIL_FULLNAME_EMAIL_NAME = 'email'
# AGREE_TO_TERMS = 'i_have_read_the_terms_and_conditions'

TASK_COMPLETED_LINK_SELECTOR = 'a.btn.btn-primary'
DISCORD_TASK_COMPLETED_LINK_SELECTOR = 'button.btn.btn-primary'
DISCORD_SAVE_XPATH = '/html/body/div/div/div/div/div/div/div[1]/div[5]/div[2]/div[3]/div/div[1]/div/div/form/div/span[1]/button'


class GleamIoPage(BasePage):

    # MARK: - Init

    def __init__(self, browser):
        super().__init__(browser)

        # FIXME: Doesn't work
        self.wait_until_found(By.CSS_SELECTOR, TWITTER_LOGIN_CSS_SELECTOR)

    # MARK: - Public methods

    def open_twitter_login_page(self):
        links = self.__twitter_login_links()

        self.browser.action_on_first_interactable(links, action_name='click')

    def open_discord_login_page(self):
        links = self.__twitter_login_links()

        self.browser.action_on_first_interactable(links, action_name='click')

    def click_join_in_dis_task(self,  join_ele, cnt_ele, token, login_flag):
        self.browser.action_on_interactable(
                join_ele,
                action_name='click'
            )
        try:
            discord_page = DiscordPage(self.browser)
            if not login_flag:
                discord_page.login(token)
            discord_page.click_join()
            self.browser.switch_to_window(0)
            self.browser.action_on_interactable(
                            cnt_ele,
                            action_name='click'
                        )
        except:
            return False
        return True

    def click_follow_on_twitter_task(self, pos1, pos2):
        links = self.__twitter_follow_links()
        self.browser.action_on_interactable(links[pos1], action_name='click')
        time.sleep(5)
        # self.browser.action_on_first_interactable(links, action_name='click')
        # self.__wait_until_follow_btn_appeared()
        # follow_btns = self.__follow_btns()
        # self.browser.action_on_first_interactable(
        # try:
        #     self.browser.action_on_interactable(
        #         follow_btns[pos2],
        #         action_name='click'
        #     )
        # except:
        #     print('任务已完成')

    def click_retweet_on_twitter_task(self, pos1, pos2):
        links = self.__twitter_retweet_links()

        self.browser.action_on_interactable(links[pos1], action_name='click')
        # try:
        #     self.browser.driver.switch_to.alert.accept()
        # except:
        #     pass
        # time.sleep(3)
        # # self.browser.action_on_first_interactable(links, action_name='click')
        # self.__wait_until_retweet_btn_appeared()
        # retweet_btns = self.__retweet_btns()
        # try:
        #     self.browser.action_on_interactable(
        #         retweet_btns[pos2],
        #         action_name='click'
        #     )
        # except:
        #     print('任务已完成')

    def mark_task_as_completed(self, pos_ele):
        self.browser.switch_to_window(0)
        self.browser.action_on_interactable(
            pos_ele,
            action_name='click'
        )

    def mark_discord_task_as_completed(self, pos):
        self.browser.switch_to_window(0)

        task_completed_links = self.__check_if_discord_task_completed_links()
        self.browser.action_on_interactable(
            task_completed_links[pos],
            action_name='click'
        )

    def click_save_button(self):
        discord_save = self.__save_discord_account()
        self.browser.action_on_interactable(
            discord_save[0],
            action_name='click'
        )

    def fill_text(self, add_ele, input_ele,text):
        self.browser.action_on_interactable(add_ele, action_name='click')
        input_ele.clear()
        input_ele.send_keys(text)

    # MARK: - Private methods

    def __wait_until_follow_btn_appeared(self):
        self.wait_until_found(By.CSS_SELECTOR, TWITTER_FOLLOW_BTN_CSS_SELECTOR)

    def __wait_until_retweet_btn_appeared(self):
        self.wait_until_found(By.CSS_SELECTOR, TWITTER_RETWEET_BTN_CSS_SELECTOR)

    def __wait_until_join_btn_appeared(self):
        self.wait.until_found(By.CSS_SELECTOR, JOIN_DISCORD_BTN_CSS_SELECTOR)

    def __twitter_login_links(self):
        self.wait_until_found(
            By.CSS_SELECTOR, TWITTER_LOGIN_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(TWITTER_LOGIN_CSS_SELECTOR)

    def __twitter_follow_links(self):
        self.wait_until_found(
            By.CSS_SELECTOR, FOLLOW_ON_TWITTER_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(FOLLOW_ON_TWITTER_CSS_SELECTOR)

    def __twitter_retweet_links(self):
        self.wait_until_found(
            By.CSS_SELECTOR, RETWEET_ON_TWITTER_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(RETWEET_ON_TWITTER_CSS_SELECTOR)

    def __discord_join_links(self):
        return self.browser \
            .driver \
            .find_elements_by_css_selector(JOIN_IN_DISCORD_XPATH_SELECTOR)

    def __bsc_address_link(self):
        self.wait_until_found(
            By.CSS_SELECTOR, ADDRESS_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_element_by_css_selector(ADDRESS_CSS_SELECTOR)

    def __bsc_address_input(self):
        return self.browser \
            .driver \
            .find_elements_by_name(BSC_ADDRESS_INPUT_NAME)

    def __follow_btns(self):
        self.wait_until_found(
            By.CSS_SELECTOR, TWITTER_FOLLOW_BTN_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(TWITTER_FOLLOW_BTN_CSS_SELECTOR)

    def __retweet_btns(self):
        self.wait_until_found(
            By.CSS_SELECTOR, TWITTER_RETWEET_BTN_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(TWITTER_RETWEET_BTN_CSS_SELECTOR)

    def __join_btns(self):
        self.wait_until_found(
            By.CSS_SELECTOR, JOIN_DISCORD_BTN_CSS_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(JOIN_DISCORD_BTN_CSS_SELECTOR)

    def __check_if_task_completed_links(self):
        self.wait_until_found(
            By.CSS_SELECTOR, TASK_COMPLETED_LINK_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(TASK_COMPLETED_LINK_SELECTOR)

    def __check_if_discord_task_completed_links(self):
        self.wait_until_found(
            By.CSS_SELECTOR, DISCORD_TASK_COMPLETED_LINK_SELECTOR,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_css_selector(DISCORD_TASK_COMPLETED_LINK_SELECTOR)

    def __save_discord_account(self):
        self.wait_until_found(
            By.XPATH, DISCORD_SAVE_XPATH,
            timeout=10
        )
        return self.browser \
            .driver \
            .find_elements_by_xpath(DISCORD_SAVE_XPATH)
