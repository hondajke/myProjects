from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time
import requests
import base64
from fake_useragent import UserAgent
import binascii as ba

def get_captcha(img_base64 ,capKey):
    url = 'https://rucaptcha.com/in.php'
    params = dict(key=capKey, method='base64', body=img_base64, json=1)
    res = requests.post(url, params)
    #print(res.content)
    captcha = ''
    url = 'https://rucaptcha.com/res.php'
    params = dict(key=capKey, action='get', id=res.json()['request'], json=1)
    while True:
        time.sleep(1)
        res = requests.get(url, params)
        if int(res.json()['status']) == 1:
            # тут делать, что нужно, т.е. повторно отправлять запрос с решенной капчей
            # решенная капча в res.json()['request']
            #print(res.content)
            captcha = res.json()['request']
            break
        elif res.json()['status'] != '1':
            continue
        else:
            #print('ERROR')
            #print(res.json())
            break
    url = 'https://lk.rosreestr.ru/account-back/captcha/' + captcha
    res = requests.get(url, verify=False)
    #print(res)
    return captcha

ua = UserAgent()
user_agent = ua.random
op = webdriver.ChromeOptions()
op.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=op)
response = browser.get('https://lk-dealer.tricolor.tv/#Login')
try:
    WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input-field")))
    inputLogin = browser.find_element_by_id('login')
    inputLogin.send_keys('3840')
    inputPassword = browser.find_element_by_id('password')
    inputPassword.send_keys('vadim2305')
    inputPassword.send_keys(Keys.ENTER)
    try:
        WebDriverWait(browser, 4).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".captcha-row")))
        l = browser.find_element_by_xpath('//*[@class="capcha"]')
        images_url = l.get_attribute("src")
        temp = images_url.rfind('base64,')
        #response = requests.get(images_url[temp+7:])
        #print(images_url)
        captcha = get_captcha(images_url[temp+7:], '16fcf3724f4397a9518df1a0badb93b1')
        print(captcha)
        inputCaptcha = browser.find_element_by_xpath('//*[@id="capcha-input"]')
        inputCaptcha.send_keys(captcha)
        inputCaptcha.send_keys(Keys.ENTER)
    except:
        print('error')
    try:
        WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nav")))     
        browser.get('https://lk-dealer.tricolor.tv/#Demands')
        #WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button"))).click()
        WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s2id_autogen17']"))).click()
        WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'На подтверждении')]"))).click()
        WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s2id_autogen3']"))).click()
        search_input = browser.find_element_by_xpath('//*[@id="s2id_autogen4_search"]')
        search_input.send_keys('Кабардино-Балкарская')
        WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Кабардино-Балкарская')]"))).click()
        while True:
            WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='btn ladda-button btn-primary btn-sm btn-find btn-bold offset-top-small pull-right']"))).click()
            try:
                WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Принять в работу"]'))).click()
                #bet_fa.clear()
                #bet_fa.send_keys(d1)
                try:
                    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='CaptchaBlock']")))
                    bet_fa = WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='form-control planDateInput']"))) #WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="form-control planDateInput"]'))).click()
                    #print(bet_fa)
                    #bet_fa.clear()
                    #bet_fa.click()
                    today = datetime.today()
                    d1 = today.strftime("%d.%m.%Y")
                    temp_data = d1.split('.')
                    print(d1)
                    final_day = int(temp_data[0]) - 1
                    final_month = int(temp_data[1]) + 1
                    final_data = str(final_day) + '.' + str(final_month) + '.' + temp_data[2]
                    bet_fa.send_keys(final_data)
                    comment = WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@class='comment']")))
                    comment.send_keys('Принята в работу')
                    image_elements = browser.find_elements_by_xpath("//div[@id='CaptchaBlock']")
                    image_el = browser.find_elements_by_xpath("//img[@class='capcha']")[-1]
                    images_url = image_el.get_attribute("src")
                    temp = images_url.rfind('base64,')
                    captcha = get_captcha(images_url[temp+7:], '16fcf3724f4397a9518df1a0badb93b1')
                    print(captcha)
                    inputCaptcha = browser.find_element_by_xpath('//*[@id="captchaValue"]')
                    inputCaptcha.send_keys(captcha)
                    WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Принять в работу')]"))).click()
                except:
                    print('error')
                continue
            except:
                print('Не найдена принять в работу')
            #WebDriverWait(browser, 86400).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='.reply-button']"))).click()
    except:
        print('Не найдена кнопка')
finally:
    browser.quit()
