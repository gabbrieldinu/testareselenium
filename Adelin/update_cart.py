from selenium import webdriver
from selenium.common import ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

"""
   Descrierea testului:
       Pas 1 : Deschide browser pe site-ul emag
       Pas 2 : Apasa pe primul buton gasit "Adauga in cos"
       Pas 3 : Apasa pe butonul "Vezi detalii cos"
       Pas 4 : Verificare daca produsul se afla in cos o singura data
       Pas 5 : Apasa pe butonul de "+"
       Pas 6 : Intoarcere la ecranul principal
       Pas 7 : Apasa pe butonul "Cosul meu"
       Pas 8 : Verificare daca a fost incrementata cantitatea
"""

LINK = "https://www.emag.ro/"
PATH = "C:\Program Files (x86)\chromedriver.exe"
ADD_BUTTON_CLASS = "yeahIWantThisProduct"
SEE_CART_LINK = "Vezi detalii cos"
QUANTITY_CLASS = "qty-value"
INCREMENT_VALUE_BUTTON_CLASS = "qty-plus"
HOME_PAGE_CLASS = "navbar-brand"
MY_CART_ID = "my_cart"

logsFile = open("logs.txt", "w")
logsFile.write("Started Selenium\n")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get(LINK)
driver.maximize_window()


def test_content():
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, ADD_BUTTON_CLASS)))
        add_to_cart_button.click()
        see_cart_details_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, SEE_CART_LINK)))
        see_cart_details_button.click()
        quantity_value = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, QUANTITY_CLASS)))
        quantity_values = driver.find_elements(By.CLASS_NAME, QUANTITY_CLASS)
        quantity_value_text = ''
        for element in quantity_values:
            if element.is_displayed():
                quantity_value_text = element.get_attribute("innerHTML")
        if quantity_value_text != '1':
            logsFile.write("Update cart test failed (more than one product added by one click), stopping script....")
            return

        increment_quantity_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, INCREMENT_VALUE_BUTTON_CLASS)))
        increment_quantity_buttons = driver.find_elements(By.CLASS_NAME, INCREMENT_VALUE_BUTTON_CLASS)
        for button in increment_quantity_buttons:
            if button.is_displayed():
                button.send_keys(Keys.ENTER)
                break
        navigate_to_home_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, HOME_PAGE_CLASS)))
        navigate_to_home_button.click()
        navigate_to_cart_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, MY_CART_ID)))
        navigate_to_cart_button.click()
        quantity_value = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, QUANTITY_CLASS)))
        quantity_values = driver.find_elements(By.CLASS_NAME, QUANTITY_CLASS)
        quantity_value_text_after_increment = ''
        for element in quantity_values:
            if element.is_displayed():
                quantity_value_text_after_increment = element.get_attribute("innerHTML")
        if quantity_value_text_after_increment != '2':
            logsFile.write("Update cart test failed (increment didn't work), stopping script....")
            return
        logsFile.write("Update cart test finished successfully, stopping script....")
        sleep(3)
    finally:
        driver.close()
        driver.quit()


test_content()

