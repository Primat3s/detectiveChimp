import selenium
import webbrowser
import requests
import datetime as dt
import time

import wd

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
print_blue = lambda x: cprint(x, 'blue')


def get_exif(filename):
    try:
        image = Image.open(filename)
        image.verify()
    except:
        print_red("!!! Image error")
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
    try:
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse(loc)
        print(location)
        print_green("LocationName")
        print(location.address)
    except:
        location = "Not found"
        print_red("!!! Location name error")    
    

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def get_coordinates(geotags):
    
    lat = decimal_coords(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = decimal_coords(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    
    return (float(lat),float(lon))

def twit_geosearch(geotags, kilo="5", since="", until=""):            
    #wd.load_driver()    
    if (since=="" or until ==""):        
        twgeosearch = twurl + 'geocode:' + str(get_coordinates(geotags)[0]) + ',' + str(get_coordinates(geotags)[1]) + ',' + kilo + '&src=typed_query'
    else:
        twgeosearch = twurl + 'geocode:' + str(get_coordinates(geotags)[0]) + ',' + str(get_coordinates(geotags)[1]) + ',' + kilo + ' since:'+ since + ' until:' + until + '&src=typed_query'            
    #wd.get_driver(twgeosearch)
    time.sleep(8)    
    #twits = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/article"         
    #tweet_divs = driver.find_elements_by_xpath(twits)
    #wait.until(ec.visibility_of_element_located((By.XPATH, twits)))        
    print_green ("::: URL ")
    print_blue (twgeosearch)

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
        print_green("GeoTags")
        print(geotags)
        reverse_geo(get_coordinates(geotags))

    except KeyError:
        pass        
    
    print("-------------------------------------------------------------------------------")
    kilo = str(input("Input distance to search (ex. 5km) - Default 5km : ") or "5km")
    since = str(input("[*optional*] Input Since date (ex. 2021-10-01) : "))
    until = str(input("[*optional*] Input Until date (ex. 2021-10-11) : "))
    twit_geosearch(geotags,kilo,since,until)