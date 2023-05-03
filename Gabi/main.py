import os
import time
import socket
import pyautogui as pag
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# cont:
MAIL_USERNAME = "testareselenium@mail.com"
MAIL_PASSWORD = "2p9GRWgmL5W3DW9"
logsFile = open("logs.txt","w")

SLEEP_TIME_SHORT = 1.5
SLEEP_TIME_LONG = 2

os.environ['PATH'] += r"C:/SeleniumDrivers"
logsFile.write("Started Selenium\n")

LINK_EMAG = 'https://www.emag.ro/'
LINK_GENERATOR_PAROLA = 'https://passwordsgenerator.net/'
LINK_MAIL = 'https://www.mail.com/'

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




def test15():
    global driver
    """
    Descrierea testului:
        Pasul 1: Deschideți browser-ul
        Pasul 2: Navigați la pagina de pornire
        Pasul 3: Faceți clic pe butonul "Contact" din antet/subsol/meniu de navigare
        Pasul 4: Apasa pe butonul "Aici gasesti"
        Pasul 5: Apasa pe campul de cautare de oras
        Pasul 6: Verifica ca s-a afisat un dropdown cu orase
        Pasul 7: Introduceți o locație validă, de exemplu "Bucuresti"
        Pasul 8: Verfica ca exista doar orasul "Bucuresti" in lista
        Pasul 9: Apasa pe orasul "Bucuresti"
        Pasul 10: Apasa pe campul de cautare a localitatii
        Pasul 11: Verifica ca s-a afisat un dropdown cu localitati
        Pasul 12: Introduceți o locație validă, de exemplu "Bucuresti (Sectorul 6)"
        Pasul 13: Verfica ca exista doar "Bucuresti (Sectorul 6)" in lista
        Pasul 14: Apasa pe "Bucuresti (Sectorul 6)"
        Pasul 15: Apasa pe campul de cautare showroom
        Pasul 16: Cauta un showroom, (de exemplu ("Crangasi")
        Pasul 17: Apasa pe butonul "Showroom Crangasi"
        Pasul 18: Apasa pe butonul "Deschide in Google Maps"
        Pasul 19: Verifica ca s-a deschis un alt tab
        Pasul 20: Intra pe noul tab deschis
        Pasul 21: Verifica ca site-ul pe care a intrat este google maps si coordonatele sunt ale showroomului din Crangasi, Bucurestiuli ("44.45041,26.044972")
        Pasul 22: Inchide tab-ul nou
        Pasul 23: Revino in pagina emag
        Pasul 24: Inchide browserul
    """

    # Pasul 1: Deschideți browser-ul
    # Pasul 2: Navigați la pagina de pornire
    setup(LINK_EMAG)
    press_button_at_xpath("/html/body/div[1]/div/div/button")
    # Pas 2 : Apasa pe butonul "Accept" referitor la cookieuri
    press_button_at_xpath("/html/body/div[9]/div/div[2]/button[1]")

    # Pas 3 : Apasa pe butonul "x" de a inchide popup-ul de login
    press_button_at_xpath("/html/body/div[9]/div/button")

    # Pasul 3: Faceți clic pe butonul "Contact" din antet/subsol/meniu de navigare
    press_button_at_xpath("/html/body/div[4]/footer/div[2]/div/div/div[3]/ul/li[2]/a")

    # Pasul 4: Apasa pe butonul "Aici gasesti"
    press_button_at_xpath("/html/body/div[2]/div/div[2]/div[4]/div[1]/p[6]/a")

    # Pasul 5: Apasa pe campul de cautare de oras
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div/div[1]/div/div/a")

    # Pasul 6: Verifica ca s-a afisat un dropdown cu orase
    dropdown_orase = find_element_by_xpath("/html/body/div[10]/div/div[2]")

    if dropdown_orase is None:
        exit(1)

    # Pasul 7: Introduceți o locație validă, de exemplu "Bucuresti"
    send_keys_at_xpath("/html/body/div[10]/div/div[1]/input", "Bucuresti")

    # Pasul 9: Apasa pe orasul "Bucuresti"
    press_button_at_xpath("/html/body/div[10]/div/div[2]/a[1]")


    # Pasul 10: Apasa pe campul de cautare a localitatii
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div[1]/div/div/div[2]/div/a")

    # Pasul 12: Introduceți o locație validă, de exemplu "Bucuresti (Sectorul 6)"
    send_keys_at_xpath("/html/body/div[11]/div/div[1]/input","Bucuresti (Sectorul 6)")

    # Pasul 14: Apasa pe "Bucuresti (Sectorul 6)"
    press_button_at_xpath("/html/body/div[11]/div/div[2]/a[6]")

    # Pasul 16: Cauta un showroom, (de exemplu ("Crangasi")
    send_keys_at_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/input","Showroom "
                                                                                                         "Crangasi")
    # Pasul 17: Apasa pe butonul "Showroom Crangasi"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div[2]/div/div[2]/div[2]/ul/li/span")


    # Pasul 18: Apasa pe butonul "Deschide in Google Maps"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section/div/div[2]/div[2]/div/div[2]/div/div[2]/a")

    # Pasul 19: Verifica ca s-a deschis un alt tab
    if len(driver.window_handles) > 1:

        # Pasul 20: Intra pe noul tab deschis
        driver.switch_to.window(driver.window_handles[1])
        logsFile.write('Switched to new tab')


        # Pasul 21: Apasa pe "Reject All", in pop-ul de cookies
        press_button_at_xpath("/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button")

        # Pasul 20: Verifica ca site-ul pe care a intrat este google maps si coordonatele sunt ale showroomului din Crangasi, Bucurestiuli ("44.45041,26.044972")
        if "Google Maps" in driver.title and "" in driver.title:
            logsFile.write("Google maps opened ok, closing ...")

        # Pasul 21: Inchide tab-ul nou
        driver.close()

    # Revino in pagina Emag
    driver.switch_to.window(driver.window_handles[0])

    # Pasul 22: Inchide browserul
    teardown()

def test5():
    global driver

    """
    Descrierea testului:
        Pas 1 : Deschide browser pe site-ul emag
        Pas 2 : Apasa pe butonul "Accept" referitor la cookieuri
        Pas 3 : Apasa pe butonul "x" de a inchide popup-ul de login
        Pas 4 : Introdu in bara de cautare "laptop"
        Pas 5 : Apasa pe butonul de cautare
        Pas 6 : Verifica ca se afiseaza doar produse din categorie "Laptopuri"
        Pas 7 : Filtreaza dupa "Toate Produsele" 
        Pas 8: Introdu in campul de filtrare a procesoarelor "AMD Ryzen™ 9"
        Pas 9 : Apasa pe campul de filtrare "AMD Ryzen™ 9"
        Pas 10 : Apasa in campul de filtrare "Capacitate memorie" pe butonul "Peste 16 GB"
        Pas 11 :  Apasa in campul de filtrare "Brand" pe butonul "Acer"
        Pas 12 :  Apasa in campul de filtrare "Tip Laptop" pe butonul "Gaming"
        Pas 13 :  Apasa in campul de filtrare "Disponibilitate" pe butonul "In Stoc"
        Pas 14 : Scroll in partea de sus a paginii
        Pas 15 : Verifica ca s-a afisat produsul corect
    """
    # Pas 1 : Deschide browser pe site-ul emag
    setup(LINK_EMAG)

    # Pas 2 : Apasa pe butonul "Accept" referitor la cookieuri
    press_button_at_xpath("/html/body/div[9]/div/div[2]/button[1]")

    # Pas 3 : Apasa pe butonul "x" de a inchide popup-ul de login
    press_button_at_xpath("/html/body/div[9]/div/button")

    # Pas 4 : Introdu in bara de cautare textul "laptop"
    send_keys_at_xpath("/html/body/div[4]/nav[1]/div/div/div[2]/div/form/div[1]/div[1]/input[2]", "laptop")

    # Pas 5 : Apasa pe butonul de cautare
    press_button_at_xpath("/html/body/div[4]/nav[1]/div/div/div[2]/div/form/div[1]/div[2]/button[2]")

    # Pas 6 : Verifica ca se afiseaza doar produse din categorie "Laptopuri"
    categorie_afisata = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[2]/a/div/div[2]/div")
    if categorie_afisata.text == "Laptopuri":
        logsFile.write("Categorie afisata corecta, continuare...")
    else:
        exit(1)

    # Pas 7 : Filtreaza dupa "Toate Produsele"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/div/a[1]")

    # Pas 8: Introdu in campul de filtrare a procesoarelor "AMD Ryzen™ 9"
    send_keys_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/input","AMD Ryzen™ 9")

    # Pas 9 : Apasa pe campul de filtrare "AMD Ryzen™ 9"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/a[14]")

    # Pas 10 : Apasa in campul de filtrare "Capacitate memorie" pe butonul "Peste 16 GB"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[3]/div/div/a[2]")

    # Pas 11 :  Apasa in campul de filtrare "Brand" pe butonul "Acer"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[4]/div/div/a[4]")

    # Pas 12 :  Apasa in campul de filtrare "Tip Laptop" pe butonul "Gaming"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[5]/div/div/a")

    # Pas 13 :  Apasa in campul de filtrare "Disponibilitate" pe butonul "In Stoc"
    press_button_at_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[1]/div[2]/div[2]/div[11]/div/div/a[1]")

    # Pas 14 : Scroll in partea de sus a paginii
    driver.execute_script("window.scrollTo(0, 0)")

    # Pas 15 : Verifica ca s-a afisat produsul corect
    laptop_filtrat = find_element_by_xpath("/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[2]/div[5]/div/div/div/div[3]/a/div/img")
    if laptop_filtrat.get_attribute("alt") == "Laptop Gaming Acer Nitro 5 AN517-42 cu procesor AMD Ryzen™ 9 6900HX pana la 4.90 GHz, 17.3\" QHD, IPS, 165Hz, 32GB, 1TB SSD, NVIDIA® GeForce RTX™ 3070 Ti 8GB GDDR6, No OS, Black":
        logsFile.write("Test finished successfully, stopping script....")

    teardown()

    return 0

def generate_password ():
    setup(LINK_GENERATOR_PAROLA)
    press_button_at_xpath("/html/body/div/div[4]/div[1]")
    inputBar = find_element_by_xpath('/html[1]/body[1]/div[1]/div[5]/div[2]/input[1]')

    return inputBar.get_attribute('value')


def login_to_email(username=MAIL_USERNAME, password=MAIL_PASSWORD):
    global driver

    """
        Descrierea testului:
            Pas 1 : Deschide linkul emailului
            Pas 2 : Apasa pe butonul de "Accept all" de la cookieuri
            Pas 3 : Apasa pe butonul de "Log In"
            Pas 4 : Introdu in campul de "Username", numele de utilizator definit mai sus
            Pas 5 : Introdu in campul "Password", parola definita mai sus
            Pas 6 : Apasa pe butonul de "Log In"
            Pas 7 : Apasa pe butonul "Email"
            Pas 8 : Apasa pe ultimul mail din lista
        """
    # Pas 1 : Deschide linkul emailului
    setup(LINK_MAIL)

    # Pas 2 : Apasa pe butonul de "Accept all" de la cookieuri - aici am folosit pyautogui pentru ca popup-ul este generat dinamic independent de html
    pag.moveTo(x=1009, y=654)
    pag.click()
    
    # Pas 3 : Apasa pe butonul de "Log In" 
    time.sleep(SLEEP_TIME_SHORT)

    press_button_at_xpath("/html/body/div[1]/div/div[1]/header/div[1]/div[3]/a[2]")

    # Pas 4 : Introdu in campul de "Username", numele de utilizator definit mai sus
    send_keys_at_xpath("/html/body/div[1]/div/div[1]/div/div/div/div[2]/form/div[1]/input", username)

    # Pas 5 : Introdu in campul "Password", parola definita mai sus
    send_keys_at_xpath("/html/body/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/input", password)

    # Pas 6 : Apasa pe butonul de "Log In"
    press_button_at_xpath("/html/body/div[1]/div/div[1]/div/div/div/div[2]/form/button")


    # Pas 7 : Apasa pe butonul "Email"
    press_button_at_xpath("/html/body/nav/nav-actions-menu/div[1]/div[1]/a[2]")

    # Pas 8 : Apasa pe ultimul mail din lista
    press_button_at_xpath("/html/body/div[3]/div[3]/div[3]/div[1]/div[1]/div/form/div[3]/div/div/table/tbody/tr[1]/td[2]")

    teardown()

def main():
    global driver
    test15()

    #login_to_email()

    #test5()

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome()
    except Exception as e:
        logsFile.write("Couldn't load website\n")
        logsFile.write(e)
        exit(1)
    main()
