from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import shutil
import os
import requests
import sys
import logging
import math
import time

pause = 0

def check_if_output_folder_exists(output_folder_path):
    if os.path.isdir(output_folder_path):
        return True
    else:
        return False

def get_num_of_scrolls(num_of_images):
    ROWSPERLOAD = 7
    COLSPERROW = 4
    return math.floor(num_of_images / (ROWSPERLOAD * COLSPERROW))

def download_images_from_album(albums_list=[], output_folder_path="", num_of_images=10):

    if check_if_output_folder_exists(output_folder_path):
        logging.info("Beginning Download")
    else:
        logging.error("Folder does not exist, please create it and try again")
        sys.exit(0)

    num_of_scrolls = get_num_of_scrolls(num_of_images)

    browser = webdriver.Chrome()

    for album in albums_list:
        browser.get(album)
        image_links_list = get_image_links(browser, num_of_images, num_of_scrolls)
        scontent_list = compile_scontent_list(image_links_list, browser)
        download_images_from_scontent(scontent_list, output_folder_path)

def find(driver):
    element = driver.find_element_by_class_name("_1ktf")
    if element:
        return element
    else:
        return False

def get_image_links(browser, num_of_images, num_of_scrolls):

    if int(num_of_scrolls) > 0:
        for i in range(0, int(num_of_scrolls)):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)


    list_links = browser.find_elements_by_class_name("_2eea")
    links = []

    for link in list_links[:num_of_images]:
        links.append(link.find_element_by_css_selector('a').get_attribute('href'))

    return links

def compile_scontent_list(image_links_list, browser):

    scontent_list = []
    for image_link in image_links_list:

        browser.get(image_link)
        element = WebDriverWait(browser, 3).until(find)
        scontent = element.find_element_by_css_selector('a').get_attribute("data-ploi")
        scontent_list.append(scontent)

    return scontent_list

def get_image_name_from_facebook_url(image_url):
    return (image_url.split("/")[-1]).split("?")[0]

def download_images_from_scontent(scontent_list=[], output_foler_location=""):

    for image_url in scontent_list:
        image_name = get_image_name_from_facebook_url(image_url)

        if output_foler_location:
            image_file_path = os.path.join(output_foler_location, image_name)
        else:
            image_file_path = image_name

        resp = requests.get(image_url, stream=True)
        with open(image_file_path, 'wb') as local_file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)

        del resp

album_list = ['https://www.facebook.com/pg/DankMemesGang/photos/?tab=album&album_id=713208772115898',
              'https://www.facebook.com/pg/occreamystolenmemes/photos/?tab=album&album_id=1983141641970216',
              'https://www.facebook.com/pg/occreamystolenmemes/photos/?tab=album&album_id=1983128928638154']

download_images_from_album(album_list, 'E:\Programare\Freelance\FacebookAlbumDownloader\meme', 89)

'''lastHeight = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = browser.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight'''
