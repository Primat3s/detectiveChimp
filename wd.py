from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from termcolor import colored, cprint

global setDriver
global driver


print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')

def choose_os():    
    setOS = input ("Choose your OS - 1. Windows  2. Linux  3. Mac  4. Mac_M1 : ")
    if setOS == "1":
        setDriver = "./drivers/chromedriver"        
        print_blue ("::: Windwos Selected.")
    elif setOS == "2":
        setDriver = "./drivers/chromedriver_l64"
        print_blue ("::: Linux Selected.")
    elif setOS == "3":
        setDriver = "./drivers/chromedriver_m64"
        print_blue ("::: Mac Selected.")
    elif setOS == "4":
        setDriver = "./drivers/chromedriver_m164"
        print_blue ("::: Mac M1 Selected.")
    else:
        setDriver = "./drivers/chromedriver_l64"
        print_blue ("::: Not matched, Linux Selected.")

def load_driver():    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        setDriver = "./drivers/chromedriver"
        driver = webdriver.Chrome(executable_path=setDriver, options=options)
        wait = WebDriverWait(driver, 50)
    except:
        print_red("!!! Web driver error")


def get_driver(get):
    load_driver()
    