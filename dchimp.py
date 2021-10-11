import selenium
import webbrowser
import requests
import datetime as dt
import time

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


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
global drvier
driver = webdriver.Chrome(executable_path='./drivers/chromedriver', options=options)
wait = WebDriverWait(driver, 50)
print ("Driver Loaded.")


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
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def get_coordinates(geotags):
    lat = decimal_coords(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = decimal_coords(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    
    return (float(lat),float(lon))

def twit_geosearch(geotags,kilo):    
    twgeosearch = twurl + 'q=geocode:' + str(get_coordinates(geotags)[0]) + ',' + str(get_coordinates(geotags)[1]) + ',' + kilo + '&src=typed_query'    
    
    driver.get(twgeosearch)
    time.sleep(8)
    #twits = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/article"         
    driver.save_screenshot("twitter_geo.png")
    twits = "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/article"    
    tweet_divs = driver.find_elements_by_xpath(twits)
    #wait.until(ec.visibility_of_element_located((By.XPATH, twits)))    
    print(tweet_divs)
    
    
    print ("search URL : " + twgeosearch)
    
exif = get_exif('./img/img.jpg')
labeled = get_labeled_exif(exif)
geotags = get_geotagging(exif)

if __name__ == "__main__":
    print ("Detective Chimp v0.1")
    print ("Github : ")
    twit_geosearch(geotags,"5km")
