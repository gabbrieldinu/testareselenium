import os
import time
import socket
import pyautogui as pag
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logsFile = open("logs.txt","w")

SLEEP_TIME_SHORT = 1.5
SLEEP_TIME_LONG = 2

os.environ['PATH'] += r"C:/SeleniumDrivers"
logsFile.write("Started Selenium\n")

LINK_EMAG = 'https://www.emag.ro/'

driver = None

def connectedToInternet():
    try:
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
        return True
    except OSError:
        pass
    return False

def setup(pageLink):
    global driver

    driver.maximize_window()
    driver.get(pageLink)
    time.sleep(SLEEP_TIME_LONG)


def teardown():
    global driver

    driver.quit()
    logsFile.close()

def press_button_at_xpath(XPath):
    global driver

    if connectedToInternet() is False:
        teardown()

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                               XPath))).click()
    time.sleep(SLEEP_TIME_SHORT)

def send_keys_at_xpath(XPath,keys):
    global driver

    if connectedToInternet() is False:
        teardown()

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable  ((By.XPATH,
                                                               XPath))).send_keys(keys)
    time.sleep(SLEEP_TIME_SHORT)

def find_element_by_xpath(XPath):
    global driver

    element = None

    if connectedToInternet() is False:
        teardown()

    try:
        element = driver.find_element(By.XPATH,XPath)
    except Exception as e:
        logsFile.write(e)
        exit(1)
    time.sleep(SLEEP_TIME_LONG)

    return element

def test_product_detail_view():
    global driver

    '''
    8) Test product detail view:
        Open browser
        Navigate to the homepage
        Locate the categories navigation menu
        Click a specific category (e.g., "Electronics")
        Verify the category page is loaded
        Click a specific product
        Verify the product detail page is loaded
        Locate and verify the product name
        Locate and verify the product price
        Locate and verify the product description
        Locate and verify the product images
        Locate and verify the product specifications
        Locate and verify the product reviews section
        Locate and verify the "Add to Cart" button
        Locate and verify the "Add to Wishlist" button
    '''

    # Open browser and navigate to homepage
    setup(LINK_EMAG)

    # Click a specific category - "Laptop, tablete si telefoane"
    press_button_at_xpath("/html/body/div[4]/div[1]/div/div[1]/ul/li[2]/a")

    # Go to a specific category - "Laptopuri"
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")

    # Verify the category page is loaded
    if driver.title != "Laptopuri. Comanda Online - eMAG.ro":
        logsFile.write("Test 8 (product detail view) failed - the category page failed to load...")
        exit(1)

    # Click a specific product
    press_button_at_xpath("/html/body/div[4]/div[2]/div/section[1]/div/div[3]/div[2]/div[5]/div[1]")

    # Locate and verify product details
    product_name = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[2]/div/div[1]/h1")
    product_price = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form/div/div[1]/div[1]/div/div/div[1]/p[2]")
    product_description = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[8]/a")
    product_images = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/a/img")
    product_specifications = find_element_by_xpath("/html/body/div[3]/div[2]/div/div[3]/div/ul/li[2]/a")
    product_reviews = find_element_by_xpath("/html/body/div[3]/div[2]/div/div[3]/div/ul/li[3]/a")
    add_to_cart_button = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form/div/div[3]/div[3]/div[1]/button")
    add_to_wishlist_button = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form/div/div[3]/div[3]/div[3]/button/span")

    if not product_name or not product_price or not product_description or not product_images or not product_specifications or not product_reviews:
        logsFile.write("Test 8 (product detail view) failed - one or more product details is missing...")
        exit(1)

    if add_to_cart_button.text != "Adauga in Cos" or not add_to_wishlist_button:
        logsFile.write("Test 8 (product detail view) failed - one or more product details is missing...")
        exit(1)

    logsFile.write("Test 8 (product detail view) finished successfully")
    teardown()
    return 0

def test_social_media_sharing():
    global driver

    '''
    14) Test social media sharing:
        Open browser
        Navigate to the homepage
        Locate the categories navigation menu
        Click a specific category (e.g., "Electronics")
        Verify the category page is loaded
        Click a specific product
        Verify the product detail page is loaded
        Locate the social media sharing buttons (e.g., Facebook, Twitter, Pinterest)
        Click the Facebook sharing button
        Verify a new window/tab opens with the Facebook share prompt
        Close the Facebook share window/tab
    '''

    # Open browser and navigate to homepage
    setup(LINK_EMAG)

    # Click a specific category - "Laptop, tablete si telefoane"
    press_button_at_xpath("/html/body/div[4]/div[1]/div/div[1]/ul/li[2]/a")

    # Go to a specific category - "Laptopuri"
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")

    # Verify the category page is loaded
    if driver.title != "Laptopuri. Comanda Online - eMAG.ro":
        logsFile.write("Test 14 (social media sharing) failed - the category page failed to load...")
        exit(1)

    # Click a specific product
    press_button_at_xpath("/html/body/div[4]/div[2]/div/section[1]/div/div[3]/div[2]/div[5]/div[1]")

    # Locate the Facebook sharing button
    share_button = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[2]/div/div[1]/div/a")

    if not share_button or share_button.text != "Share":
        logsFile.write("Test 14 (social media sharing) failed - the SHARE button is missing...")
        exit(1)

    # Click the Facebook sharing button
    share_button.click()

    # Verify a new window/tab opens with the Facebook share prompt

    if len(driver.window_handles) <= 1:
        logsFile.write("Test 14 (social media sharing) failed - failed to open a new window/tab with Facebook share prompt...")
        exit(1)

    # Close the Facebook share window/tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    logsFile.write("Test 14 (social media sharing) finished successfully")
    teardown()
    return 0

def test_wishlist_add():
    global driver

    '''
    9) Test adding a product to wishlist:
        Open browser
        Navigate to the homepage
        Locate the categories navigation menu
        Click a specific category (e.g., "Electronics")
        Verify the category page is loaded
        Click a specific product
        Verify the product detail page is loaded
        Locate the "Add to Wishlist" button
        Click the "Add to Wishlist" button
        Verify a success message or a cart update notification is displayed
        Locate and click the "Wishlist" link/button in the header/navigation bar
        Verify the wishlist page is loaded
        Locate and verify the added product in the wishlist
    '''

    # Open browser and navigate to homepage
    setup(LINK_EMAG)

    # Click a specific category - "Laptop, tablete si telefoane"
    press_button_at_xpath("/html/body/div[4]/div[1]/div/div[1]/ul/li[2]/a")

    # Go to a specific category - "Laptopuri"
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")
    press_button_at_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/aside/ul[1]/li[1]/a")

    # Verify the category page is loaded
    if driver.title != "Laptopuri. Comanda Online - eMAG.ro":
        logsFile.write("Test 3 (adding a product wishlist) failed - the category page failed to load...")
        exit(1)

    # Click a specific product
    press_button_at_xpath("/html/body/div[4]/div[2]/div/section[1]/div/div[3]/div[2]/div[5]/div[1]")
    product_title_text = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[2]/div/div[1]/h1").text

    # Locate the "Add to Wishlist" button
    add_to_wishlist_button = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form/div/div[3]/div[3]/div[3]")
    # Click the "Add to Wishlist" button
    add_to_wishlist_button.click()
    time.sleep(SLEEP_TIME_SHORT)

    # Verify a success message or a cart update notification is displayed
    wishlist_button_icon = find_element_by_xpath("/html/body/div[4]/nav[2]/div/div/div[3]/div/div[3]/a/span[1]")

    if wishlist_button_icon.text != "1":
        logsFile.write("Test 3 (adding a product wishlist) failed - the wishlist page contains a wrong number of products...")
        exit(1)

    # Locate and click the "Wishlist" link/button in the header/navigation bar
    wishlist_top_button = find_element_by_xpath("/html/body/div[4]/nav[2]/div/div/div[3]/div/div[3]/a")
    wishlist_top_button.click()
    time.sleep(SLEEP_TIME_SHORT)

    # Verify the wishlist page is loaded
    container_title = find_element_by_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div/div/div[1]/div/h3")

    if container_title.text != "Favorite":
        logsFile.write("Test 3 (adding a product wishlist) failed - the wishlist page failed to load...")
        exit(1)

    # Locate and verify the added product in the wishlist
    product_title_from_wishlist_page = find_element_by_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div/div/div[2]/div/div/div[2]/div[1]/h2/a/span")

    if product_title_text != product_title_from_wishlist_page.text:
        logsFile.write("Test 3 (adding a product wishlist) failed - missing product from wishlist...")
        exit(1)

    logsFile.write("Test 3 (adding a product to wishlist) finished successfully")
    teardown()
    return 0

def main():
    global driver

    test_product_detail_view()
    test_social_media_sharing()
    test_wishlist_add()

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    except Exception as e:
        logsFile.write("Couldn't load website\n")
        logsFile.write(e)
        exit(1)
    main()