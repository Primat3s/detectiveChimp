import pyfiglet
import selenium
import webbrowser
import requests
import datetime as dt
import time

from geopy.geocoders import Nominatim
from pyfiglet import Figlet
from termcolor import colored, cprint
from bs4 import BeautifulSoup

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

twurl = "https://twitter.com/search?q="

print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')

def load_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    global driver
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver', options=options)
    wait = WebDriverWait(driver, 50)

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_geotagging(exif):
    if not exif:
        print_red("!!! No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                print_red("!!! No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def reverse_geo(loc):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.reverse(loc)
    print_green("Location")
    print(location.address)

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def get_coordinates(geotags):
    lat = decimal_coords(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = decimal_coords(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    
    return (float(lat),float(lon))

def twit_geosearch(geotags, kilo, since, until):            
    load_driver()
    print (since)
    print (until)
    if (since=="" or until ==""):
        twgeosearch = twurl + 'geocode:' + str(get_coordinates(geotags)[0]) + ',' + str(get_coordinates(geotags)[1]) + ',' + kilo + '&src=typed_query'
    else:
        twgeosearch = twurl + 'geocode:' + str(get_coordinates(geotags)[0]) + ',' + str(get_coordinates(geotags)[1]) + ',' + kilo + ' since:'+ since + ' until:' + until + '&src=typed_query'            

    driver.get(twgeosearch)
    time.sleep(8)    
    twits = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/article"         
    tweet_divs = driver.find_elements_by_xpath(twits)
    #wait.until(ec.visibility_of_element_located((By.XPATH, twits)))    
    print(tweet_divs)
    print ("search URL : " + twgeosearch)

def twit_geo():
    try:
        img = input("Input image path (ex. ./img/img.jpg) : ")
        exif = get_exif(img)
        labeled = get_labeled_exif(exif)        
        print("-------------------------------------------------------------------------------")          
        for attribute, value in labeled.items():
            if (attribute=="Make" or attribute=="Model" or attribute=="Software" or attribute=="DateTime" or attribute=="DateTimeOriginal" or attribute=="DateTimeDigitized" or attribute=="UserComment"):
                print_green(attribute)
                print(value)
        geotags = get_geotagging(exif)
        reverse_geo(get_coordinates(geotags))
        """
        print_green("Brand")
        print(str(labeled["Make"]))
        print_green("Model")
        print(str(labeled["Model"]))
        print_green("Software")
        print(str(labeled["Software"]))
        print_green("DateTime")
        print(str(labeled["DateTime"]))
        print_green("OriginalDateTime")
        print(str(labeled["DateTimeOriginal"]))
        print_green("DigitalDateTime")
        print(str(labeled["DateTimeDigitized"]))
        print_green("UserComment")
        print(str(labeled["UserComment"]))
        
        """
    except KeyError:
        pass        
    
    print("-------------------------------------------------------------------------------")
    kilo = str(input("Input distance to search (ex. 5km) - Default 5km : ") or "5km")
    since = str(input("[*optional*] Input Since date (ex. 2021-10-01) : "))
    until = str(input("[*optional*] Input Until date (ex. 2021-10-11) : "))
    twit_geosearch(geotags,kilo,since,until)
  
if __name__ == "__main__":    
    title = pyfiglet.figlet_format("Detective Chimp v0.1", font="slant")
    print (title)
    print_green ("Author : Chamchi")
    print ("Github : https://github.com/Primat3s/detectiveChimp")
    print ("-------------------------------------------------\n")
    print_green ("1. Twitter Geo search\n")


    usersel = input("Please select number : ")
    print(usersel)
    if usersel == "1":
        twit_geo()        
    else :
        print_red("Invalid number!")
    
