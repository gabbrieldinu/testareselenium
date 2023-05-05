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
       Pas 4 : Verificare daca produsul se afla in cos
       Pas 5 : Apasa pe butonul de "Sterge"
       Pas 6 : Verificare daca produsul nu se mai afla in cos dupa stergere 
       Pas 7 : Intoarcere la ecranul principal
       Pas 8 : Apasa pe butonul "Cosul meu"
       Pas 9 : Verificare daca cosul este gol
"""


LINK = "https://www.emag.ro/"
PATH = "C:\Program Files (x86)\chromedriver.exe"
ADD_BUTTON_CLASS = "yeahIWantThisProduct"
SEE_CART_LINK = "Vezi detalii cos"
QUANTITY_CLASS = "qty-value"
REMOVE_PRODUCT_BUTTON_CLASS = "btn-remove-product"
HOME_PAGE_CLASS = "navbar-brand"
MY_CART_ID = "my_cart"
RETURN_TO_SHOP_TEXT = "sa te intorci in magazin."

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
        try:
            no_products_found_p = WebDriverWait(driver, 1).until(ec.presence_of_element_located((By.LINK_TEXT, RETURN_TO_SHOP_TEXT)))
            logsFile.write("Delete from cart test failed (no product added), stopping script....")
            return
        except TimeoutException:
            pass
        remove_item_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, REMOVE_PRODUCT_BUTTON_CLASS)))
        remove_item_buttons = driver.find_elements(By.CLASS_NAME, REMOVE_PRODUCT_BUTTON_CLASS)
        for button in remove_item_buttons:
            if button.is_displayed():
                button.send_keys(Keys.ENTER)
                break
        no_products_found_link = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, RETURN_TO_SHOP_TEXT)))
        if not no_products_found_link:
            logsFile.write("Delete from cart test failed (product was not deleted), stopping script....")
            return
        no_products_found_link.click()
        navigate_to_cart_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, MY_CART_ID)))
        navigate_to_cart_button.click()
        no_products_found_link = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, RETURN_TO_SHOP_TEXT)))
        if not no_products_found_link:
            logsFile.write("Delete from cart test failed (product deletion didn't persist after refresh), stopping script....")
            return
        logsFile.write("Delete from cart test finished successfully, stopping script....")
        sleep(3)
    finally:
        driver.close()
        driver.quit()


test_content()
