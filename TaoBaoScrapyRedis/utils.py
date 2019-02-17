from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random


def register():
    USER = "西南大爷"
    PASSWORD = "lyh1995"
    # 用于登陆淘宝，并且保存Cookies
    browser = webdriver.Chrome()
    # 淘宝对selenium的识别主要是通过navigator.webdriver,使用selenium的浏览器api显示的是True，所有我们改成FALSE就可以过淘宝的检测
    browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
    browser.get('https://login.taobao.com/member/login.jhtml')
    try:
        #browser.switch_to.frame(1)
        wait = WebDriverWait(browser, 10)
        input = wait.until(EC.presence_of_element_located((By.ID, 'J_Quick2Static')))
        input.click() # 切换到密码登陆
    except Exception as e:
        print("直接输入登陆")
    # 切换到支付宝登陆
    # ali = browser.find_element(By.CLASS_NAME, 'alipay-login')
    # ali.click()
    # aliloggoin = browser.find_element(By.CSS_SELECTOR, '#J-loginMethod-tabs > li:nth-child(2)')
    # aliloggoin.click()
    uesr = browser.find_element(By.ID, 'TPL_username_1')  # 账号输入框
    password = browser.find_element(By.ID, 'TPL_password_1')  # 密码输入框
    uesr.send_keys(USER)  # 输入密码
    time.sleep(random.random() * 2)  # 暂停
    password.send_keys(PASSWORD)  # 输入账号
    time.sleep(random.random() * 2)  # 暂停
    try:
        browser.switch_to.frame(browser.find_element(By.ID, '_oid_ifr_'))
        browser.switch_to.default_content()
        # 滑块出现
        loggin = browser.find_element(By.ID, 'nc_1_n1z')
        action = ActionChains(browser)
        action.click_and_hold(loggin).perform()
        action.reset_actions()
        action.move_by_offset(285, 0).perform()  # 输入账号密码后会有一个滑动验证
        time.sleep(random.random() * 1)
    except Exception as e:
        print("滑动滑块")
    button = browser.find_element(By.ID, 'J_SubmitStatic')  # 登录按钮
    button.click()
    time.sleep(random.random() * 2)
    cookie = browser.get_cookies()
    list = {}  # scrapy携带的cookies需要字典类型的
    for cookiez in cookie:
        name = cookiez['name']
        value = cookiez['value']
        list[name] = value
        if len(list) > 10:
            break
    else:
        browser.close()

    return browser, list


def loggoin():
    temp = input("请输入验证码：")
    return temp

