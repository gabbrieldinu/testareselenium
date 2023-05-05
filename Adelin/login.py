from selenium import webdriver
from selenium.common import ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

"""
   Descrierea testului:
       Pas 1 : Deschide browser pe site-ul emag
       Pas 2 : Apasa pe butonul "Contul meu"
       Pas 3 : Introdu in input de email "saftaadelin@gmail.com"
       Pas 4 : Apasa pe butonul de "continua"
       Pas 5 : Introdu in input de parola "ParolaTest11"
       Pas 6 : Apasa pe butonul de "continua"
       Pas 7 : Rezolvat CAPTCHA 
       Pas 8 : Apasa pe butonul de skip introducere numar telefon
       Pas 9 : Apasa pe butonul "Contul meu"
       Pas 10 : Verificat ca numele din cont este "Test Selenium"
       Pas 11 : Facut hover peste contul meu si apasat butonul logout
"""

LINK = "https://www.emag.ro/"
PATH = "C:\Program Files (x86)\chromedriver.exe"
EMAIL = "saftaadelin@gmail.com"
PASSWORD = "ParolaTest11"
ACCOUNT_BUTTON_ID = "my_account"
CONTINUE_BUTTON_ID = "user_login_continue"
LOGIN_EMAIL_ID = "user_login_email"
LOGIN_PASSWORD_ID = "user_login_password"
SKIP_PHONE_TEXT ="Activează mai târziu"
PROFILE_NAME_ELEMENT_CLASS = "js-personal-details-name"
LOGOUT_LINK = "Log out"
USER_NAME = "Test Selenium"

logsFile = open("logs.txt", "w")
logsFile.write("Started Selenium\n")

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get(LINK)


def test_content():
    try:
        account_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, ACCOUNT_BUTTON_ID)))
        account_button.click()
        login_email_input = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, LOGIN_EMAIL_ID)))
        login_email_input.clear()
        login_email_input.send_keys(EMAIL)
        continue_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, CONTINUE_BUTTON_ID)))
        continue_button.click()
        login_password_input = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, LOGIN_PASSWORD_ID)))
        login_password_input.clear()
        login_password_input.send_keys(PASSWORD)
        continue_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, CONTINUE_BUTTON_ID)))
        continue_button.click()
        try:
            skip_button = WebDriverWait(driver, timeout=20).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/a")))
            skip_button.click()
        except TimeoutException:
            pass
        account_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, ACCOUNT_BUTTON_ID)))
        account_button.click()
        name_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, PROFILE_NAME_ELEMENT_CLASS)))
        name_element_text = name_element.text
        account_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, ACCOUNT_BUTTON_ID)))
        hover = ActionChains(driver).move_to_element(account_button)
        hover.perform()
        logout_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, LOGOUT_LINK)))
        logout_button.click()
        if name_element_text == USER_NAME:
            logsFile.write("Login test finished successfully, stopping script....")
        else:
            logsFile.write("Login test failed, stopping script....")
        sleep(3)
    finally:
        driver.close()
        driver.quit()


test_content()

