import os
from email.policy import default
import traceback
from multiprocessing import Process
from browser import Browser
from pages.gleam_io_page import GleamIoPage
from pages.twitter_login_page import TwitterLoginPage
from pages.twitter_page import TwitterPage
from pages.discord_page import DiscordPage
from selenium.webdriver.common.by import By
from pages.discord_auth_page import DiscordAuthPage
import time
import json
import random

REFERAL_LINK = 'https://gleam.io/XTUFh/last-chance-mint-'
ACCOUNTS_FILE_PATH = 'accounts_new3.txt'
RESULT_FILE_PATH = 'result.txt'
DISCORD_LOGIN_FLAG = False

DIS_ADDRESS = '//*[@id="em6482985"]'
DIS_INPUT_XPATH = '//*[@id="em6482985Details"]'
DIS_CONTINUE = '//*[@id="em6482985"]/div/div/form/div[2]/div/a'

WALLET_ADDRESS = '//*[@id="em6482986"]'
WALLET_INPUT_XPATH = '//*[@id="em6482986Details"]'
WALLET_CONTINUE = '//*[@id="em6482986"]/div/div/form/div[2]/div/a'


def complete_twitter_task(user_info):
    token = user_info['discord_token']

    browser = Browser()
    browser.start()
    res = ""
    browser.get_url(REFERAL_LINK)
    try:
        gleam_io_page = GleamIoPage(browser)
    except:
        browser.stop()
        complete_twitter_task(user_info)

    try:
        gleam_io_page.open_twitter_login_page()

        twitter_login_page = TwitterLoginPage(browser)

        status = twitter_login_page.submit_credentials(user_info)
        if status:
            gleam_io_page.open_twitter_login_page()
            twitter_login_page = TwitterLoginPage(browser)
            twitter_login_page.submit_credentials(user_info)
            print("twitter login success")

        email_fil = browser.\
            driver.\
            find_elements(
                By.CSS_SELECTOR,
                "input.ng-empty.ng-valid-email.ng-invalid.ng-invalid-required.ng-valid-pattern.ng-dirty.ng-touched"
                )
        if len(email_fil) == 1:
            email_fil[0].clear()
            email_fil[0].send_keys(user_info['mail'])
            continue_btn = browser.\
                driver.\
                find_element(
                    By.XPATH,
                    "/html/body/div/div/div/div[1]/div/div/div[1]/div[5]/div[2]/div[2]/div/form/div/span[1]/button"
                )
            continue_btn.click()
    except:
        res += "twitter_login_failed\t"
        return

    try:
        wallet_ele = browser.driver.find_element(By.XPATH, WALLET_ADDRESS)
        wallet_input_ele = browser.driver.find_element(By.XPATH, WALLET_INPUT_XPATH)
        gleam_io_page.fill_text(wallet_ele, wallet_input_ele, user_info['xtz_address'])
        wallet_complete_ele = browser.driver.find_element(By.XPATH, WALLET_CONTINUE)
        gleam_io_page.mark_task_as_completed(wallet_complete_ele)
        time.sleep(2)
    except:
        res += "address_wrong\t"
    try:
        dis_ele = browser.driver.find_element(By.XPATH, DIS_ADDRESS)
        dis_input_ele = browser.driver.find_element(By.XPATH, DIS_INPUT_XPATH)
        gleam_io_page.fill_text(dis_ele, dis_input_ele, user_info['dcname'])
        dis_complete_ele = browser.driver.find_element(By.XPATH, DIS_CONTINUE)
        gleam_io_page.mark_task_as_completed(dis_complete_ele)
        time.sleep(2)
    except:
        res += "address_wrong\t"



    browser.stop()
    return res


def flight_mode_on():
    command1 = "adb shell settings put global airplane_mode_on 1"
    command2 = "adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true"

    os.system(command1)
    os.system(command2)
    print("flight_mode_on")


def flight_mode_off():
    command1 = "adb shell settings put global airplane_mode_on 0"
    command2 = "adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false"

    os.system(command1)
    os.system(command2)
    print("关闭飞行模式")


def process(userinfo, num):
    login, password, phone_number, bsc_address, discord_token, mail, pwd ,xtz_address,dcname= userinfo.split(',')
    dcname = str(pwd).replace("\n", "")
    result_num_path = './result' + str(num) + '.txt'

    status = complete_twitter_task({
        'login': login,
        'password': password,
        'phone_number': phone_number,
        'bsc_address': bsc_address,
        'discord_token': discord_token,
        'mail': mail,
        'pwd': pwd,
        'xtz_address': xtz_address,
        'dcname' :dcname,
    })
    if status != "":
        with open(result_num_path, 'a') as result:
            result.write(f"failed : {status}\t")

    with open(result_num_path, 'a') as result:
        result.write(login)
        result.write("\n")


def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


if __name__ == '__main__':
    n = 0
    batch_flag = False
    with open(ACCOUNTS_FILE_PATH, 'r',encoding='utf-8') as file:
        userinfos = file.readlines()
        while n < len(userinfos):
            process(userinfos[n], 1)
            n += 1
