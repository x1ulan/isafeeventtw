from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
url = 'https://isafeevent.moe.edu.tw'
username = 'EDU_SSO_USERNAME'
password = 'EDU_SSO_PASSWORD'
timeout = 0.5
ans = [2,4,1,3,3,2,4,1,4,4,2,4,3,4,3,2]


def login(username, password):
    driver.get(url + '/cloudoauth/authenticate/')
    namebox = driver.find_element(By.NAME, 'user')
    pswdbox = driver.find_element(By.NAME, 'pwd')
    captcha = driver.find_element(By.NAME, 'captchatext')

    namebox.send_keys(username)
    pswdbox.send_keys(password)

    while len(captcha.get_attribute('value')) < 3:
        time.sleep(timeout)

    captcha.send_keys(Keys.RETURN)

def action():
    driver.get(url)
    time.sleep(timeout)
    startbtn1 = driver.find_element(By.CLASS_NAME, 'btn.rounded-pill.px-5.btn-green.shadow')
    startbtn1.send_keys(Keys.ENTER)
    startbtn2 = driver.find_element(By.CLASS_NAME, 'btnStartExam')
    startbtn2.send_keys(Keys.ENTER)
    time.sleep(timeout)
    for i in range(1,17):
        obj = driver.find_element(By.ID, f'q_{i}_5')
        driver.execute_script("arguments[0].click();", obj)
    submitbtn1 = driver.find_element(By.CLASS_NAME, 'btnSendExam')
    submitbtn1.send_keys(Keys.ENTER)
    time.sleep(timeout)
    for i in range(1, 17):
        obj = driver.find_element(By.ID, f'q_{i}_{ans[i-1]}')
        driver.execute_script("arguments[0].click();", obj)
    submitbtn2 = driver.find_element(By.CLASS_NAME, 'btnSendExam')
    submitbtn2.send_keys(Keys.ENTER)

def main():
    login(username, password)
    time.sleep(timeout*3)
    for i in range(150):
        action()
        time.sleep(timeout*3)
    
main()